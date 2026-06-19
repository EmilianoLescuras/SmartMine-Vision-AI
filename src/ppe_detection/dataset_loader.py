"""Dataset inspection and statistics for the PPE Detection module."""

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .utils import (
    CLASS_NAMES,
    TRAIN_IMAGES, TRAIN_LABELS,
    VALID_IMAGES, VALID_LABELS,
    TEST_IMAGES,  TEST_LABELS,
)


@dataclass
class SplitStats:
    name: str
    n_images: int
    n_labels: int
    n_annotations: int
    class_counts: dict[int, int] = field(default_factory=dict)


def count_annotations(labels_dir: Path) -> tuple[int, dict[int, int]]:
    """Return total annotation count and per-class counts for a labels directory."""
    class_counts: dict[int, int] = {}
    total = 0
    for txt in labels_dir.glob("*.txt"):
        for line in txt.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            cls_id = int(line.split()[0])
            class_counts[cls_id] = class_counts.get(cls_id, 0) + 1
            total += 1
    return total, class_counts


def get_split_stats(name: str, images_dir: Path, labels_dir: Path) -> SplitStats:
    """Compute statistics for a single dataset split."""
    n_images = len(list(images_dir.glob("*.jpg"))) + len(list(images_dir.glob("*.png")))
    n_labels = len(list(labels_dir.glob("*.txt")))
    total_ann, class_counts = count_annotations(labels_dir)
    return SplitStats(name, n_images, n_labels, total_ann, class_counts)


def load_dataset_stats() -> list[SplitStats]:
    """Load statistics for all three splits."""
    splits = [
        ("train", TRAIN_IMAGES, TRAIN_LABELS),
        ("valid", VALID_IMAGES, VALID_LABELS),
        ("test",  TEST_IMAGES,  TEST_LABELS),
    ]
    return [get_split_stats(name, img, lbl) for name, img, lbl in splits]


def stats_to_dataframe(stats: list[SplitStats]) -> pd.DataFrame:
    """Convert split stats to a summary DataFrame."""
    rows = []
    for s in stats:
        rows.append({
            "split":       s.name,
            "images":      s.n_images,
            "labels":      s.n_labels,
            "annotations": s.n_annotations,
        })
    return pd.DataFrame(rows).set_index("split")


def class_distribution_dataframe(stats: list[SplitStats]) -> pd.DataFrame:
    """Return per-class annotation counts across all splits as a DataFrame."""
    combined: dict[int, dict[str, int]] = {}
    for s in stats:
        for cls_id, count in s.class_counts.items():
            if cls_id not in combined:
                combined[cls_id] = {}
            combined[cls_id][s.name] = count

    rows = []
    for cls_id in sorted(combined):
        row = {"class_id": cls_id, "class_name": CLASS_NAMES.get(cls_id, str(cls_id))}
        row.update(combined[cls_id])
        rows.append(row)

    df = pd.DataFrame(rows).fillna(0).astype(
        {c: int for c in ["train", "valid", "test"] if c in pd.DataFrame(rows).columns}
    )
    df["total"] = df[["train", "valid", "test"]].sum(axis=1)
    return df.set_index("class_id")
