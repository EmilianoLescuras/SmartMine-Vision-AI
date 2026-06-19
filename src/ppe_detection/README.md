# src/ppe_detection/

PPE detection module — the first production module of SmartMine Vision AI.

Uses a fine-tuned YOLOv8 model to detect Personal Protective Equipment on construction and mining sites.

---

## Planned Files

| File             | Responsibility                                             |
|------------------|------------------------------------------------------------|
| `__init__.py`    | Public exports: `PPEDetector`, `DetectionResult`           |
| `detector.py`    | `PPEDetector` class — load model, run inference per frame  |
| `config.py`      | Class names, confidence thresholds, path constants         |
| `postprocess.py` | Filter, format, and validate raw YOLO results              |

---

## Classes Detected

From the Construction Site Safety Dataset:

- `Hardhat`
- `Mask`
- `NO-Hardhat` ← violation
- `NO-Mask` ← violation
- `NO-Safety Vest` ← violation
- `Person`
- `Safety Cone`
- `Safety Vest`
- `machinery`
- `vehicle`

---

## Interface (Planned)

```python
from src.ppe_detection import PPEDetector

detector = PPEDetector(model_path="models/ppe/yolov8n_ppe_v1.pt", conf=0.5)
results = detector.predict(frame)  # frame: np.ndarray (H, W, 3)
# results: list[DetectionResult]
```

`DetectionResult` will be a dataclass with: `class_name`, `confidence`, `bbox`, `is_violation`.

---

## Development Status

- [ ] `config.py` — class names and thresholds
- [ ] `detector.py` — `PPEDetector` class
- [ ] `postprocess.py` — result formatting
- [ ] Unit tests in `tests/test_ppe_detection.py`

Will be implemented after notebook exploration in `notebooks/01_ppe_detection/`.
