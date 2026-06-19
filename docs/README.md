# docs/

Project documentation: architecture decisions, system diagrams, and research notes.

---

## Structure

```
docs/
├── architecture/   ← Architecture Decision Records (ADRs) and design docs
├── diagrams/       ← System diagrams (draw.io, PNG exports)
└── research/       ← Literature notes, model comparisons, dataset analysis
```

---

## `architecture/`

Planned documents:

| File                          | Description                                        |
|-------------------------------|----------------------------------------------------|
| `ADR-001-detection-model.md`  | Why YOLOv8 over alternatives (RT-DETR, YOLOv9)    |
| `ADR-002-tracking.md`         | Why ByteTrack over StrongSORT, DeepSORT            |
| `ADR-003-database.md`         | Why PostgreSQL over InfluxDB or Elasticsearch      |
| `ADR-004-api.md`              | Why FastAPI over Django REST / Flask               |
| `system-design.md`            | End-to-end data flow description                   |

ADR format: **Context → Decision → Consequences**

---

## `diagrams/`

Planned diagrams:

| File                          | Description                                        |
|-------------------------------|----------------------------------------------------|
| `pipeline-overview.png`       | High-level data flow (video → detection → DB)      |
| `database-schema.png`         | ER diagram of PostgreSQL tables                    |
| `api-architecture.png`        | FastAPI service and dependency graph               |
| `deployment-aws.png`          | AWS cloud deployment topology                      |

Diagrams are created in draw.io and exported as PNG. Source `.drawio` files are also committed.

---

## `research/`

Planned notes:

| File                          | Description                                        |
|-------------------------------|----------------------------------------------------|
| `ppe-datasets-survey.md`      | Comparison of PPE datasets (class coverage, size)  |
| `yolo-model-comparison.md`    | YOLOv8n vs YOLOv8s vs YOLOv8m benchmark           |
| `tracking-algorithms.md`      | ByteTrack, StrongSORT, DeepSORT comparison         |
| `proximity-estimation.md`     | Methods for pixel-space distance estimation        |

---

## Documentation Philosophy

- Documents explain **why**, not **what**. Code explains what.
- ADRs are written **before** major implementation decisions.
- Diagrams are updated when the architecture changes.
- Research notes are informal but referenced in ADRs.
