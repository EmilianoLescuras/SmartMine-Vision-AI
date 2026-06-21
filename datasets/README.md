# datasets/

All datasets used by SmartMine Vision AI. Raw data is **never committed
to git** (see `.gitignore`). Only README files and `.gitkeep`
placeholders are tracked.

---

## Structure

```
datasets/
├── raw/              ← Original downloads, untouched
│   ├── ppe/
│   │   └── css-data/                   # Construction Site Safety (Roboflow / Kaggle)
│   └── vehicles/
│       ├── riskalert/                  # Roboflow Universe — personal-q02wc/riskalert-mining
│       ├── deteccion_escenarios/       # Roboflow Universe — mining scene detection
│       └── mining_area/                # Roboflow Universe — mining-area vehicle entry
├── processed/        ← (reserved) intermediate single-source preprocessing
└── merged/
    └── smartmine_v1/                   # Unified 32-class corpus used for training
        ├── train/{images,labels}
        ├── valid/{images,labels}
        ├── test/{images,labels}
        └── data.yaml                   # copy of configs/yaml/smartmine_unified.yaml
```

---

## Unified Corpus — `merged/smartmine_v1`

Produced by `scripts/merge_datasets.py`. Filenames are prefixed with
their source (`css_ppe_…`, `riskalert_…`, `deteccion_escenarios_…`,
`mining_area_…`) so collisions are impossible across sources.

| Property | Value |
|----------|-------|
| Classes | 32 (see `src/ppe_detection/README.md`) |
| Total images | ~5 785 (train + valid + test) |
| Total annotations | ~40 085 |
| Image size | 640 × 640 px (sources are already 640²; merge does not re-encode) |
| Label format | YOLO (cx cy w h normalised) |
| YAML | `configs/yaml/smartmine_unified.yaml` |

To rebuild the merged corpus after editing class maps:

```bash
python scripts/merge_datasets.py
# delete cached YOLO indexes so the new schema is reloaded
find datasets -name "*.cache" -delete
```

The script reports per-source coverage and the top-5 skipped class IDs
so you can see exactly which source labels are being dropped.

---

## Source Datasets

### `raw/ppe/css-data` — Construction Site Safety
- **Source:** Roboflow / Kaggle (CC BY 4.0).
- **Contribution:** generic PPE objects (`hardhat`, `mask`, `safety_vest`)
  and a generic `Person` class that uses spatial overlap for compliance.
- **Split:** 2 605 train / 114 valid / 82 test images.

### `raw/vehicles/riskalert` — RiskAlert Mining
- **Source:** Roboflow Universe — `personal-q02wc/riskalert-mining`.
- **Contribution:** mining-specific personnel labels with embedded PPE
  state (`PERSONA_CON_CASCO`, `PERSONA_SIN_GUANTES`, …) plus heavy
  machinery (`EXCAVADORA`, `VOLQUETE`, `CARGADOR_FRONTAL`, …).
- **Used as primary signal for compliance attributes.**

### `raw/vehicles/deteccion_escenarios` — Mining Scene Detection
- **Source:** Roboflow Universe.
- **Contribution:** color variants of hardhats (`PERSONA_CON_CASCO_AMARILLO`,
  `…_AZUL`), `PERSONA_CON_BARBIJO` (mask), parked vs operating machinery.
  Many scene labels (signage states, road conditions) are intentionally
  skipped — see `scripts/merge_datasets.py` class map.

### `raw/vehicles/mining_area` — Mining-Area Vehicle Entry
- **Source:** Roboflow Universe.
- **Contribution:** heavy vehicle entering a mining zone. Only the
  generic vehicle classes are kept; the area-polygon class is dropped.

---

## Known Gaps

| Gap | Impact | Mitigation |
|-----|--------|------------|
| `botas` (boots) | Required for mining compliance; not labelled in any source. | Need to acquire a labelled corpus (e.g. capture on-site, label with Roboflow). |
| `traje minero` / mining suit | Same. | Same. |
| `person_con_chaleco` (id 3) empty | No source emits this label explicitly. | Compliance is derived from separate `safety_vest` (28) overlapping a generic person — covered by classifier logic. |
| Class imbalance | Heavy machinery 10× fewer instances than person classes. | Roadmap: class-weighted sampling at train time. |

---

## Dependencies

- `ultralytics` — dataset format compatibility and training.
- `pyyaml` — read / write merged `data.yaml`.
- `Pillow`, `opencv-python` — image inspection.
- `pandas` — statistics dataframes.
