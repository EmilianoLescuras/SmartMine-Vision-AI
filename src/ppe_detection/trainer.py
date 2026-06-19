"""YOLOv8 training wrapper for the PPE detection model."""

from __future__ import annotations

from pathlib import Path

from ultralytics import YOLO

from .utils import CONFIGS_DIR, EXPERIMENTS_DIR, MODELS_DIR, ensure_dirs


def train_ppe_model(
    data_yaml: Path | None = None,
    base_model: str = "yolov8n.pt",
    epochs: int = 100,
    imgsz: int = 640,
    project: str | None = None,
    name: str = "baseline",
    device: str = "0",
) -> Path:
    """
    Fine-tune YOLOv8 on the PPE dataset.

    Returns the path to the best weights file.
    """
    ensure_dirs()

    data_yaml = data_yaml or CONFIGS_DIR / "ppe_dataset.yaml"
    project = project or str(EXPERIMENTS_DIR / "ppe_v1")

    model = YOLO(base_model)
    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=-1,           # auto batch size
        device=device,
        project=project,
        name=name,
        exist_ok=False,
        verbose=True,
    )

    best_weights = Path(results.save_dir) / "weights" / "best.pt"
    dest = MODELS_DIR / f"yolov8n_ppe_{name}.pt"
    if best_weights.exists():
        dest.write_bytes(best_weights.read_bytes())
        print(f"Best weights copied → {dest}")

    return dest


def resume_training(weights_path: Path, additional_epochs: int = 50) -> None:
    """Resume training from a checkpoint."""
    model = YOLO(str(weights_path))
    model.train(resume=True, epochs=additional_epochs)
