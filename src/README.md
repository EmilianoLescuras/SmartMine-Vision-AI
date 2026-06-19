# src/

Production-quality source code for all SmartMine Vision AI modules.

Code here is modular, typed, PEP8-compliant, and independently testable. Notebooks in `notebooks/` call these modules rather than reimplementing logic.

---

## Structure

```
src/
├── ppe_detection/      ← YOLOv8 PPE detector (current module)
├── vehicle_detection/  ← YOLOv8 vehicle detector (Phase 2)
├── tracking/           ← ByteTrack multi-object tracker (Phase 3)
├── proximity/          ← Proximity alert engine (Phase 4)
├── database/           ← SQLAlchemy ORM models and queries (Phase 5)
├── api/                ← FastAPI application and routers (Phase 5)
└── utils/              ← Shared utilities (all phases)
```

---

## Module: `ppe_detection/`

**Status:** In Development (Phase 1)

Planned files:

| File               | Responsibility                                    |
|--------------------|---------------------------------------------------|
| `__init__.py`      | Module exports                                    |
| `detector.py`      | `PPEDetector` class — load model, run inference   |
| `config.py`        | Detection thresholds, class names, paths          |
| `postprocess.py`   | NMS, confidence filtering, result formatting      |

---

## Module: `vehicle_detection/`

**Status:** Planned (Phase 2)

Will mirror `ppe_detection/` structure with vehicle-specific config and classes.

---

## Module: `tracking/`

**Status:** Planned (Phase 3)

Will wrap ByteTrack with:
- `TrackerManager` — per-frame update and ID assignment
- Integration adapters for detection outputs

---

## Module: `proximity/`

**Status:** Planned (Phase 4)

Will include:
- `ProximityEngine` — compute distances between person and vehicle bounding boxes
- Zone definitions (warning, critical)
- Alert payload construction

---

## Module: `database/`

**Status:** Planned (Phase 5)

Will include:
- SQLAlchemy `Base` and ORM models
- `DetectionEvent`, `Alert`, `VideoSession` tables
- CRUD utilities

---

## Module: `api/`

**Status:** Planned (Phase 5)

Will include:
- FastAPI `app` factory
- Routers: `/detections`, `/alerts`, `/sessions`
- Pydantic schemas
- Authentication middleware

---

## Module: `utils/`

**Status:** Active — grows as needed

Planned files:

| File               | Responsibility                                  |
|--------------------|-------------------------------------------------|
| `data_utils.py`    | Dataset splitting, label validation             |
| `video_utils.py`   | Frame reading, video writing helpers            |
| `draw_utils.py`    | Bounding box and label drawing on frames        |
| `logger.py`        | Loguru-based structured logger                  |
| `config_loader.py` | Load and validate YAML configs                  |

---

## Coding Standards

- Python 3.12, PEP8 enforced.
- Type hints on all function signatures.
- Dataclasses for structured data (detection results, configs).
- `pathlib.Path` instead of `os.path`.
- Functions ≤ 40 lines.
- No global state; dependency injection preferred.
- Docstrings on public classes and functions (one-line summary only).
