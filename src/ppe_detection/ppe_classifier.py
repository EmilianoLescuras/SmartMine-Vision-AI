"""
Worker PPE compliance classification for the SmartMine unified model.

The unified dataset encodes compliance in two ways:
  1. Embedded in person class  (riskalert / deteccion_escenarios sources):
       person_con_casco (1) → hardhat present
       person_sin_casco (2) → hardhat missing  [violation]
       person_sin_chaleco (4) → vest missing   [violation]
       … etc. for gloves, eyewear, respirator, reflective clothing

  2. Separate PPE objects  (CSS source):
       Person (0) detected separately from hardhat (27) / safety_vest (28) /
       mask (13). Compliance is inferred via IoU overlap.

A worker is SAFE when at minimum: hardhat=True AND vest=True.
Other violations (gloves, eyewear, …) are reported but do not flip the
status to UNSAFE on their own — adapt thresholds to site requirements.

For any worker (regardless of source class) we ALSO scan overlapping
separate PPE detections. The embedded class signal takes precedence;
separate detections only fill attributes still unknown. This makes the
classifier robust to mixed-source predictions at inference time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .inference import Detection
from .utils import PERSON_CLASS_IDS


class ComplianceStatus(str, Enum):
    SAFE    = "SAFE"
    UNSAFE  = "UNSAFE"
    UNKNOWN = "UNKNOWN"   # generic person with no overlapping PPE found


_REQUIRED = {"hardhat", "vest"}

_ATTRIBUTES: tuple[str, ...] = (
    "hardhat", "vest", "gloves", "eyewear", "respirator", "reflective", "mask",
)

_CLASS_ATTRIBUTE: dict[int, tuple[str, bool]] = {
    1:  ("hardhat",    True),
    2:  ("hardhat",    False),
    3:  ("vest",       True),
    4:  ("vest",       False),
    5:  ("gloves",     True),
    6:  ("gloves",     False),
    7:  ("eyewear",    True),
    8:  ("eyewear",    False),
    9:  ("respirator", True),
    10: ("respirator", False),
    11: ("reflective", True),
    12: ("reflective", False),
}

_SEPARATE_PPE: dict[int, str] = {
    27: "hardhat",
    28: "vest",
    13: "mask",
}


@dataclass
class WorkerCompliance:
    person_bbox:     tuple[int, int, int, int]
    person_class_id: int
    status:          ComplianceStatus
    attributes:      dict[str, bool | None] = field(default_factory=dict)
    violations:      list[str]              = field(default_factory=list)
    confidence:      float                  = 0.0


def _iou(a: tuple, b: tuple) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    if inter == 0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return inter / (area_a + area_b - inter)


def _contains_center(person_box: tuple, item_box: tuple) -> bool:
    """True when the item's center lies inside the person box.

    More lenient than IoU when a small PPE item (hardhat) sits at the top
    of a tall person box — IoU stays small but the spatial relationship is
    clear.
    """
    px1, py1, px2, py2 = person_box
    ix1, iy1, ix2, iy2 = item_box
    cx, cy = (ix1 + ix2) / 2, (iy1 + iy2) / 2
    return px1 <= cx <= px2 and py1 <= cy <= py2


def _overlaps(person_box: tuple, item_box: tuple, iou_thresh: float) -> bool:
    return _iou(person_box, item_box) >= iou_thresh or _contains_center(person_box, item_box)


def _resolve_status(attrs: dict[str, bool | None]) -> tuple[ComplianceStatus, list[str]]:
    violations: list[str] = []
    unknown_required = False

    for attr in _REQUIRED:
        val = attrs.get(attr)
        if val is False:
            violations.append(f"Falta {attr}")
        elif val is None:
            unknown_required = True

    if violations:
        return ComplianceStatus.UNSAFE, violations
    if unknown_required:
        return ComplianceStatus.UNKNOWN, []
    return ComplianceStatus.SAFE, []


def classify_workers(
    detections: list[Detection],
    iou_thresh: float = 0.05,
) -> list[WorkerCompliance]:
    """
    Classify each detected worker as SAFE / UNSAFE / UNKNOWN.

    Workers come from any detection whose class_id is in PERSON_CLASS_IDS (0-12).
    The embedded class fills the attribute it encodes (e.g. person_sin_casco
    → hardhat=False). Separate PPE items (hardhat=27, safety_vest=28, mask=13)
    fill any remaining unknown attributes via IoU / center-containment matching.
    """
    workers   = [d for d in detections if d.class_id in PERSON_CLASS_IDS]
    ppe_items = [d for d in detections if d.class_id in _SEPARATE_PPE]

    results: list[WorkerCompliance] = []

    for worker in workers:
        cls = worker.class_id
        attrs: dict[str, bool | None] = {a: None for a in _ATTRIBUTES}

        attr_info = _CLASS_ATTRIBUTE.get(cls)
        if attr_info is not None:
            attribute, is_compliant = attr_info
            attrs[attribute] = is_compliant

        for ppe in ppe_items:
            attr = _SEPARATE_PPE[ppe.class_id]
            if attrs.get(attr) is not None:
                continue
            if _overlaps(worker.bbox, ppe.bbox, iou_thresh):
                attrs[attr] = True

        status, violations = _resolve_status(attrs)
        results.append(WorkerCompliance(
            person_bbox=worker.bbox,
            person_class_id=cls,
            status=status,
            attributes=attrs,
            violations=violations,
            confidence=getattr(worker, "confidence", 0.0),
        ))

    return results


def compliance_color(status: ComplianceStatus) -> tuple[int, int, int]:
    """Return BGR overlay color for a compliance status."""
    return {
        ComplianceStatus.SAFE:    (0, 220, 0),
        ComplianceStatus.UNSAFE:  (0, 0, 220),
        ComplianceStatus.UNKNOWN: (0, 165, 255),
    }[status]


def compliance_summary(results: list[WorkerCompliance]) -> dict[str, int]:
    """Return counts of SAFE / UNSAFE / UNKNOWN workers."""
    summary = {"SAFE": 0, "UNSAFE": 0, "UNKNOWN": 0}
    for r in results:
        summary[r.status.value] += 1
    return summary
