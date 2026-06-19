# database/

SQL schemas, migrations, and seed scripts for the SmartMine Vision AI PostgreSQL database.

---

## Purpose

Persists detection events, proximity alerts, video session metadata, and camera configurations for long-term auditability, reporting, and Power BI consumption.

---

## Planned Structure

```
database/
├── schemas/
│   └── 001_initial_schema.sql     ← Core tables
├── migrations/
│   └── (Alembic auto-generated)   ← Schema evolution
└── seeds/
    └── seed_cameras.sql           ← Initial camera config data
```

---

## Planned Tables

### `video_sessions`
Tracks each inference run on a video source.

| Column        | Type        | Description                     |
|---------------|-------------|---------------------------------|
| `id`          | UUID        | Primary key                     |
| `camera_id`   | VARCHAR     | Camera or file identifier       |
| `started_at`  | TIMESTAMP   | Session start                   |
| `ended_at`    | TIMESTAMP   | Session end                     |
| `fps`         | FLOAT       | Frames per second processed     |
| `model_name`  | VARCHAR     | Model used for inference        |

### `detection_events`
One row per detected object per frame.

| Column         | Type      | Description                        |
|----------------|-----------|------------------------------------|
| `id`           | UUID      | Primary key                        |
| `session_id`   | UUID      | FK → `video_sessions`              |
| `frame_id`     | INT       | Frame number in session            |
| `timestamp`    | TIMESTAMP | Event time                         |
| `class_name`   | VARCHAR   | Detected class (e.g., "Hardhat")   |
| `confidence`   | FLOAT     | Detection confidence               |
| `bbox_x1`      | FLOAT     | Bounding box coordinates           |
| `bbox_y1`      | FLOAT     |                                    |
| `bbox_x2`      | FLOAT     |                                    |
| `bbox_y2`      | FLOAT     |                                    |

### `proximity_alerts`
Records person-vehicle proximity violations.

| Column          | Type      | Description                            |
|-----------------|-----------|----------------------------------------|
| `id`            | UUID      | Primary key                            |
| `session_id`    | UUID      | FK → `video_sessions`                  |
| `frame_id`      | INT       | Frame of violation                     |
| `timestamp`     | TIMESTAMP | Alert time                             |
| `person_bbox`   | JSON      | Person bounding box                    |
| `vehicle_bbox`  | JSON      | Vehicle bounding box                   |
| `distance_px`   | FLOAT     | Pixel distance between boxes           |
| `severity`      | VARCHAR   | `warning` or `critical`                |
| `acknowledged`  | BOOLEAN   | Operator acknowledgment flag           |

---

## Migration Strategy

- Alembic manages all schema changes after initial creation.
- Each migration is numbered and descriptive: `002_add_acknowledged_to_alerts.py`.
- Never modify `001_initial_schema.sql` after deployment — use migrations.

---

## Dependencies

- PostgreSQL 15+
- SQLAlchemy 2.x (ORM, defined in `src/database/`)
- Alembic (migrations)
- psycopg2-binary (driver)
