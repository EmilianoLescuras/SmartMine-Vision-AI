<!--
SYNC IMPACT REPORT
Version change: (template) → 1.0.0
Migrated from: docs/specs/constitution.md (2026-06-21)
Added sections: Core Principles (4), Technical Conventions (4 sub-sections), Governance
Templates checked:
  ✅ .specify/templates/plan-template.md — Constitution Check gate is generic; no updates needed
  ✅ .specify/templates/spec-template.md — no principle-driven mandatory sections added
  ✅ .specify/templates/tasks-template.md — no task categories added or removed
Deferred TODOs:
  - Python version unification (see Principle IV / Entorno)
  - Owner field for existing specs (SPEC-001, SPEC-002)
-->

# SmartMine Vision AI — Constitution

Principios y convenciones que todo spec, PR y notebook del proyecto respeta.
Es el documento más estable del repo: cambia poco y solo por acuerdo explícito.

## Core Principles

### I. Specs como fuente de verdad técnica

Los specs son el contrato técnico del proyecto. El código implementa un spec;
la documentación describe lo que el spec define. Ante cualquier conflicto entre
código, propuesta o especificación, se resuelve **actualizando el spec** — nunca
ignorándolo ni resolviendo en silencio.

- Todo PR que cambia comportamiento observable MUST incluir la actualización del
  spec correspondiente en el **mismo** PR.
- El drift documentado es deuda técnica; el drift silencioso es un bug.

### II. La propuesta comercial es visión, no contrato

`docs/SmartMine_Vision_AI_Project_Proposal.md` fija objetivos de negocio
(mAP > 0.70, FPS objetivo, tiempos de respuesta). Estos son metas a considerar,
no acceptance criteria. Los criterios de aceptación MUST vivir en los specs.

### III. Estado explícito sobre estado implícito

Todo documento o notebook que reporte resultados MUST declarar su `Status`
explícito: `draft` / `previsión` / `validado`. Está prohibido afirmar
"Complete ✅" o "Clean" sobre artefactos que no fueron ejecutados o verificados
en la sesión actual.

### IV. Notebooks son artefactos generados, no fuente

Los `.ipynb` bajo `notebooks/` se generan con `scripts/generate_notebooks.py`.

- Se edita el **generador**, nunca el `.ipynb` directamente.
- Tras modificar el generador o cualquier API de `src/` que consuma, MUST
  regenerarse: `python3 scripts/generate_notebooks.py`.
- Un `.ipynb` editado a mano se pierde en la próxima regeneración.

## Technical Conventions

### Código

- Idioma: código, comentarios y docstrings en **inglés**. Las clases de dominio
  van en español cuando lo impone el dataset (`person_con_casco`) — eso es dato,
  no código.
- `from __future__ import annotations` y type hints en toda firma pública.
- Paths MUST resolverse siempre desde `src/ppe_detection/utils.py`. Prohibido
  hardcodear rutas absolutas (caso real: `configs/yaml/smartmine_unified.yaml`
  apuntaba a `/Users/nanolescuras/...` y rompía en todas las demás máquinas).
- `src/` no es un paquete instalable: se importa vía `sys.path` resuelto por la
  setup cell de cada notebook (camina hacia arriba buscando `src/`). No asumir
  `pip install -e`.

### Git

- Conventional commits con scope: `feat(trainer):`, `fix(nb05):`,
  `docs(specs):`, `chore:`, `refactor:`. El scope es el módulo o el notebook.
- Trabajo nuevo en rama; no se commitea a `main` directamente.

### Entorno

- Versión de Python: **pendiente de unificación**. Hoy coexisten 3.12
  (requirements/environment), 3.14.2 (generador) y 3.9 (historia de commits).
  Hasta que se resuelva, ninguna afirmación de versión es autoritativa.
  TODO(PYTHON_VERSION): cerrar en SPEC-003 o spec de plataforma.

### Estructura de specs

- Specs históricos (Fase 1): `docs/specs/` — registro inmutable, no se mueven.
- Features nuevas con spec-kit: `specs/<###-feature-name>/` con `spec.md`,
  `plan.md`, `tasks.md` generados por las skills `/speckit-*`.

## Governance

- Esta constitución MUST ser leída por el agente al inicio de cada sesión
  (vive en `.specify/memory/constitution.md`).
- Enmiendas requieren acuerdo explícito y MUST actualizarse en el mismo PR que
  introduce el cambio que las motiva.
- Versioning semántico:
  - MAJOR: eliminación o redefinición incompatible de un principio.
  - MINOR: principio nuevo o expansión material de uno existente.
  - PATCH: clarificaciones, redacción, correcciones tipográficas.
- Compliance: todo PR MUST verificar que no contradice ningún principio de esta
  constitución antes de mergearse.

**Version**: 1.0.0 | **Ratified**: 2026-06-21 | **Last Amended**: 2026-06-24
