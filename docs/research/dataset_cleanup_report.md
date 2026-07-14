# Reporte post-limpieza de corpus — SPEC-007

**Fecha:** 2026-07-12 · **Ejecución:** `scripts/merge_datasets.py` (SPEC-007) sobre `develop`
**Todos los números medidos por re-auditoría de archivos reales tras regenerar.**

## Antes → Después

| Métrica | Antes (auditoría 2026-07-12) | Después |
|---|---:|---:|
| Líneas malformadas en corpus | 185 | **0** |
| `missing_label` inexplicados | 271 | **0** (265 backgrounds explícitos con label vacío) |
| Falsas instancias en `camion` | 4.179 (61% eventos + 39% genéricos) | **0** (clase vacía, documentada como reservada) |
| Imágenes v1 | 5.785 | 4.453 (−1.332 de mining_area, excluida con rationale) |
| Anotaciones v1 | 42.261 | 39.710 |
| Clases v1 | 32 (1 vacía oculta) | 33 (2 vacías **documentadas**: `person_con_chaleco`, `camion`) |
| Corpus de entrenamiento | no existía (se entrenaba sobre las 32) | **`smartmine_core`: 18 clases, todas ≥100 inst.** |
| Trazabilidad de descartes | ninguna | `merge_manifest.json` + `_quarantine/manifest.json` |

## Corpus core (para SPEC-005)

4.453 imgs · 37.176 anotaciones · 18 clases · mínimo por clase: 101
(`person_sin_ropa_reflectiva`) · config: `configs/yaml/smartmine_core.yaml`

| Clase | Inst. | Clase | Inst. |
|---|---:|---|---:|
| person | 9.944 | safety_cone | 3.725 |
| person_con_casco | 907 | camioneta | 218 |
| person_sin_casco | 2.522 | volquete | 476 |
| person_sin_chaleco | 4.163 | excavadora | 459 |
| person_ropa_reflectiva | 650 | retro_excavadora | 118 |
| person_sin_ropa_reflectiva | 101 | motoniveladora | 128 |
| mask | 1.705 | rodillo | 120 |
| hardhat | 3.334 | cisterna_agua | 125 |
| safety_vest | 3.135 | machinery | 5.346 |

## Verificación (AC de SPEC-007)

- AC-1 ✅ validación activa; 0 líneas en cuarentena en esta corrida (la fuente
  sucia — mining_area — quedó fuera; la validación protege fuentes futuras)
- AC-2 ✅ 0 `missing_label`; 265 (v1) / 383 (core) backgrounds explícitos
- AC-3 ✅ mining_area excluida, rationale en `SOURCES` y en manifiesto
- AC-4 ✅ `vehiculo_generico` (32) con 1.628 inst.; `camion` limpia
- AC-5 ✅ `smartmine_core` generado, 18/18 clases ≥100 inst.
- AC-6 ✅ re-auditoría con ceros; caches YOLO borrados
- AC-7 ✅ pytest 13/13; `utils.CLASS_NAMES` = 33 clases

## Pendiente (fuera de este spec)

- El desbalance de dominio persiste (~88% css-data): se resuelve con las
  adquisiciones P0/P1 de `dataset_audit_opsia.md`, no con limpieza.
- `person_con_chaleco` sigue en 0 hasta sumar datos con chaleco embebido
  (el resolver híbrido lo deriva vía overlap con `safety_vest` en inferencia).
- Próximo paso: baseline completo sobre `smartmine_core` (SPEC-005).
