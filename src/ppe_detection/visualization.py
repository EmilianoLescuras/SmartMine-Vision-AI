"""Plotting utilities for dataset exploration and inference results."""

from pathlib import Path
import random

import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from .utils import CLASS_COLORS, CLASS_NAMES


def plot_class_distribution(df: pd.DataFrame, save_path: Path | None = None) -> None:
    """Bar chart of annotation counts per class across splits."""
    splits = [c for c in ["train", "valid", "test"] if c in df.columns]
    x = range(len(df))
    width = 0.25

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, split in enumerate(splits):
        ax.bar([xi + i * width for xi in x], df[split], width, label=split)

    ax.set_xticks([xi + width for xi in x])
    ax.set_xticklabels(df["class_name"], rotation=35, ha="right", fontsize=10)
    ax.set_ylabel("Annotations")
    ax.set_title("Class Distribution Across Splits")
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved → {save_path}")
    plt.show()


def plot_split_sizes(summary_df: pd.DataFrame, save_path: Path | None = None) -> None:
    """Horizontal bar chart of image counts per split."""
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = ["#4CAF50", "#2196F3", "#FF9800"]
    summary_df["images"].plot(kind="barh", ax=ax, color=colors)
    ax.set_xlabel("Number of Images")
    ax.set_title("Dataset Split Sizes")
    for i, v in enumerate(summary_df["images"]):
        ax.text(v + 10, i, str(v), va="center")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved → {save_path}")
    plt.show()


def draw_yolo_boxes(
    image: np.ndarray,
    label_path: Path,
    class_names: dict[int, str] = CLASS_NAMES,
    colors: dict[int, tuple] = CLASS_COLORS,
) -> np.ndarray:
    """Draw YOLO bounding boxes on an image (returns annotated copy)."""
    h, w = image.shape[:2]
    canvas = image.copy()

    if not label_path.exists():
        return canvas

    for line in label_path.read_text().splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        cls_id = int(parts[0])
        cx, cy, bw, bh = map(float, parts[1:5])
        x1 = int((cx - bw / 2) * w)
        y1 = int((cy - bh / 2) * h)
        x2 = int((cx + bw / 2) * w)
        y2 = int((cy + bh / 2) * h)

        color = colors.get(cls_id, (200, 200, 200))
        label = class_names.get(cls_id, str(cls_id))
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
        cv2.putText(canvas, label, (x1, max(y1 - 5, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return canvas


def plot_sample_images(
    images_dir: Path,
    labels_dir: Path,
    n: int = 6,
    save_path: Path | None = None,
    seed: int = 42,
) -> None:
    """Display n random images from a split with ground-truth boxes."""
    random.seed(seed)
    all_images = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
    samples = random.sample(all_images, min(n, len(all_images)))

    cols = 3
    rows = (len(samples) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = np.array(axes).flatten()

    for ax, img_path in zip(axes, samples):
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lbl_path = labels_dir / (img_path.stem + ".txt")
        annotated = draw_yolo_boxes(
            cv2.cvtColor(img, cv2.COLOR_RGB2BGR), lbl_path
        )
        ax.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        ax.set_title(img_path.name[:40], fontsize=8)
        ax.axis("off")

    for ax in axes[len(samples):]:
        ax.axis("off")

    plt.suptitle("Sample Images with Ground-Truth Annotations", fontsize=13)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved → {save_path}")
    plt.show()
