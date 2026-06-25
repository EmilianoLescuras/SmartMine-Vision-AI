# SPEC-004 — Vehicle Dataset Sourcing & Homologation

## Status
`IMPLEMENTED`

## Problem

The SmartMine unified corpus already integrates three vehicle/PPE datasets
(`riskalert`, `deteccion_escenarios`, `mining_area`), but the download
process was entirely manual: no script existed, collaborators had to locate
the sources independently, and the exact workspace/project/version IDs were
not recorded. Adding two new Roboflow Universe sources for the vehicle
detection module required a formal sourcing mechanism.

## Solution

1. **`scripts/download_datasets.py`** — single entry point that downloads all
   four Roboflow Universe sources to their canonical locations under
   `datasets/raw/vehicles/`. It is idempotent (skips if already present),
   reads the API key from `ROBOFLOW_API_KEY` env var (or `.env`), and prints
   clear instructions when the key is missing.

2. **`notebooks/02_vehicle_detection/01_dataset_download.ipynb`** — generated
   notebook that wraps the download call and validates the downloaded structure.
   Executes without errors even when data is absent (shows a "data not found"
   guidance block instead of crashing).

3. **`notebooks/02_vehicle_detection/02_dataset_exploration.ipynb`** — generated
   notebook that runs class distribution, image count, and bbox geometry
   analysis on the downloaded vehicle datasets. Uses the same guard pattern as
   PPE notebooks (`if DATA_AVAILABLE:`).

4. **`.env.example`** — documents `ROBOFLOW_API_KEY` so any collaborator
   cloning the repo knows exactly what credential is needed.

## Dataset Sources

| Alias | Roboflow Universe URL | Workspace | Project | Local path |
|---|---|---|---|---|
| `construction_vehicles` | [/0925/construction-vehicle-inspection](https://universe.roboflow.com/0925/construction-vehicle-inspection) | `0925` | `construction-vehicle-inspection` | `datasets/raw/vehicles/construction_vehicles/` |
| `mining_area_detection` | [/septiana-s-workspace/mining-area-vehicle-detection](https://universe.roboflow.com/septiana-s-workspace/mining-area-vehicle-detection) | `septiana-s-workspace` | `mining-area-vehicle-detection` | `datasets/raw/vehicles/mining_area_detection/` |
| `riskalert` | [/personal-q02wc/riskalert-mining](https://universe.roboflow.com/personal-q02wc/riskalert-mining) | `personal-q02wc` | `riskalert-mining` | `datasets/raw/vehicles/riskalert/` |
| `riskalertai` | [/personal-q02wc/riskalertai-mining](https://universe.roboflow.com/personal-q02wc/riskalertai-mining) | `personal-q02wc` | `riskalertai-mining` | `datasets/raw/vehicles/riskalertai/` |

## Download Format

All datasets are downloaded in **YOLOv8 format** (`cx cy w h` normalised),
which is the native format for Ultralytics and compatible with
`scripts/merge_datasets.py`.

## Acceptance Criteria

1. `scripts/download_datasets.py` exists and is runnable.
2. Running it with a valid `ROBOFLOW_API_KEY` downloads all four sources to
   their canonical local paths.
3. Running it without a key prints a clear error with setup instructions
   and exits with code 1 — it does NOT crash or produce a traceback.
4. `notebooks/02_vehicle_detection/01_dataset_download.ipynb` executes
   without errors whether or not data is present locally.
5. `notebooks/02_vehicle_detection/02_dataset_exploration.ipynb` executes
   without errors; when data is absent it prints a "data not found" notice
   and skips the analysis sections gracefully.
6. `.env.example` documents the `ROBOFLOW_API_KEY` variable.
7. All four source directories have `.gitkeep` placeholders committed, so
   the directory structure is reproducible on a fresh clone.

## Implementation Notes

- `roboflow` Python SDK is added to `requirements.txt` and `environment.yml`.
- The `.env` file (with the actual key) is already in `.gitignore`; only
  `.env.example` is committed.
- Download is version-pinned per source (see `SOURCES` dict in the script).
  To upgrade a dataset version, update the version number there.
- The `riskalert` source is also used by the existing PPE unified corpus.
  Its raw files should **not** be deleted before checking `merge_datasets.py`.

## References

- Roboflow Python SDK — `pip install roboflow`
- [Roboflow Universe](https://universe.roboflow.com/)
- `datasets/README.md` — full dataset catalogue with source attributions
