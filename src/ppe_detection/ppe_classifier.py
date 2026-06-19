"""
SAFE / UNSAFE classification logic for PPE compliance.

A worker (Person bounding box) is classified as:
  SAFE   — if a Hardhat AND a Safety Vest are detected overlapping or near them.
  UNSAFE — if either PPE item is missing or a violation class is detected.

This module is independent of tracking, databases, and APIs.
"""

from dataclasses import dataclass
from enum import Enum

from .inference import Detection


class ComplianceStatus(str, Enum):
    SAFE   = "SAFE"
    UNSAFE = "UNSAFE"


PERSON_CLASS_ID      = 5
HARDHAT_CLASS_ID     = 0
VEST_CLASS_ID        = 7
NO_HARDHAT_CLASS_ID  = 2
NO_VEST_CLASS_ID     = 4


@dataclass
class WorkerCompliance:
    person_bbox: tuple[int, int, int, int]
    status: ComplianceStatus
    has_hardhat: bool
    has_vest: bool
    violations: list[str]


def _iou(box_a: tuple, box_b: tuple) -> float:
    """Compute Intersection-over-Union between two (x1,y1,x2,y2) boxes."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    if inter == 0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return inter / (area_a + area_b - inter)


def _overlaps(person_box: tuple, ppe_box: tuple, iou_thresh: float = 0.05) -> bool:
    """Return True if ppe_box overlaps the person_box above threshold."""
    return _iou(person_box, ppe_box) >= iou_thresh


def classify_workers(
    detections: list[Detection],
    iou_thresh: float = 0.05,
) -> list[WorkerCompliance]:
    """
    Classify each detected person as SAFE or UNSAFE.

    Strategy:
    1. Isolate Person boxes.
    2. For each person, check if a Hardhat and Safety Vest overlap.
    3. Also flag explicit violation classes (NO-Hardhat, NO-Safety Vest).
    """
    persons  = [d for d in detections if d.class_id == PERSON_CLASS_ID]
    hardhats = [d for d in detections if d.class_id == HARDHAT_CLASS_ID]
    vests    = [d for d in detections if d.class_id == VEST_CLASS_ID]
    no_hats  = [d for d in detections if d.class_id == NO_HARDHAT_CLASS_ID]
    no_vests = [d for d in detections if d.class_id == NO_VEST_CLASS_ID]

    results: list[WorkerCompliance] = []

    for person in persons:
        pb = person.bbox
        has_hardhat = any(_overlaps(pb, h.bbox, iou_thresh) for h in hardhats)
        has_vest    = any(_overlaps(pb, v.bbox, iou_thresh) for v in vests)

        # Explicit violation detections near the person also count as unsafe
        viol_hat  = any(_overlaps(pb, n.bbox, iou_thresh) for n in no_hats)
        viol_vest = any(_overlaps(pb, n.bbox, iou_thresh) for n in no_vests)

        if viol_hat:
            has_hardhat = False
        if viol_vest:
            has_vest = False

        violations: list[str] = []
        if not has_hardhat:
            violations.append("Missing Hardhat")
        if not has_vest:
            violations.append("Missing Safety Vest")

        status = ComplianceStatus.SAFE if not violations else ComplianceStatus.UNSAFE
        results.append(WorkerCompliance(pb, status, has_hardhat, has_vest, violations))

    return results


def compliance_color(status: ComplianceStatus) -> tuple[int, int, int]:
    """Return BGR color for overlaying compliance status."""
    return (0, 255, 0) if status == ComplianceStatus.SAFE else (0, 0, 255)
