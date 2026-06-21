"""PPE Detection module — Stage 1 of SmartMine Vision AI."""

from __future__ import annotations

from .dataset_loader import (
    SplitStats,
    class_distribution_dataframe,
    count_annotations,
    get_split_stats,
    load_dataset_stats,
    stats_to_dataframe,
)
from .inference import (
    Detection,
    load_model,
    predict_image,
    run_image_inference,
    run_video_inference,
)
from .ppe_classifier import (
    ComplianceStatus,
    WorkerCompliance,
    classify_workers,
    compliance_color,
    compliance_summary,
)
from .utils import (
    CLASS_COLORS,
    CLASS_NAMES,
    PERSON_CLASS_IDS,
    PPE_CLASSES,
    VEHICLE_CLASS_IDS,
    ensure_dirs,
)
from .visualization import (
    draw_yolo_boxes,
    plot_class_distribution,
    plot_sample_images,
    plot_split_sizes,
)

__all__ = [
    # Dataset
    "SplitStats",
    "class_distribution_dataframe",
    "count_annotations",
    "get_split_stats",
    "load_dataset_stats",
    "stats_to_dataframe",
    # Inference
    "Detection",
    "load_model",
    "predict_image",
    "run_image_inference",
    "run_video_inference",
    # Compliance
    "ComplianceStatus",
    "WorkerCompliance",
    "classify_workers",
    "compliance_color",
    "compliance_summary",
    # Constants
    "CLASS_COLORS",
    "CLASS_NAMES",
    "PERSON_CLASS_IDS",
    "PPE_CLASSES",
    "VEHICLE_CLASS_IDS",
    "ensure_dirs",
    # Visualization
    "draw_yolo_boxes",
    "plot_class_distribution",
    "plot_sample_images",
    "plot_split_sizes",
]
