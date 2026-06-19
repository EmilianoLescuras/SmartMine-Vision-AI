# configs/

Stores all configuration files for training, inference, and deployment.

Separating config from code allows experiments to be reproduced by sharing a YAML file rather than modifying source code.

---

## Structure

```
configs/
├── yaml/       ← Inference and dataset configs
└── training/   ← Training hyperparameter configs
```

---

## `yaml/` — Inference & Dataset Configs

Planned files:

| File                    | Purpose                                              |
|-------------------------|------------------------------------------------------|
| `ppe_dataset.yaml`      | Ultralytics dataset config (paths, classes, nc)      |
| `ppe_inference.yaml`    | Inference thresholds, IOU, confidence, device        |
| `vehicles_dataset.yaml` | Vehicle dataset config (Phase 2)                     |
| `tracking.yaml`         | ByteTrack parameters (Phase 3)                       |
| `proximity.yaml`        | Distance thresholds, alert zones (Phase 4)           |

### `ppe_dataset.yaml` example structure

```yaml
path: datasets/processed/ppe
train: train/images
val: val/images
test: test/images

nc: 10
names:
  - Hardhat
  - Mask
  - NO-Hardhat
  - NO-Mask
  - NO-Safety Vest
  - Person
  - Safety Cone
  - Safety Vest
  - machinery
  - vehicle
```

---

## `training/` — Training Hyperparameter Configs

Planned files:

| File                      | Purpose                                          |
|---------------------------|--------------------------------------------------|
| `ppe_baseline.yaml`       | YOLOv8n baseline training run                    |
| `ppe_optimized.yaml`      | Tuned hyperparameters after baseline evaluation  |
| `vehicles_baseline.yaml`  | Vehicle detection training (Phase 2)             |

### Training config example structure

```yaml
model: yolov8n.pt
data: configs/yaml/ppe_dataset.yaml
epochs: 50
imgsz: 640
batch: 16
lr0: 0.01
momentum: 0.937
weight_decay: 0.0005
device: 0        # GPU index; 'cpu' for CPU
project: experiments/ppe_v1
name: baseline
```

---

## Config Loading

All configs are loaded via `src/utils/config_loader.py` using PyYAML. This ensures type validation and consistent path resolution via `pathlib`.
