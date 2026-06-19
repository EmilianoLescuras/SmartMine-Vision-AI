# outputs/

Stores artifacts produced by inference pipelines and evaluation runs.

Output files (images, videos, large logs) are **excluded from git**. Only `.gitkeep` placeholders and this README are tracked.

---

## Structure

```
outputs/
├── images/   ← Annotated frames from image inference
├── videos/   ← Annotated video outputs from video inference
└── logs/     ← Structured inference and event logs
```

---

## `images/`

Contains annotated inference results saved as JPEG/PNG files.

Naming convention: `{source_name}_{timestamp}_{frame_id}.jpg`

Example: `site_cam01_20260619_143022_frame_042.jpg`

---

## `videos/`

Contains annotated video outputs from the inference pipeline.

Naming convention: `{source_name}_{timestamp}_{model_version}.mp4`

Example: `site_cam01_20260619_yolov8n_ppe_v1.mp4`

---

## `logs/`

Contains structured logs in JSON Lines format (`.jsonl`) for downstream consumption.

Planned log types:

| File                   | Content                                        |
|------------------------|------------------------------------------------|
| `detections.jsonl`     | Per-frame detection records                    |
| `alerts.jsonl`         | Proximity and PPE violation alerts             |
| `session.jsonl`        | Video session metadata (FPS, duration, source) |

Each log entry includes: `timestamp`, `session_id`, `frame_id`, `class`, `confidence`, `bbox`.

---

## Expected Outputs by Phase

| Phase | Output                                          |
|-------|-------------------------------------------------|
| 1     | Annotated PPE detection images and videos       |
| 2     | Annotated vehicle detection videos              |
| 3     | Tracked object videos with ID overlays          |
| 4     | Alert videos with proximity zones highlighted   |
| 5     | Logs consumed by PostgreSQL and Power BI        |

---

## Cleanup Policy

- Outputs older than 30 days are archived or deleted in production.
- In development, manually prune `outputs/` to save disk space.
