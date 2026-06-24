"""Unit tests for src/ppe_detection/ppe_classifier.py (SPEC-002 AC-4)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ppe_detection.inference import Detection
from src.ppe_detection.ppe_classifier import (
    ComplianceStatus,
    WorkerCompliance,
    classify_workers,
    compliance_summary,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def _det(class_id: int, bbox=(0, 0, 100, 200), conf=0.9) -> Detection:
    return Detection(class_id=class_id, class_name=str(class_id),
                     confidence=conf, bbox=bbox)


# ── embedded-class signal ─────────────────────────────────────────────────────

class TestEmbeddedClassSignal:
    def test_person_con_casco_y_chaleco_is_safe(self):
        # class 1 = person_con_casco, class 3 = person_con_chaleco
        # Two separate workers, each with embedded hardhat/vest
        dets = [_det(1), _det(3)]
        workers = classify_workers(dets)
        assert len(workers) == 2
        statuses = {w.status for w in workers}
        # Worker from class 1: hardhat=True, vest=None → UNKNOWN (vest not known)
        # Worker from class 3: hardhat=None, vest=True  → UNKNOWN (hardhat not known)
        assert all(w.status == ComplianceStatus.UNKNOWN for w in workers)

    def test_person_sin_casco_is_unsafe(self):
        # class 2 = person_sin_casco → hardhat=False → UNSAFE
        workers = classify_workers([_det(2)])
        assert len(workers) == 1
        assert workers[0].status == ComplianceStatus.UNSAFE
        assert workers[0].attributes["hardhat"] is False
        assert "Falta hardhat" in workers[0].violations

    def test_person_sin_chaleco_is_unsafe(self):
        workers = classify_workers([_det(4)])  # class 4 = person_sin_chaleco
        assert workers[0].status == ComplianceStatus.UNSAFE
        assert "Falta vest" in workers[0].violations

    def test_generic_person_is_unknown(self):
        workers = classify_workers([_det(0)])  # class 0 = generic person
        assert workers[0].status == ComplianceStatus.UNKNOWN
        assert workers[0].violations == []

    def test_embedded_violation_takes_precedence_over_overlapping_ppe(self):
        # Worker class 2 (sin_casco) overlaps a separate hardhat (class 27).
        # Embedded signal wins → still UNSAFE.
        worker_bbox = (0, 0, 100, 200)
        hardhat_bbox = (20, 0, 80, 40)   # center inside worker_bbox
        dets = [_det(2, bbox=worker_bbox), _det(27, bbox=hardhat_bbox)]
        workers = classify_workers(dets)
        assert workers[0].status == ComplianceStatus.UNSAFE
        # hardhat attribute should still be False (embedded overrides)
        assert workers[0].attributes["hardhat"] is False


# ── spatial resolution (IoU / center-containment) ────────────────────────────

class TestSpatialResolution:
    def test_overlapping_hardhat_and_vest_yields_safe(self):
        # Generic person (class 0) with both hardhat (27) and vest (28) overlapping.
        worker_bbox   = (0, 0, 100, 200)
        hardhat_bbox  = (20, 0, 80, 40)    # center inside worker
        vest_bbox     = (10, 100, 90, 160)  # center inside worker
        dets = [
            _det(0,  bbox=worker_bbox),
            _det(27, bbox=hardhat_bbox),
            _det(28, bbox=vest_bbox),
        ]
        workers = classify_workers(dets)
        assert workers[0].status == ComplianceStatus.SAFE
        assert workers[0].attributes["hardhat"] is True
        assert workers[0].attributes["vest"] is True

    def test_non_overlapping_ppe_not_assigned(self):
        # Hardhat far away from the worker — should not be assigned.
        worker_bbox  = (0, 0, 100, 200)
        hardhat_bbox = (500, 500, 560, 540)  # no overlap
        dets = [_det(0, bbox=worker_bbox), _det(27, bbox=hardhat_bbox)]
        workers = classify_workers(dets)
        assert workers[0].attributes["hardhat"] is None
        assert workers[0].status == ComplianceStatus.UNKNOWN

    def test_center_containment_triggers_on_small_ppe(self):
        # Tiny hardhat whose center is inside the worker box but IoU < 0.05.
        worker_bbox  = (0, 0, 200, 400)    # large worker
        hardhat_bbox = (90, 5, 110, 25)    # tiny hat, center (100, 15) inside worker
        dets = [_det(0, bbox=worker_bbox), _det(27, bbox=hardhat_bbox)]
        workers = classify_workers(dets)
        assert workers[0].attributes["hardhat"] is True


# ── IoU helper ────────────────────────────────────────────────────────────────

class TestIou:
    def test_identical_boxes_iou_is_1(self):
        from src.ppe_detection.ppe_classifier import _iou
        assert _iou((0, 0, 10, 10), (0, 0, 10, 10)) == pytest.approx(1.0)

    def test_non_overlapping_boxes_iou_is_0(self):
        from src.ppe_detection.ppe_classifier import _iou
        assert _iou((0, 0, 5, 5), (10, 10, 20, 20)) == 0.0

    def test_partial_overlap(self):
        from src.ppe_detection.ppe_classifier import _iou
        # 5×5 overlap out of two 10×10 boxes sharing a corner
        iou = _iou((0, 0, 10, 10), (5, 5, 15, 15))
        # intersection = 5*5=25, union = 100+100-25=175
        assert iou == pytest.approx(25 / 175)


# ── compliance_summary ────────────────────────────────────────────────────────

class TestComplianceSummary:
    def test_summary_counts(self):
        workers = [
            WorkerCompliance((0,0,1,1), 0, ComplianceStatus.SAFE,    {}, []),
            WorkerCompliance((0,0,1,1), 2, ComplianceStatus.UNSAFE,  {}, ["Falta hardhat"]),
            WorkerCompliance((0,0,1,1), 0, ComplianceStatus.UNKNOWN, {}, []),
            WorkerCompliance((0,0,1,1), 0, ComplianceStatus.UNKNOWN, {}, []),
        ]
        s = compliance_summary(workers)
        assert s == {"SAFE": 1, "UNSAFE": 1, "UNKNOWN": 2}

    def test_empty_list(self):
        assert compliance_summary([]) == {"SAFE": 0, "UNSAFE": 0, "UNKNOWN": 0}
