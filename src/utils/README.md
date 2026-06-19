# src/utils/

Shared utilities used across all SmartMine Vision AI modules.

---

## Planned Files

| File               | Purpose                                                       |
|--------------------|---------------------------------------------------------------|
| `__init__.py`      | Utility exports                                               |
| `logger.py`        | Loguru-based structured logger with file rotation             |
| `config_loader.py` | Load and validate YAML configs via `pathlib`                  |
| `data_utils.py`    | Dataset splitting, label validation, class balance stats      |
| `video_utils.py`   | Frame reading, video writing, FPS calculation                 |
| `draw_utils.py`    | Draw bounding boxes, labels, and zones on frames              |

---

## `logger.py`

Will provide a pre-configured `loguru` logger:
- Console output with color
- JSON file sink for structured machine-readable logs
- Log rotation at 100 MB

---

## `config_loader.py`

Will provide:

```python
def load_config(path: str | Path) -> dict:
    """Load a YAML config file and return as a dict."""
```

---

## `draw_utils.py`

Will provide:

```python
def draw_detections(frame: np.ndarray, results: list[DetectionResult]) -> np.ndarray:
    """Draw bounding boxes and class labels on a frame."""
```

Class-to-color mapping will be consistent across all modules (PPE, vehicles, tracking).

---

## Conventions

- All functions accept and return `pathlib.Path` for file paths.
- No global state.
- Type hints on all signatures.
- Functions under 40 lines.
