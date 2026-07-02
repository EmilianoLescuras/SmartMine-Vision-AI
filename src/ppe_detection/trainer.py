"""YOLOv8 training wrapper for the SmartMine unified detection model."""

from __future__ import annotations

from pathlib import Path

import torch
from ultralytics import YOLO

from .utils import EXPERIMENTS_DIR, MODELS_DIR, ensure_dirs, write_dataset_yaml


def detect_device() -> str:
    """Pick the best available device for *inference*.

    Returns 'mps' on Apple Silicon, '0' on CUDA, 'cpu' otherwise.
    Ultralytics accepts these strings directly.
    """
    if torch.cuda.is_available():
        return "0"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def detect_train_device() -> str:
    """Pick the best available device for *training*.

    Unlike inference, training is deliberately kept off Apple's MPS backend:
    YOLO's backward pass crashes on MPS with torch<=2.5
    ("view size is not compatible with input tensor's size and stride"), a
    known PyTorch regression. We therefore use CUDA when present and otherwise
    fall back to CPU (slower but correct). Once a torch release fixes MPS
    autograd, this can return 'mps' again.
    """
    if torch.cuda.is_available():
        return "0"
    return "cpu"


def recommended_train_config(device: str | None = None) -> dict:
    """Device-aware training hyperparameters so the *same* notebook runs well on
    a CPU-only laptop and on a CUDA desktop without manual edits.

    - **CUDA**: full dataset at 640px, AutoBatch (``batch=-1``, GPU-only) and 100
      epochs — aims for the proposal's mAP>0.70 target; early stopping
      (``patience``) cuts it short once converged.
    - **CPU / MPS**: a 20% subset at 416px with a fixed batch so a run finishes
      in ~30 min instead of many hours. (MPS trains on CPU here — see
      ``detect_train_device``.)

    Returns a dict ready to splat into ``train_ppe_model(**cfg)``; override any
    field at the call site.
    """
    device = device or detect_train_device()
    is_cuda = str(device).isdigit() or str(device).startswith("cuda")
    if is_cuda:
        return {"epochs": 100, "imgsz": 640, "batch": -1, "fraction": 1.0}
    return {"epochs": 10, "imgsz": 416, "batch": 16, "fraction": 0.20}


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
    fraction: float = 1.0,
) -> Path:
    """
    Fine-tune YOLOv8 on the unified SmartMine dataset.

    device=None auto-detects (cuda:0 if available, else cpu — MPS is skipped
    for training, see detect_train_device). batch=-1 lets Ultralytics auto-pick
    the largest batch on CUDA; on CPU it falls back to a fixed batch.

    Returns the path to the copied best-weights file under models/ppe/.
    """
    ensure_dirs()

    data_yaml = data_yaml or write_dataset_yaml()
    project = project or str(EXPERIMENTS_DIR / "smartmine_v1")
    device = device or detect_train_device()
    print(f"[trainer] device={device}  data={data_yaml}  epochs={epochs}  "
          f"imgsz={imgsz}  fraction={fraction}")

    def _run(dev: str):
        model = YOLO(base_model)
        return model.train(
            data=str(data_yaml),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=dev,
            project=project,
            name=name,
            exist_ok=True,
            patience=patience,
            fraction=fraction,
            verbose=True,
        )

    try:
        results = _run(device)
    except RuntimeError as e:
        # Known MPS autograd bug — degrade to CPU instead of crashing the run.
        if device != "cpu" and "view size is not compatible" in str(e):
            print(f"[trainer] device={device} backward failed (known MPS/torch "
                  f"bug); retrying on CPU…")
            device = "cpu"
            results = _run(device)
        else:
            raise

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
