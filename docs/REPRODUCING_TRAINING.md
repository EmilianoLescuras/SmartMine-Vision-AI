# Reproducir el entrenamiento en otra máquina

Guía para levantar el corpus y entrenar `smartmine_core` desde cero.
Los datasets **no** están en el repo (gitignoreados por tamaño y licencias);
se regeneran con los scripts de abajo y quedan idénticos al corpus de
referencia (verificable contra `merge_manifest.json`).

## 1. Clonar y preparar

```bash
git clone https://github.com/OPSIA-CV/SmartMine-Vision-AI.git
cd SmartMine-Vision-AI
git checkout 008-dataset-acquisition   # hasta que se mergeen PR #7 y #8
make dev-setup                          # nbstripout + pull.autostash
pip install -r requirements.txt
pip install roboflow python-dotenv
```

## 2. Descargar los datasets (una sola vez)

Crear `.env` en la raíz con una API key gratuita de Roboflow
(app.roboflow.com → Settings → API Keys):

```
ROBOFLOW_API_KEY=xxxx
```

```bash
python scripts/download_datasets.py
```

Esto baja TODO lo que el merge necesita:

| Fuente | Origen | Rol |
|---|---|---|
| `css-data` | Roboflow | EPP genérico (volumen) |
| `riskalert` / `riskalertai` | Roboflow | minería real |
| `deteccion_escenarios` | Roboflow | minería real |
| `construction_ppe` | Ultralytics (zip directo) | botas / lentes / guantes |
| `construction_vehicles` | Roboflow | reserva (aún no mapeado al merge) |

> `mining_area` NO se descarga: está excluido del merge (SPEC-007 — clases de
> evento + labels corruptos).

## 3. Generar el corpus

```bash
python scripts/merge_datasets.py
find datasets -name "*.cache" -delete
```

Salida esperada: `datasets/merged/smartmine_v1` (37 clases, archivo) y
`datasets/merged/smartmine_core` (**26 clases — este es el de entrenar**),
más `merge_manifest.json` con los conteos. Referencia sana: ~5.869 imágenes
totales, 0 líneas en cuarentena.

## 4. Entrenar

```bash
# YAML con path absoluto local (ultralytics no resuelve el relativo)
python - <<'EOF'
import yaml
from pathlib import Path
core = Path("datasets/merged/smartmine_core").resolve()
d = yaml.safe_load(open(core / "data.yaml")); d["path"] = str(core)
yaml.dump(d, open(core / "smartmine_core.autogen.yaml", "w"), allow_unicode=True, sort_keys=False)
EOF

PYTHONPATH=src python -c "
from pathlib import Path
from ppe_detection.trainer import train_ppe_model
train_ppe_model(
    data_yaml=Path('datasets/merged/smartmine_core/smartmine_core.autogen.yaml').resolve(),
    epochs=100, imgsz=640, patience=30,
)"
```

`train_ppe_model` detecta el device solo: **CUDA** usa AutoBatch (config
ideal); en CPU/Mac ver notas abajo.

## Notas por hardware

- **GPU NVIDIA (recomendado):** 100 épocas ≈ 2-4 h. No tocar nada.
- **Apple Silicon (MPS):** pasar `device='mps', batch=16, workers=8`
  explícitos (el default `workers=0` triplica el tiempo). MPS tiene bugs
  esporádicos del backend Metal: si crashea, relanzar con
  `YOLO('.../last.pt').train(resume=True)` — el checkpoint no se pierde.
- **CPU pelado:** solo para smoke tests (`epochs=3, imgsz=416, fraction=0.2`).

## Resultados de referencia (para comparar)

- Baseline actual (26 clases, ~72 ép. acumuladas en MPS): mAP50 global 0.400,
  EPP-objeto ≈ 0.70-0.74. Detalle por clase:
  `docs/research/training_report_baseline2.md`.
- Una corrida limpia de 100 ép. en GPU debería igualar o superar eso.
