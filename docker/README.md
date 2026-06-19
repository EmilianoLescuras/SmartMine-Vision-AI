# docker/

Dockerfiles and Docker Compose configurations for containerized deployment of SmartMine Vision AI.

---

## Planned Structure

```
docker/
├── Dockerfile.inference       ← CV inference service (YOLOv8 + OpenCV)
├── Dockerfile.api             ← FastAPI backend service
├── docker-compose.yml         ← Multi-service local deployment
├── docker-compose.prod.yml    ← Production overrides (GPU, volumes)
└── .env.example               ← Environment variable template
```

---

## Services (Planned)

| Service       | Image Base              | Purpose                              |
|---------------|-------------------------|--------------------------------------|
| `inference`   | `ultralytics/ultralytics` | Run CV pipeline on video streams   |
| `api`         | `python:3.12-slim`      | FastAPI REST backend                 |
| `db`          | `postgres:15-alpine`    | PostgreSQL database                  |
| `pgadmin`     | `dpage/pgadmin4`        | DB admin UI (dev only)               |

---

## `docker-compose.yml` — Local Dev (Planned)

```yaml
# Preview — not yet implemented
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: smartmine
      POSTGRES_USER: smartmine
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data

  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://smartmine:${DB_PASSWORD}@db:5432/smartmine

  inference:
    build:
      context: .
      dockerfile: docker/Dockerfile.inference
    depends_on:
      - api
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

volumes:
  pg_data:
```

---

## GPU Support

The inference container uses NVIDIA Container Toolkit for GPU access. Production deployment requires:
- Docker Engine 24+
- NVIDIA Container Toolkit
- CUDA 11.8+ drivers on the host

---

## Cloud Deployment (Future — Phase 6)

| Target          | Strategy                                    |
|-----------------|---------------------------------------------|
| AWS             | ECS Fargate + RDS PostgreSQL + S3 for models|
| Azure           | ACI + Azure Database for PostgreSQL + Blob  |
| CI/CD           | GitHub Actions → Docker Hub → ECS/ACI       |

---

## Dependencies

- Docker Engine 24+
- Docker Compose v2
- NVIDIA Container Toolkit (GPU hosts)
