"""PPE Detection module — Stage 1 of SmartMine Vision AI."""

from __future__ import annotations

from .dataset_loader import load_dataset_stats, stats_to_dataframe, class_distribution_dataframe
from .utils import CLASS_NAMES, PPE_CLASSES, ensure_dirs

# NOTE: inference and ppe_classifier are imported lazily to avoid loading
# ultralytics (a heavy dependency) when only dataset utilities are needed.
def _lazy_imports():
    from .inference import Detection, load_model, predict_image, run_image_inference, run_video_inference  # noqa: F401
    from .ppe_classifier import WorkerCompliance, ComplianceStatus, classify_workers  # noqa: F401

__all__ = [
    "load_dataset_stats", "stats_to_dataframe", "class_distribution_dataframe",
    "Detection", "load_model", "predict_image", "run_image_inference", "run_video_inference",
    "WorkerCompliance", "ComplianceStatus", "classify_workers",
    "CLASS_NAMES", "PPE_CLASSES", "ensure_dirs",
]
