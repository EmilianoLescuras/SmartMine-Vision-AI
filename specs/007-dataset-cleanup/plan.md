# SPEC-007 — Plan de implementación

## Archivos a tocar

| Archivo | Cambio |
|---|---|
| `scripts/merge_datasets.py` | Validación de líneas + cuarentena; mining_area comentado; `vehiculo_generico` (32); labels vacíos para backgrounds; generación dual v1 + core; manifiesto JSON. |
| `src/ppe_detection/utils.py` | Agregar id 32 `vehiculo_generico` a `CLASS_NAMES` y `CLASS_COLORS` (al final — ids 0-31 intactos). |
| `configs/yaml/smartmine_unified.yaml` | Regenerado por el merge (33 clases). |
| `configs/yaml/smartmine_core.yaml` | Nuevo, generado por el merge (18 clases). |
| `docs/research/` | Reporte de re-auditoría post-limpieza con conteos finales. |

## Orden de ejecución

1. Modificar `merge_datasets.py` (validación → cuarentena → dual output).
2. Alinear `utils.py` (33 clases).
3. Borrar `merged/smartmine_v1/` viejo y regenerar (v1 + core) en un pase.
4. `find datasets -name "*.cache" -delete`.
5. Re-auditar con el script de auditoría (mismo del informe) → verificar AC-6.
6. `pytest` → AC-7.
7. Actualizar reporte en `docs/research/` con números post-limpieza.

## Riesgos

- **Duplicación de disco** (v1 + core copian imágenes 2×): aceptable para el
  tamaño actual (~1-2 GB); si crece, pasar core a symlinks.
- **Notebooks 01-06** leen `smartmine_unified.yaml` (nc pasa 32→33): el
  generador de notebooks toma el schema de utils → regenerar en spec aparte
  si algo rompe (no bloquea este spec: el corpus v1 es superset).
- **Baseline-7 ya no es comparable** con el próximo run (corpus distinto):
  esperado y deseado — el próximo baseline se mide sobre datos limpios.

## Mapa unified → core (AC-5)

```
0→0 person · 1→1 con_casco · 2→2 sin_casco · 4→3 sin_chaleco
11→4 ropa_reflectiva · 12→5 sin_ropa_reflectiva · 13→6 mask
27→7 hardhat · 28→8 safety_vest · 25→9 safety_cone
14→10 camioneta · 16→11 volquete · 18→12 excavadora
19→13 retro_excavadora · 21→14 motoniveladora · 23→15 rodillo
24→16 cisterna_agua · 31→17 machinery
(resto → drop, contabilizado en manifiesto)
```
