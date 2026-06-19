# notebooks/

Jupyter notebooks for exploratory analysis, experimentation, and prototyping. Each subfolder maps to one platform module.

Notebooks are created **progressively** — a new notebook is only added when that module's development begins.

---

## Structure

```
notebooks/
├── 01_ppe_detection/       ← Current module
├── 02_vehicle_detection/   ← Planned
├── 03_tracking/            ← Planned
├── 04_proximity_alerts/    ← Planned
├── 05_database/            ← Planned
└── 06_api/                 ← Planned
```

---

## Module 01 — PPE Detection (`01_ppe_detection/`)

Planned notebooks:

| Notebook                        | Purpose                                              |
|---------------------------------|------------------------------------------------------|
| `01_dataset_exploration.ipynb`  | Class distribution, image stats, sample visualization |
| `02_data_cleaning.ipynb`        | Remove corrupt files, fix labels, balance classes    |
| `03_training_yolo.ipynb`        | YOLOv8 fine-tuning with Ultralytics                  |
| `04_evaluation.ipynb`           | mAP, precision, recall, confusion matrix             |
| `05_video_inference.ipynb`      | Run model on video, visualize detections             |

---

## Module 02 — Vehicle Detection (`02_vehicle_detection/`)

Planned notebooks (Phase 2):

| Notebook                        | Purpose                                         |
|---------------------------------|-------------------------------------------------|
| `01_bdd100k_exploration.ipynb`  | BDD100K dataset analysis                        |
| `02_training_vehicles.ipynb`    | YOLOv8 vehicle model fine-tuning                |
| `03_evaluation.ipynb`           | Vehicle detection metrics                       |
| `04_video_inference.ipynb`      | Vehicle detection on video streams              |

---

## Module 03 — Tracking (`03_tracking/`)

Planned (Phase 3):

- ByteTrack integration
- Track visualization (ID persistence across frames)
- Re-identification analysis

---

## Module 04 — Proximity Alerts (`04_proximity_alerts/`)

Planned (Phase 4):

- Distance estimation methods
- Zone definition and alert logic
- Alert severity classification

---

## Module 05 — Database (`05_database/`)

Planned (Phase 5):

- Schema exploration
- ORM query testing
- Event data analysis

---

## Module 06 — API (`06_api/`)

Planned (Phase 5):

- FastAPI endpoint testing
- Payload design
- Authentication flow

---

## Conventions

- Notebooks are numbered and named clearly.
- Each notebook begins with a markdown cell explaining its purpose.
- Heavy computation is extracted to `src/` modules; notebooks call those functions.
- Output cells are cleared before committing.
