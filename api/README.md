# api/

FastAPI application for the SmartMine Vision AI backend.

Provides REST endpoints to trigger inference, query detection events, retrieve alerts, and manage sessions. This is the integration layer between the CV pipeline and external consumers (Power BI, dashboards, mobile apps).

---

## Planned Structure

```
api/
├── main.py               ← FastAPI app factory and startup
├── routers/
│   ├── detections.py     ← GET /detections endpoints
│   ├── alerts.py         ← GET/PATCH /alerts endpoints
│   └── sessions.py       ← GET /sessions endpoints
├── schemas/
│   ├── detection.py      ← Pydantic request/response models
│   ├── alert.py
│   └── session.py
├── dependencies.py       ← DB session, auth injection
└── auth.py               ← API key / JWT authentication
```

---

## Planned Endpoints

### Sessions
| Method | Path                    | Description                    |
|--------|-------------------------|--------------------------------|
| GET    | `/sessions`             | List all video sessions        |
| GET    | `/sessions/{id}`        | Get session detail             |

### Detections
| Method | Path                           | Description                         |
|--------|--------------------------------|-------------------------------------|
| GET    | `/detections`                  | List detection events (paginated)   |
| GET    | `/detections?session_id={id}`  | Filter by session                   |
| GET    | `/detections?class={name}`     | Filter by class                     |

### Alerts
| Method | Path                    | Description                       |
|--------|-------------------------|-----------------------------------|
| GET    | `/alerts`               | List proximity alerts             |
| GET    | `/alerts?severity=critical` | Filter by severity            |
| PATCH  | `/alerts/{id}/acknowledge` | Mark alert as acknowledged     |

### Inference (Future)
| Method | Path              | Description                              |
|--------|-------------------|------------------------------------------|
| POST   | `/infer/image`    | Run PPE detection on uploaded image      |
| POST   | `/infer/video`    | Submit video for async inference         |

---

## Development Plan (Phase 5)

1. Implement `src/api/` module with FastAPI app.
2. Connect to PostgreSQL via SQLAlchemy session dependency.
3. Add Pydantic schemas for all response models.
4. Add API key authentication header.
5. Write integration tests against a test database.
6. Generate OpenAPI docs (`/docs`) for stakeholder review.

---

## Dependencies

- FastAPI
- Uvicorn
- Pydantic v2
- SQLAlchemy 2.x
- psycopg2-binary
