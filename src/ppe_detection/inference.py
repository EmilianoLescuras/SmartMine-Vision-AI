"""Image and video inference for the PPE detection model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

from .utils import CLASS_COLORS, CLASS_NAMES, OUTPUTS_DIR, ensure_dirs


@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[int, int, int, int]   # x1, y1, x2, y2 (pixels)


def load_model(weights_path: Path) -> YOLO:
    """Load a YOLO model from weights file."""
    return YOLO(str(weights_path))


def predict_image(
    model: YOLO,
    image: np.ndarray,
    conf: float = 0.4,
    iou: float = 0.45,
) -> list[Detection]:
    """Run inference on a single frame and return structured detections."""
    results = model.predict(image, conf=conf, iou=iou, verbose=False)
    detections: list[Detection] = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append(Detection(
            class_id=cls_id,
            class_name=CLASS_NAMES.get(cls_id, str(cls_id)),
            confidence=float(box.conf[0]),
            bbox=(x1, y1, x2, y2),
        ))
    return detections


def draw_detections(image: np.ndarray, detections: list[Detection]) -> np.ndarray:
    """Draw bounding boxes and labels on a frame."""
    canvas = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det.bbox
        color = CLASS_COLORS.get(det.class_id, (200, 200, 200))
        label = f"{det.class_name} {det.confidence:.2f}"
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
        cv2.putText(canvas, label, (x1, max(y1 - 6, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
    return canvas


def run_image_inference(
    model: YOLO,
    image_path: Path,
    conf: float = 0.4,
    save: bool = True,
) -> tuple[np.ndarray, list[Detection]]:
    """Infer on a single image file and optionally save the annotated result."""
    ensure_dirs()
    image = cv2.imread(str(image_path))
    detections = predict_image(model, image, conf=conf)
    annotated = draw_detections(image, detections)

    if save:
        out_path = OUTPUTS_DIR / "images" / f"infer_{image_path.name}"
        cv2.imwrite(str(out_path), annotated)
        print(f"Saved → {out_path}")

    return annotated, detections


def run_video_inference(
    model: YOLO,
    video_path: Path,
    conf: float = 0.4,
    output_name: str | None = None,
) -> Path:
    """Run inference on a video file and save annotated output."""
    ensure_dirs()
    cap = cv2.VideoCapture(str(video_path))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 30
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_name = output_name or f"infer_{video_path.stem}.mp4"
    out_path = OUTPUTS_DIR / "videos" / out_name
    writer = cv2.VideoWriter(
        str(out_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps, (width, height),
    )

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        detections = predict_image(model, frame, conf=conf)
        annotated = draw_detections(frame, detections)

        # FPS overlay
        cv2.putText(annotated, f"Frame {frame_idx}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        writer.write(annotated)
        frame_idx += 1

    cap.release()
    writer.release()
    print(f"Video saved → {out_path}  ({frame_idx} frames)")
    return out_path
