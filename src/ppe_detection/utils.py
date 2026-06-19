"""Shared constants and path utilities for the PPE detection module."""

from pathlib import Path

# ── Project roots ─────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = Path("/Users/nanolescuras/Downloads/SmartMine COMP VISION/css-data")

TRAIN_IMAGES = DATASET_ROOT / "train" / "images"
TRAIN_LABELS = DATASET_ROOT / "train" / "labels"
VALID_IMAGES = DATASET_ROOT / "valid" / "images"
VALID_LABELS = DATASET_ROOT / "valid" / "labels"
TEST_IMAGES  = DATASET_ROOT / "test"  / "images"
TEST_LABELS  = DATASET_ROOT / "test"  / "labels"

OUTPUTS_DIR  = PROJECT_ROOT / "outputs"
MODELS_DIR   = PROJECT_ROOT / "models" / "ppe"
CONFIGS_DIR  = PROJECT_ROOT / "configs" / "yaml"
DOCS_DIR     = PROJECT_ROOT / "docs" / "research"
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"

# ── Class registry ────────────────────────────────────────────────────────────
CLASS_NAMES: dict[int, str] = {
    0: "Hardhat",
    1: "Mask",
    2: "NO-Hardhat",
    3: "NO-Mask",
    4: "NO-Safety Vest",
    5: "Person",
    6: "Safety Cone",
    7: "Safety Vest",
    8: "machinery",
    9: "vehicle",
}

# Classes relevant to PPE compliance logic
PPE_CLASSES = {
    "compliant":   {0: "Hardhat", 7: "Safety Vest"},
    "violation":   {2: "NO-Hardhat", 4: "NO-Safety Vest"},
    "person":      {5: "Person"},
}

# Colour palette for drawing (BGR for OpenCV)
CLASS_COLORS: dict[int, tuple[int, int, int]] = {
    0: (0, 255, 0),      # Hardhat        — green
    1: (0, 200, 255),    # Mask           — yellow-ish
    2: (0, 0, 255),      # NO-Hardhat     — red
    3: (0, 100, 255),    # NO-Mask        — orange
    4: (0, 0, 200),      # NO-Safety Vest — dark red
    5: (255, 255, 255),  # Person         — white
    6: (255, 165, 0),    # Safety Cone    — orange
    7: (0, 255, 128),    # Safety Vest    — mint
    8: (128, 0, 128),    # machinery      — purple
    9: (200, 200, 0),    # vehicle        — dark yellow
}


def ensure_dirs() -> None:
    """Create output directories if they don't exist."""
    for d in [OUTPUTS_DIR / "images", OUTPUTS_DIR / "videos",
              OUTPUTS_DIR / "logs", MODELS_DIR, DOCS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
