# src/ppe_detection/

**Stage 1 — PPE Detection Module**  
SmartMine Vision AI · Production Computer Vision System

---

## Purpose

Detect Personal Protective Equipment (PPE) in construction and mining site images/videos, and classify each worker as **SAFE** or **UNSAFE** based on detected PPE compliance.

---

## Dataset

| Property | Value |
|----------|-------|
| Name | Construction Site Safety Dataset |
| Source | Roboflow / Kaggle |
| License | CC BY 4.0 |
| Total images | 2,801 |
| Split | 2,605 train / 114 val / 82 test |
| Format | YOLOv8 (normalized XYWH) |
| Image size | 640 × 640 px |

---

## Classes

| ID | Class | Role in Stage 1 |
|----|-------|----------------|
| 0 | Hardhat | PPE compliant ✅ |
| 1 | Mask | Detected, not used in compliance |
| 2 | NO-Hardhat | Violation ❌ |
| 3 | NO-Mask | Detected, not used in compliance |
| 4 | NO-Safety Vest | Violation ❌ |
| 5 | Person | Worker anchor 👤 |
| 6 | Safety Cone | Detected, not used in compliance |
| 7 | Safety Vest | PPE compliant ✅ |
| 8 | machinery | Detected, not used in compliance |
| 9 | vehicle | Detected, not used in compliance |

---

## Module Files

| File | Responsibility |
|------|----------------|
| `utils.py` | Constants, paths, class registry, colors |
| `dataset_loader.py` | Dataset statistics and annotation counts |
| `visualization.py` | Plot generation for exploration and inference |
| `trainer.py` | YOLOv8 training wrapper |
| `inference.py` | Image and video inference runner |
| `ppe_classifier.py` | SAFE / UNSAFE logic based on IoU overlap |
| `__init__.py` | Public module exports |

---

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Base model | yolov8n.pt |
| Epochs | 100 |
| Image size | 640 |
| Batch | Auto |
| Optimizer | AdamW (Ultralytics default) |
| Config | `configs/yaml/ppe_dataset.yaml` |
| Output | `experiments/ppe_v1/baseline/` |
| Best weights | `models/ppe/yolov8n_ppe_baseline.pt` |

---

## SAFE / UNSAFE Logic

```
Person detected
    │
    ├── Hardhat overlaps Person? ──── NO → UNSAFE (Missing Hardhat)
    │
    └── Safety Vest overlaps Person? ─ NO → UNSAFE (Missing Safety Vest)
    
    Both present → SAFE
```

Overlap is determined by IoU ≥ 0.05 between the Person bounding box and each PPE box.  
Explicit violation classes (`NO-Hardhat`, `NO-Safety Vest`) override the positive detections.

---

## Usage

```python
from src.ppe_detection import load_model, predict_image, classify_workers

model = load_model("models/ppe/yolov8n_ppe_baseline.pt")
detections = predict_image(model, frame, conf=0.4)
workers = classify_workers(detections)

for w in workers:
    print(w.status.value, w.violations)
```

---

## Current Metrics

> Fill after running `04_evaluation.ipynb`

| Metric | Value |
|--------|-------|
| Precision | — |
| Recall | — |
| mAP50 | — |
| mAP50-95 | — |

---

## Current Limitations

- SAFE/UNSAFE classification uses spatial IoU, which can fail at very small scales or heavy occlusion.
- No temporal smoothing — per-frame classification may flicker on video.
- Model trained on a single public dataset — may need fine-tuning on actual mine site data.
- No tracking integration — worker IDs reset between frames.

---

## Future Improvements (Stage 3+)

- Integrate ByteTrack to maintain worker IDs across frames.
- Add temporal smoothing to compliance status.
- Fine-tune on mine-specific imagery.
- Export to ONNX / TensorRT for edge deployment.

---

## Roadmap

- [x] Repository architecture
- [x] Dataset exploration (`01_dataset_exploration.ipynb`)
- [x] Dataset validation (`02_dataset_validation.ipynb`)
- [ ] YOLOv8 training (`03_training_yolo.ipynb`)
- [ ] Model evaluation (`04_evaluation.ipynb`)
- [ ] Image inference (`05_image_inference.ipynb`)
- [ ] Video inference (`06_video_inference.ipynb`)
