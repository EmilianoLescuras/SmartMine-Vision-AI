"""
Smoke test for SPEC-001 AC-5.

Runs the full detection + compliance pipeline end-to-end using the generic
yolov8n.pt (COCO pre-trained, downloaded automatically on first run).
Does NOT require the custom smartmine dataset — a synthetic 480x640 BGR frame
is used as the test image.

Exit codes:
  0 — pipeline ran without errors, overlay saved to outputs/images/
  1 — any exception
"""

import sys
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ppe_detection.inference import draw_detections, load_model, predict_image
from src.ppe_detection.ppe_classifier import classify_workers, compliance_summary
from src.ppe_detection.utils import OUTPUTS_DIR, ensure_dirs

SMOKE_WEIGHTS = PROJECT_ROOT / "models" / "yolov8n.pt"
SMOKE_OUTPUT  = OUTPUTS_DIR / "images" / "smoke_test_overlay.png"


def _synthetic_frame() -> np.ndarray:
    """Return a 480×640 BGR frame that looks like a construction scene."""
    frame = np.full((480, 640, 3), (60, 80, 40), dtype=np.uint8)
    # sky
    frame[:160] = (200, 160, 80)
    # hard-hat yellow blob (person placeholder — model may or may not detect)
    cv2.ellipse(frame, (320, 200), (30, 40), 0, 0, 360, (0, 200, 255), -1)
    cv2.rectangle(frame, (290, 240), (350, 340), (80, 80, 180), -1)
    return frame


def main() -> None:
    ensure_dirs()

    print("─" * 50)
    print("SmartMine Smoke Test — SPEC-001 AC-5")
    print("─" * 50)

    print(f"\n[1/4] Loading model: {SMOKE_WEIGHTS.name}")
    model = load_model(SMOKE_WEIGHTS)
    print("      Model loaded OK")

    print("\n[2/4] Running inference on synthetic frame …")
    frame = _synthetic_frame()
    detections = predict_image(model, frame, conf=0.25)
    print(f"      Detections: {len(detections)}")
    for d in detections:
        print(f"        [{d.class_id:2d}] {d.class_name:<20} conf={d.confidence:.3f}")

    print("\n[3/4] Running compliance classification …")
    workers = classify_workers(detections)
    summary = compliance_summary(workers)
    print(f"      Workers: {len(workers)}  |  {summary}")

    print("\n[4/4] Saving overlay …")
    annotated = draw_detections(frame, detections)
    cv2.imwrite(str(SMOKE_OUTPUT), annotated)
    print(f"      Saved → {SMOKE_OUTPUT.relative_to(PROJECT_ROOT)}")

    print("\n✓ Smoke test passed — pipeline is functional.\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\n✗ Smoke test FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
