# datasets/

Stores all datasets used by SmartMine Vision AI.

Raw data is **never committed to git** (see `.gitignore`). Only README files and `.gitkeep` placeholders are tracked. Large files are managed via cloud storage or DVC.

---

## Structure

```
datasets/
├── raw/
│   ├── ppe/        ← Construction Site Safety Dataset (Kaggle)
│   ├── vehicles/   ← BDD100K, COCO (planned)
│   └── custom/     ← Internal or proprietary captures (planned)
└── processed/      ← Cleaned, split, normalized datasets ready for training
```

---

## Current Datasets

### PPE Detection — `raw/ppe/`
- **Name:** Construction Site Safety Dataset
- **Source:** Kaggle
- **Classes:** `Hardhat`, `Mask`, `NO-Hardhat`, `NO-Mask`, `NO-Safety Vest`, `Person`, `Safety Cone`, `Safety Vest`, `machinery`, `vehicle`
- **Format:** YOLO (images + label `.txt` files)
- **Status:** Downloaded ✅

---

## Planned Datasets

| Dataset    | Module            | Source                        | Status   |
|------------|-------------------|-------------------------------|----------|
| BDD100K    | Vehicle Detection | Berkeley DeepDrive            | Planned  |
| COCO       | Vehicle Detection | Microsoft / cocodataset.org   | Planned  |
| MOT17      | Tracking          | motchallenge.net              | Planned  |
| Custom     | All modules       | Internal mine captures        | Future   |

---

## `processed/`

Will contain:
- Train/val/test splits (80/10/10)
- Normalized annotations
- Augmented subsets
- Data statistics (class distribution CSVs)

Processing scripts will live in `src/utils/data_utils.py`.

---

## Expected Outputs

- `processed/ppe/train/`, `val/`, `test/` — YOLO-formatted splits
- `processed/ppe/stats.csv` — class balance report
- `processed/ppe/data.yaml` — Ultralytics dataset config

---

## Dependencies

- `ultralytics` — dataset format compatibility
- `pandas`, `numpy` — statistics
- `Pillow`, `opencv-python` — image inspection
