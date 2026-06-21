"""Shared constants and path utilities for the SmartMine unified detection module."""

from __future__ import annotations

from pathlib import Path

# ── Project roots ─────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = PROJECT_ROOT / "datasets" / "merged" / "smartmine_v1"

TRAIN_IMAGES = DATASET_ROOT / "train" / "images"
TRAIN_LABELS = DATASET_ROOT / "train" / "labels"
VALID_IMAGES = DATASET_ROOT / "valid" / "images"
VALID_LABELS = DATASET_ROOT / "valid" / "labels"
TEST_IMAGES  = DATASET_ROOT / "test"  / "images"
TEST_LABELS  = DATASET_ROOT / "test"  / "labels"

OUTPUTS_DIR     = PROJECT_ROOT / "outputs"
MODELS_DIR      = PROJECT_ROOT / "models" / "ppe"
CONFIGS_DIR     = PROJECT_ROOT / "configs" / "yaml"
DOCS_DIR        = PROJECT_ROOT / "docs" / "research"
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"

# ── Unified class registry (32 classes) ──────────────────────────────────────
CLASS_NAMES: dict[int, str] = {
    # People — compliance embedded in class
    0:  "person",
    1:  "person_con_casco",
    2:  "person_sin_casco",
    3:  "person_con_chaleco",
    4:  "person_sin_chaleco",
    5:  "person_con_guantes",
    6:  "person_sin_guantes",
    7:  "person_con_lentes",
    8:  "person_sin_lentes",
    9:  "person_con_respirador",
    10: "person_sin_respirador",
    11: "person_ropa_reflectiva",
    12: "person_sin_ropa_reflectiva",
    13: "mask",
    # Vehicles
    14: "camioneta",
    15: "minibus",
    16: "volquete",
    17: "camion",
    18: "excavadora",
    19: "retro_excavadora",
    20: "cargador_frontal",
    21: "motoniveladora",
    22: "tractor",
    23: "rodillo",
    24: "cisterna_agua",
    # Safety & environment
    25: "safety_cone",
    26: "senalizacion",
    27: "hardhat",
    28: "safety_vest",
    29: "animal",
    30: "polvo",
    31: "machinery",
}

# ── Compliance groups ─────────────────────────────────────────────────────────
PPE_CLASSES = {
    # class_id → compliance indicator for that attribute
    "person_generic":  {0},
    "compliant": {
        "hardhat":    {1, 27},   # person_con_casco OR separate hardhat detection
        "vest":       {3, 28},   # person_con_chaleco OR separate safety_vest
        "gloves":     {5},
        "eyewear":    {7},
        "respirator": {9},
        "reflective": {11},
    },
    "violation": {
        "hardhat":    {2},
        "vest":       {4},
        "gloves":     {6},
        "eyewear":    {8},
        "respirator": {10},
        "reflective": {12},
    },
}

# All class IDs that represent a person (used to find workers)
PERSON_CLASS_IDS: set[int] = set(range(13))

VEHICLE_CLASS_IDS: set[int] = {14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24}

# ── Colour palette (BGR for OpenCV) ──────────────────────────────────────────
CLASS_COLORS: dict[int, tuple[int, int, int]] = {
    # People — green = compliant, red = violation, white = generic
    0:  (220, 220, 220),  # person              — light grey
    1:  (0, 220, 0),      # person_con_casco    — green
    2:  (0, 0, 220),      # person_sin_casco    — red
    3:  (0, 200, 80),     # person_con_chaleco  — green-teal
    4:  (0, 60, 220),     # person_sin_chaleco  — dark red
    5:  (0, 180, 120),    # person_con_guantes  — green
    6:  (60, 0, 200),     # person_sin_guantes  — red
    7:  (0, 160, 160),    # person_con_lentes   — teal
    8:  (100, 0, 180),    # person_sin_lentes   — purple-red
    9:  (0, 140, 200),    # person_con_respirador — blue-green
    10: (140, 0, 160),    # person_sin_respirador — magenta-red
    11: (0, 255, 200),    # person_ropa_reflectiva — bright teal
    12: (200, 0, 140),    # person_sin_ropa_reflectiva — pink-red
    13: (0, 200, 255),    # mask                — yellow
    # Vehicles — blue shades
    14: (220, 140, 0),    # camioneta           — sky blue
    15: (200, 120, 0),    # minibus             — blue
    16: (180, 100, 0),    # volquete            — teal-blue
    17: (160, 80, 0),     # camion              — dark blue
    18: (255, 180, 0),    # excavadora          — bright blue
    19: (240, 160, 0),    # retro_excavadora    — cyan-blue
    20: (200, 200, 0),    # cargador_frontal    — blue-purple
    21: (180, 220, 0),    # motoniveladora      — indigo
    22: (160, 200, 0),    # tractor             — dark indigo
    23: (140, 180, 0),    # rodillo             — purple
    24: (120, 160, 0),    # cisterna_agua       — dark purple
    # Safety & environment — orange/yellow tones
    25: (0, 165, 255),    # safety_cone         — orange
    26: (0, 140, 220),    # senalizacion        — dark orange
    27: (0, 200, 255),    # hardhat             — gold
    28: (0, 220, 180),    # safety_vest         — yellow-green
    29: (100, 80, 60),    # animal              — brown
    30: (150, 150, 180),  # polvo               — grey-blue
    31: (128, 0, 128),    # machinery           — purple
}


def ensure_dirs() -> None:
    """Create output directories if they don't exist."""
    for d in [OUTPUTS_DIR / "images", OUTPUTS_DIR / "videos",
              OUTPUTS_DIR / "logs", MODELS_DIR, DOCS_DIR, EXPERIMENTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
