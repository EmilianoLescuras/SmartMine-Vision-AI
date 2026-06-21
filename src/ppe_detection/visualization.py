"""Plotting utilities for dataset exploration and inference results."""

from __future__ import annotations

from pathlib import Path
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .utils import CLASS_COLORS, CLASS_NAMES


_SPLIT_COLORS = {"train": "#4CAF50", "valid": "#2196F3", "test": "#FF9800"}


def plot_class_distribution(df: pd.DataFrame, save_path: Path | None = None) -> None:
    """Horizontal stacked-style bar chart of annotation counts per class across splits.

    Horizontal layout is required because the unified schema has 32 classes
    and vertical labels stop being readable above ~12 categories.
    """
    splits = [c for c in ["train", "valid", "test"] if c in df.columns]
    if not splits:
        print("No split columns found in dataframe.")
        return

    df_sorted = df.sort_values("total", ascending=True) if "total" in df.columns else df
    y = np.arange(len(df_sorted))
    height = 0.25

    fig_h = max(7, 0.32 * len(df_sorted))
    fig, ax = plt.subplots(figsize=(12, fig_h))

    for i, split in enumerate(splits):
        ax.barh(
            y + (i - 1) * height,
            df_sorted[split],
            height,
            label=split,
            color=_SPLIT_COLORS.get(split),
        )

    ax.set_yticks(y)
    ax.set_yticklabels(df_sorted["class_name"], fontsize=9)
    ax.set_xlabel("Annotations")
    ax.set_title(f"Class Distribution Across Splits ({len(df_sorted)} classes)")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved -> {save_path}")
    plt.show()


def plot_split_sizes(summary_df: pd.DataFrame, save_path: Path | None = None) -> None:
    """Horizontal bar chart of image counts per split."""
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = [_SPLIT_COLORS.get(s, "#888") for s in summary_df.index]
    summary_df["images"].plot(kind="barh", ax=ax, color=colors)
    ax.set_xlabel("Number of Images")
    ax.set_title("Dataset Split Sizes")
    for i, v in enumerate(summary_df["images"]):
        ax.text(v + 10, i, str(int(v)), va="center")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved -> {save_path}")
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
    all_images = (
        list(images_dir.glob("*.jpg"))
        + list(images_dir.glob("*.jpeg"))
        + list(images_dir.glob("*.png"))
    )
    if not all_images:
        print(f"[WARN] No images found in {images_dir}")
        return
    samples = random.sample(all_images, min(n, len(all_images)))

    cols = 3
    rows = (len(samples) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = np.array(axes).flatten()

    for ax, img_path in zip(axes, samples):
        img_bgr = cv2.imread(str(img_path))
        lbl_path = labels_dir / (img_path.stem + ".txt")
        annotated_bgr = draw_yolo_boxes(img_bgr, lbl_path)
        ax.imshow(cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB))
        ax.set_title(img_path.name[:40], fontsize=8)
        ax.axis("off")

    for ax in axes[len(samples):]:
        ax.axis("off")

    plt.suptitle("Sample Images with Ground-Truth Annotations", fontsize=13)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved -> {save_path}")
    plt.show()
