# SmartMine Vision AI

**Intelligent Safety Monitoring Platform for Mining and Industry 4.0 using Computer Vision and Analytics**

---

## Overview

SmartMine Vision AI is a production-grade, modular computer vision platform designed to enhance safety and operational efficiency in mining and industrial environments. It leverages state-of-the-art object detection, multi-object tracking, and real-time analytics to detect safety violations, monitor vehicle-person proximity, and generate actionable alerts.

---

## Objectives

- Detect PPE compliance (helmets, vests, persons) in real-time video streams.
- Detect and classify vehicles (trucks, cars) operating in restricted zones.
- Track multiple objects across frames using ByteTrack.
- Generate proximity alerts when persons are too close to moving vehicles.
- Persist events to a PostgreSQL database for audit and analytics.
- Expose a FastAPI REST backend for integration and dashboarding.
- Visualize KPIs and safety trends in Power BI.
- Deploy via Docker containers, targeting AWS/Azure cloud infrastructure.

---

## Architecture

```
Video Source (RTSP / File)
        │
        ▼
┌─────────────────────┐
│   PPE Detection     │  ← YOLOv8, Construction Site Safety Dataset
└────────┬────────────┘
         │
┌────────▼────────────┐
│  Vehicle Detection  │  ← YOLOv8, BDD100K / COCO
└────────┬────────────┘
         │
┌────────▼────────────┐
│  Multi-Object       │  ← ByteTrack
│  Tracking           │
└────────┬────────────┘
         │
┌────────▼────────────┐
│  Proximity Alerts   │  ← Distance estimation, zone logic
└────────┬────────────┘
         │
┌────────▼────────────┐
│  Event Generator    │  ← Structured event payloads
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
PostgreSQL  FastAPI
    │         │
    └────┬────┘
         ▼
     Power BI
```

---

## Planned Modules

| Module              | Status      | Description                              |
|---------------------|-------------|------------------------------------------|
| PPE Detection       | In Progress | Helmet/vest/person detection via YOLOv8  |
| Vehicle Detection   | Planned     | Truck/car detection via YOLOv8           |
| Multi-Object Track  | Planned     | ByteTrack integration                    |
| Proximity Alerts    | Planned     | Person-vehicle distance logic            |
| Database Layer      | Planned     | PostgreSQL event persistence             |
| FastAPI Backend     | Planned     | REST API for events and inference        |
| Power BI Dashboard  | Planned     | KPI visualization and reporting          |
| Dockerization       | Planned     | Containerized deployment                 |
| Cloud Deployment    | Future      | AWS / Azure production deployment        |

---

## Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Detection          | YOLOv8 (Ultralytics)                |
| Tracking           | ByteTrack                           |
| Computer Vision    | OpenCV                              |
| Deep Learning      | PyTorch                             |
| Backend API        | FastAPI                             |
| Database           | PostgreSQL + SQLAlchemy             |
| Dashboard          | Power BI                            |
| Containerization   | Docker + Docker Compose             |
| Cloud (Future)     | AWS SageMaker / Azure ML            |
| Language           | Python 3.12                         |
| Experiment Track   | MLflow (planned)                    |

---

## Roadmap

### Phase 1 — PPE Detection (Current)
- [x] Repository architecture and documentation
- [ ] Dataset exploration and cleaning (`datasets/raw/ppe/`)
- [ ] YOLOv8 fine-tuning on Construction Site Safety Dataset
- [ ] Evaluation: mAP, precision, recall
- [ ] Video inference pipeline

### Phase 2 — Vehicle Detection
- [ ] BDD100K / COCO dataset integration
- [ ] YOLOv8 vehicle model training
- [ ] Evaluation and video inference

### Phase 3 — Tracking
- [ ] ByteTrack integration with detection outputs
- [ ] Multi-object ID assignment and persistence

### Phase 4 — Proximity Alerts
- [ ] Person-vehicle distance estimation
- [ ] Zone-based alert logic
- [ ] Alert severity classification

### Phase 5 — Database & API
- [ ] PostgreSQL schema design
- [ ] SQLAlchemy ORM models
- [ ] FastAPI endpoint implementation
- [ ] Authentication layer

### Phase 6 — Dashboard & Deployment
- [ ] Power BI dataset connection
- [ ] KPI dashboard design
- [ ] Docker Compose multi-service setup
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS / Azure)

---

## Dataset Credits

- **Construction Site Safety** — Kaggle (PPE detection)
- **BDD100K** — Berkeley DeepDrive (vehicle detection, planned)
- **COCO** — Microsoft (general objects, planned)
- **MOT17** — Multiple Object Tracking benchmark (planned)

---

## Project Structure

```
SmartMine-Vision-AI/
├── datasets/        # Raw and processed datasets
├── notebooks/       # Jupyter notebooks per module
├── src/             # Production source code
├── models/          # Trained model weights
├── outputs/         # Inference results, logs
├── configs/         # YAML configs for training/inference
├── powerbi/         # Power BI report files
├── database/        # SQL schemas and migrations
├── api/             # FastAPI application
├── docker/          # Dockerfiles and Compose files
├── docs/            # Architecture docs, diagrams, research
└── experiments/     # Experiment tracking and results
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/SmartMine-Vision-AI.git
cd SmartMine-Vision-AI

# Create conda environment
conda env create -f environment.yml
conda activate smartmine

# Or install with pip
pip install -r requirements.txt
```

### One-time setup for notebook contributors

Run this once per local clone to install the `nbstripout` git filter.
It ensures notebooks are always committed without outputs or execution
counts, preventing merge conflicts on notebook metadata:

```bash
make dev-setup
```

After this, `git add` on any `.ipynb` file will automatically strip
outputs before staging. Your local notebook still shows outputs while
running — only what reaches the index (and therefore the remote) is clean.

### Downloading datasets

See [`datasets/README.md`](datasets/README.md) and
[`docs/specs/SPEC-004-vehicle-dataset.md`](docs/specs/SPEC-004-vehicle-dataset.md)
for dataset sources and download instructions.

```bash
# Copy and fill in your Roboflow API key
cp .env.example .env
# Edit .env and set ROBOFLOW_API_KEY

# Download all source datasets
python scripts/download_datasets.py
```

---

## License

MIT License — see `LICENSE` for details.

---

*Built incrementally as a production portfolio project. Each module is developed, tested, and documented before moving to the next.*
