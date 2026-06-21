# Constitution — SmartMine Vision AI

Principios y convenciones que todo spec, PR y notebook del proyecto respeta.
Es el documento más estable del repo: cambia poco y solo por acuerdo explícito.

Status: draft · Created: 2026-06-21

---

## 1. Principios de proceso

1. **Los specs son la fuente de verdad técnica.** El código implementa un spec;
   la doc describe lo que el spec define. Ante conflicto entre código, propuesta
   y spec, se resuelve **actualizando el spec** — no ignorándolo.

2. **La propuesta comercial es previsión, no contrato técnico.**
   `docs/SmartMine_Vision_AI_Project_Proposal.md` fija visión y metas de negocio
   (mAP > 0.70, FPS, tiempos). Son objetivos a tener en cuenta, no acceptance
   criteria. Los criterios viven en los specs.

3. **Estado explícito sobre estado implícito.** Todo documento o notebook que
   reporte resultados declara su `Status` (draft / previsión / validado). Está
   prohibido afirmar "Complete ✅" o "Clean" sobre algo que no se ejecutó o
   verificó. (Hoy los notebooks 02 y 06 violan esto — ver SPEC-002 AC-5.)

4. **Regla de actualización (anti-drift).** Todo PR que cambia comportamiento
   actualiza el spec correspondiente en el **mismo** PR. Si un cambio invalida
   una afirmación de un notebook/doc, se regenera o se corrige en el mismo PR.
   El drift documentado es deuda; el drift silencioso es un bug.

---

## 2. Convenciones técnicas

### Notebooks son artefactos generados
Los `.ipynb` bajo `notebooks/` se **generan** con `scripts/generate_notebooks.py`.
- Editás el **generador**, nunca el `.ipynb`.
- Tras tocar el generador —o cualquier API de `src/` que el generador consuma—
  **regenerás**: `python3 scripts/generate_notebooks.py`.
- Un `.ipynb` editado a mano se pierde en la próxima regeneración.

### Código
- Idioma: código, comentarios y docstrings en **inglés**. Las clases de dominio
  van en español por dataset (`person_con_casco`) — eso es dato, no código.
- `from __future__ import annotations` y type hints en toda firma pública.
- Paths **siempre** desde `src/ppe_detection/utils.py`. Prohibido hardcodear
  rutas absolutas: un path de una máquina rompe en todas las demás
  (caso real: `configs/yaml/smartmine_unified.yaml` apunta a `/Users/nanolescuras/...`).
- `src/` no es un paquete instalable: se importa vía `sys.path` resuelto por el
  setup cell (camina hacia arriba buscando `src/`). No asumir `pip install -e`.

### Git
- Conventional commits con scope: `feat(trainer):`, `fix(nb05):`, `docs(specs):`,
  `chore:`, `refactor:`. El scope es el módulo o el notebook.
- Trabajo nuevo en rama; no se commitea a `main` directo.

### Entorno
- Versión de Python: **a unificar** (hoy: 3.12 en requirements/environment,
  3.14.2 en el generador, 3.9 en la historia de commits — ver SPEC-002 AC-3).
  Hasta resolverse, ninguna afirmación de versión es autoritativa.
