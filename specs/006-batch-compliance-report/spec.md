# SPEC-006 — Batch Compliance Report (MVP comercial)

Status: draft · pendiente de aprobación del board (decisión D1 del reporte estratégico)
Created: 2026-07-02 · Owner: TBD · Phase: MVP

---

## Context & Problem

El reporte estratégico (`docs/strategy/2026-07_reporte_estrategico_board.md`)
propone como MVP una **auditoría de cumplimiento EPP sobre video grabado**:
el cliente entrega horas de video de sus cámaras y recibe un reporte de
compliance — sin tiempo real, sin instalación en sitio, sin hardware nuevo.

Racional: reusa ~90% del pipeline existente (inferencia + clasificador híbrido
SAFE/UNSAFE/UNKNOWN + export ONNX que corre en CPU), es vendible como servicio
antes de tener producto, y genera video real de sitios para fine-tuning
(cláusula de consentimiento mediante — decisión D6 del board).

Hoy el gap es: `nb06` procesa video y anota frames, pero no existe la capa de
**agregación y reporte** (métricas por período, evidencia por infracción,
salida entregable a un cliente).

## Goals

- CLI/función `generate_compliance_report(video_path | dir, out_dir)` en
  `src/` que procese uno o más videos y produzca:
  - **Resumen ejecutivo:** % de compliance por video/cámara/período, conteo de
    infracciones por tipo (NO-casco, NO-chaleco), serie temporal.
  - **Evidencia:** captura anotada + timestamp por cada infracción detectada
    (con deduplicación temporal — una infracción sostenida = 1 evento, no
    N frames).
  - **Formato entregable:** HTML o PDF auto-contenido + CSV de eventos.
- Ejecutable en CPU (vía ONNX) para delivery sin GPU.
- Parámetros de umbral (confianza, ventana de deduplicación) configurables y
  documentados con sus defaults.

## Non-Goals

- Ingesta RTSP / tiempo real / alertas en vivo (fase pilot-ready, spec futuro).
- Tracking con IDs persistentes (mejoraría la deduplicación; se integra cuando
  exista el módulo 3 — la deduplicación temporal simple es suficiente para MVP).
- Base de datos / API (el entregable es archivo, no servicio).
- Dashboard Power BI.
- Identificación de personas (privacy by design: el reporte cuenta y evidencia,
  no identifica; blur de rostros configurable — ver decisión D5/D6).

## Acceptance Criteria

1. **AC-1:** Sobre un video de test, el comando produce el reporte completo
   (resumen + evidencias + CSV) sin intervención manual.
2. **AC-2:** La deduplicación temporal funciona: una persona sin casco durante
   30 s continuos genera 1 evento con duración, no cientos de eventos.
3. **AC-3:** El pipeline corre en CPU-only con throughput documentado
   (≥ N× tiempo real está OK para batch; N se mide y reporta, no se promete).
4. **AC-4:** Los defaults de umbral están justificados con una mini-evaluación
   (precision/recall de eventos sobre un video etiquetado a mano).
5. **AC-5:** Blur de rostros disponible como flag (default: activado) —
   requisito de privacidad para mostrar reportes a terceros.
6. **AC-6:** Un colaborador que no participó del desarrollo genera un reporte
   siguiendo solo el README del feature.

## Dependencies

- **SPEC-005 (gate):** sin modelo a calidad razonable, el reporte produce
  ruido. Este spec no se implementa hasta que SPEC-005 cierre AC-1/AC-3.
- Video de prueba representativo (idealmente de un prospecto real, con
  permiso; fallback: footage público de obra/minería).
