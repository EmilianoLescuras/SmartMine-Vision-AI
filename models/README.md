# models/

Stores trained model weights and checkpoints.

Model files (`.pt`, `.pth`, `.onnx`, `.engine`) are **excluded from git** due to file size. Store them in cloud storage (S3, Azure Blob, Google Drive) or use DVC for versioning.

---

## Structure

```
models/
├── ppe/        ← PPE detection weights (Phase 1)
├── vehicles/   ← Vehicle detection weights (Phase 2)
└── tracking/   ← Tracking model assets (Phase 3, if applicable)
```

---

## `ppe/`

Expected files after Phase 1 training:

| File                          | Description                                      |
|-------------------------------|--------------------------------------------------|
| `yolov8n_ppe_v1.pt`           | YOLOv8n fine-tuned on PPE dataset (baseline)     |
| `yolov8s_ppe_v1.pt`           | YOLOv8s variant (higher accuracy)                |
| `yolov8n_ppe_v1.onnx`         | ONNX export for deployment                       |
| `training_config.yaml`        | Config used to produce this model                |
| `metrics.json`                | mAP50, mAP50-95, precision, recall at export     |

Naming convention: `{architecture}_{task}_{version}.{ext}`

---

## `vehicles/`

Planned (Phase 2):

- `yolov8n_vehicles_v1.pt`
- `yolov8s_vehicles_v1.pt`

---

## `tracking/`

Planned (Phase 3):

- ByteTrack requires no separate model weights by default (uses Kalman filter).
- This folder will hold Re-ID model weights if person re-identification is added.

---

## Model Registry Strategy (Future)

In production, models will be versioned and tracked using:
- **MLflow Model Registry** — experiment tracking and model promotion
- **Cloud storage** — S3 or Azure Blob for weight storage
- **Docker images** — models baked into inference containers for deployment

---

## Loading Convention

```python
from ultralytics import YOLO

model = YOLO("models/ppe/yolov8n_ppe_v1.pt")
results = model.predict(source="path/to/image.jpg")
```
