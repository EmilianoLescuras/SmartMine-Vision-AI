"""YOLOv8 training wrapper for the SmartMine unified detection model."""

from __future__ import annotations

from pathlib import Path

import torch
from ultralytics import YOLO

from .utils import CONFIGS_DIR, EXPERIMENTS_DIR, MODELS_DIR, ensure_dirs


def detect_device() -> str:
    """Pick the best available training device.

    Returns 'mps' on Apple Silicon, '0' on CUDA, 'cpu' otherwise.
    Ultralytics accepts these strings directly.
    """
    if torch.cuda.is_available():
        return "0"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def train_ppe_model(
    data_yaml: Path | None = None,
    base_model: str = "yolov8n.pt",
    epochs: int = 100,
    imgsz: int = 640,
    project: str | None = None,
    name: str = "baseline",
    device: str | None = None,
    batch: int | float = -1,
    patience: int = 50,
) -> Path:
    """
    Fine-tune YOLOv8 on the unified SmartMine dataset.

    device=None auto-detects (mps on Apple Silicon, cuda:0 if available,
    cpu otherwise). batch=-1 lets Ultralytics auto-pick the largest batch
    that fits on the chosen device.

    Returns the path to the copied best-weights file under models/ppe/.
    """
    ensure_dirs()

    data_yaml = data_yaml or CONFIGS_DIR / "smartmine_unified.yaml"
    project = project or str(EXPERIMENTS_DIR / "smartmine_v1")
    device = device or detect_device()
    print(f"[trainer] device={device}  data={data_yaml}  epochs={epochs}  imgsz={imgsz}")

    model = YOLO(base_model)
    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        exist_ok=False,
        patience=patience,
        verbose=True,
    )

    best_weights = Path(results.save_dir) / "weights" / "best.pt"
    dest = MODELS_DIR / f"yolov8n_smartmine_{name}.pt"
    if best_weights.exists():
        dest.write_bytes(best_weights.read_bytes())
        print(f"Best weights copied -> {dest}")

    return dest


def resume_training(weights_path: Path, additional_epochs: int = 50) -> None:
    """Resume training from a checkpoint."""
    model = YOLO(str(weights_path))
    model.train(resume=True, epochs=additional_epochs)
