# src/ppe_detection/

**Stage 1 — PPE Detection & Mining Asset Module**
SmartMine Vision AI · Production Computer Vision System

---

## Purpose

Detect Personal Protective Equipment (PPE), mining personnel, mining
machinery, and environmental hazards in surface-mine imagery.
For every detected worker, classify compliance as **SAFE**, **UNSAFE**
or **UNKNOWN** based on the PPE attributes carried by their bounding box.

The module powers Stage 1 of the SmartMine pipeline and feeds the
downstream tracking, proximity-alert, and reporting stages.

---

## Dataset — Unified `smartmine_v1`

The training corpus merges four public YOLOv8 datasets into one
32-class schema. The merge script and class map live in
`scripts/merge_datasets.py`; the canonical YAML is
`configs/yaml/smartmine_unified.yaml`.

| Source | Origin | Contribution |
|--------|--------|--------------|
| `css_ppe`              | Roboflow / Kaggle — Construction Site Safety | Generic PPE (hardhat, vest, mask) + person |
| `riskalert`            | Roboflow Universe — `personal-q02wc/riskalert-mining` | Mining-specific personnel + machinery |
| `deteccion_escenarios` | Roboflow Universe — mining scene detection | Casco color variants, vehicle states |
| `mining_area`          | Roboflow Universe — mining area vehicle entry | Heavy vehicle in zone |

| Property | Value |
|----------|-------|
| Format | YOLOv8 (normalized cx cy w h) |
| Image size | 640 × 640 px (standardised on merge) |
| Total images | ~5 785 (train + valid + test) |
| Total annotations | ~40 085 |
| Classes | 32 |

---

## Unified Class Schema (32 classes)

| ID | Class | Group | Source signal |
|----|-------|-------|---------------|
| 0  | person | Persona genérica | CSS Person, riskalert PERSONA |
| 1  | person_con_casco | PPE compliant | embedded |
| 2  | person_sin_casco | PPE violation | embedded |
| 3  | person_con_chaleco | PPE compliant | embedded (currently empty — see Known Gaps) |
| 4  | person_sin_chaleco | PPE violation | embedded |
| 5  | person_con_guantes | PPE compliant | embedded |
| 6  | person_sin_guantes | PPE violation | embedded |
| 7  | person_con_lentes | PPE compliant | embedded |
| 8  | person_sin_lentes | PPE violation | embedded |
| 9  | person_con_respirador | PPE compliant | embedded |
| 10 | person_sin_respirador | PPE violation | embedded |
| 11 | person_ropa_reflectiva | PPE compliant | embedded |
| 12 | person_sin_ropa_reflectiva | PPE violation | embedded |
| 13 | mask | Separate PPE object | CSS Mask |
| 14 | camioneta | Vehículo liviano | riskalert / escenarios |
| 15 | minibus | Vehículo liviano | riskalert / escenarios |
| 16 | volquete | Maquinaria pesada | riskalert / escenarios |
| 17 | camion | Vehículo pesado (genérico) | CSS vehicle / mining_area |
| 18 | excavadora | Maquinaria pesada | riskalert / escenarios |
| 19 | retro_excavadora | Maquinaria pesada | riskalert / escenarios |
| 20 | cargador_frontal | Maquinaria pesada | riskalert / escenarios |
| 21 | motoniveladora | Maquinaria pesada | riskalert / escenarios |
| 22 | tractor | Maquinaria pesada | riskalert / escenarios |
| 23 | rodillo | Maquinaria pesada | riskalert / escenarios |
| 24 | cisterna_agua | Maquinaria pesada | riskalert / escenarios |
| 25 | safety_cone | Señalética | todas |
| 26 | senalizacion | Señalética | riskalert / escenarios |
| 27 | hardhat | Separate PPE object | CSS Hardhat |
| 28 | safety_vest | Separate PPE object | CSS Safety Vest |
| 29 | animal | Hazard | riskalert / escenarios |
| 30 | polvo | Hazard | riskalert / escenarios |
| 31 | machinery | Maquinaria genérica (legacy) | CSS machinery |

---

## Module Files

| File | Responsibility |
|------|----------------|
| `utils.py`           | Project paths, 32-class registry, color palette, group sets |
| `dataset_loader.py`  | Split statistics, annotation counts, distribution dataframes |
| `visualization.py`   | Matplotlib / OpenCV plotting for exploration and inference |
| `trainer.py`         | YOLOv8 training wrapper (defaults to `smartmine_unified.yaml`) |
| `inference.py`       | Image + video inference, structured `Detection` dataclass |
| `ppe_classifier.py`  | SAFE / UNSAFE / UNKNOWN logic with hybrid attribute resolution |
| `__init__.py`        | Public API surface |

---

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Base model | `yolov8n.pt` (downloaded by ultralytics at first run) |
| Epochs | 100 (configurable) |
| Image size | 640 |
| Batch | Auto (`batch=-1`) |
| Device | `mps` on Apple Silicon, `0` on CUDA |
| Optimizer | AdamW (Ultralytics default) |
| Data config | `configs/yaml/smartmine_unified.yaml` |
| Run dir | `experiments/smartmine_v1/<name>/` |
| Best weights → | `models/ppe/yolov8n_smartmine_<name>.pt` |

---

## Compliance Logic

```
For each worker (any person class 0–12):
    1. Embedded signal:
         person_con_casco → hardhat=True
         person_sin_casco → hardhat=False
         …
    2. Overlap signal (only fills attributes still unknown):
         hardhat(27) / safety_vest(28) / mask(13) overlapping
         the person box mark hardhat / vest / mask = True.
         Overlap = IoU ≥ 0.05 OR item center inside person box.
    3. Resolution:
         any required attr == False  →  UNSAFE   (red)
         any required attr is None   →  UNKNOWN  (amber)
         all required attrs True     →  SAFE     (green)
       Required = {hardhat, vest}. Other attrs reported, never fatal.
```

The embedded signal always takes precedence; separate-detection
inference only fills the gaps it leaves behind.

---

## Usage

```python
from src.ppe_detection import (
    load_model, predict_image,
    classify_workers, compliance_color, compliance_summary,
)

model = load_model("models/ppe/yolov8n_smartmine_baseline.pt")
detections = predict_image(model, frame, conf=0.4)
workers = classify_workers(detections)

print(compliance_summary(workers))
# → {"SAFE": 3, "UNSAFE": 1, "UNKNOWN": 0}

for w in workers:
    print(w.status.value, w.violations, w.attributes)
```

---

## Known Gaps & Limitations

- **Class 3 (`person_con_chaleco`) empty** — none of the four sources
  uses an explicit "con chaleco" label. Compliance is derived from
  separate `safety_vest` (28) detections overlapping a generic person.
- **No boots / mining suit data** — `botas` and `traje minero` are
  required by typical mining safety standards but not labelled in any
  source dataset. Acquiring a labelled corpus is on the Stage 1+ roadmap.
- **Source class imbalance** — heavy-machinery classes have 10× fewer
  instances than person classes; consider class-weighted sampling.
- Compliance uses spatial IoU + center containment — robust for typical
  shots, can mis-fire on heavy occlusion or distant micro-detections.
- No temporal smoothing — per-frame classification may flicker on video.
  Tracking (Stage 3) will provide stable IDs and majority-vote smoothing.

---

## Roadmap

- [x] Repository architecture
- [x] Dataset merge into unified `smartmine_v1` (32 classes)
- [x] Module 1 refactor (utils, classifier, trainer, inference)
- [x] Dataset exploration (`01_dataset_exploration.ipynb`)
- [x] Dataset validation (`02_dataset_validation.ipynb`)
- [ ] YOLOv8 training (`03_training_yolo.ipynb`) — runs end-to-end
- [ ] Model evaluation (`04_evaluation.ipynb`) — per-class metrics
- [ ] Image inference (`05_image_inference.ipynb`)
- [ ] Video inference (`06_video_inference.ipynb`)
- [ ] Acquire boots / mining-suit dataset
- [ ] Move to Stage 2 (proximity & tracking)
