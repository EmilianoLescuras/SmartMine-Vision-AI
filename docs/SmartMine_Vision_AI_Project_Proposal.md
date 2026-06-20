# SmartMine Vision AI
## Propuesta Técnica y Comercial
### Plataforma Inteligente de Monitoreo de Seguridad para Minería e Industria 4.0

---

> **Versión:** 1.0  
> **Fecha:** Junio 2026  
> **Clasificación:** Confidencial

---

# ÍNDICE

1. Resumen Ejecutivo
2. El Problema
3. La Solución
4. Arquitectura Técnica
5. Módulos del Sistema
6. Plan de Implementación y Tiempos
7. Tiempo de Llegada a Producción
8. Beneficios para la Empresa
9. Análisis de ROI
10. Tecnologías Utilizadas
11. Preguntas Frecuentes

---

# 1. RESUMEN EJECUTIVO

SmartMine Vision AI es una plataforma de inteligencia artificial aplicada a visión computacional, diseñada específicamente para **monitorear la seguridad en sitios mineros e industriales en tiempo real**.

El sistema analiza automáticamente feeds de cámaras de vigilancia ya existentes para:

- Detectar si los trabajadores usan el Equipo de Protección Personal (EPP) obligatorio.
- Alertar cuando un vehículo pesado se acerca peligrosamente a un operario.
- Registrar cada evento en una base de datos centralizada.
- Visualizar el estado de seguridad del sitio en dashboards en tiempo real.

**No requiere reemplazar infraestructura existente.** Se conecta a las cámaras ya instaladas en el sitio y comienza a generar valor desde el primer día de despliegue.

---

# 2. EL PROBLEMA

## 2.1 La Realidad de la Seguridad Minera

La industria minera es uno de los sectores con mayor tasa de accidentes laborales a nivel mundial. Según datos de la Organización Internacional del Trabajo (OIT):

- **La minería representa menos del 1% de la fuerza laboral global pero genera el 8% de los accidentes mortales.**
- El 70% de los accidentes graves en sitios mineros involucran **falta de EPP** o **colisiones vehículo-persona**.
- El costo promedio de un accidente grave para una empresa minera supera los **USD 500,000** contando atención médica, paralización de operaciones, litigios y multas regulatorias.

## 2.2 Las Limitaciones del Control Manual

Los métodos actuales de supervisión de seguridad tienen fallas estructurales:

| Método Actual | Problema |
|---|---|
| Supervisor en campo | No puede estar en todos los puntos a la vez |
| Revisión de cámaras por personal | Costoso, propenso a fatiga visual, reactivo |
| Auditorías periódicas | Detectan problemas después de que ocurrieron |
| Planillas de cumplimiento | Datos manuales, fácilmente alterables |
| Alarmas manuales | Solo funcionan cuando alguien las activa |

## 2.3 El Costo de No Actuar

Un solo accidente grave puede costar a la empresa:

- **USD 200,000 – 1,000,000** en indemnizaciones y atención médica.
- **10 a 30 días** de paralización parcial o total de operaciones.
- **Multas regulatorias** que en muchos países superan los USD 100,000 por infracción.
- **Daño reputacional** que afecta contratos futuros y relaciones con comunidades.
- **Procesos penales** para directivos en caso de accidente fatal.

---

# 3. LA SOLUCIÓN

## 3.1 ¿Qué es SmartMine Vision AI?

Es un sistema de software que utiliza **modelos de inteligencia artificial de visión computacional** para analizar el video de las cámaras del sitio minero en tiempo real, sin intervención humana.

El sistema:

1. **Ve** — Analiza cada fotograma del video capturado por las cámaras.
2. **Detecta** — Identifica personas, cascos, chalecos, vehículos y equipos pesados.
3. **Clasifica** — Determina si cada trabajador es SEGURO o EN RIESGO.
4. **Alerta** — Genera una notificación inmediata cuando detecta una infracción.
5. **Registra** — Guarda cada evento en base de datos con timestamp, imagen y descripción.
6. **Reporta** — Muestra un dashboard en tiempo real con el estado de seguridad del sitio.

## 3.2 ¿Cómo Funciona? (Sin Tecnicismos)

Imagine que coloca un supervisor digital con visión perfecta en cada cámara del sitio, que nunca se distrae, nunca se cansa, trabaja las 24 horas los 365 días del año, y puede procesar hasta **120 fotogramas por segundo** por cámara.

Ese supervisor digital:

- Sabe exactamente qué es un casco y qué no lo es.
- Sabe cuándo un camión está demasiado cerca de un operario.
- Genera una alerta en menos de **1 segundo** desde que detecta el problema.
- Lleva un registro perfecto, automático e inalterable de todo lo que ocurre.

---

# 4. ARQUITECTURA TÉCNICA

```
┌─────────────────────────────────────────────────────────────┐
│                     FUENTE DE VIDEO                         │
│          Cámaras IP / RTSP / Archivos de video              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              MÓDULO 1: DETECCIÓN DE EPP                     │
│   YOLOv8 — detecta: Casco, Chaleco, Persona,               │
│   NO-Casco, NO-Chaleco (violación directa)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           MÓDULO 2: DETECCIÓN DE VEHÍCULOS                  │
│   YOLOv8 — detecta: Camión, Auto, Maquinaria                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          MÓDULO 3: TRACKING MULTI-OBJETO                    │
│   ByteTrack — asigna ID único a cada persona/vehículo       │
│   y mantiene su identidad entre fotogramas                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          MÓDULO 4: ALERTAS DE PROXIMIDAD                    │
│   Calcula distancia persona-vehículo en tiempo real.        │
│   Zona ADVERTENCIA (amarilla) / Zona CRÍTICA (roja)         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
              ┌─────────┴──────────┐
              ▼                    ▼
┌─────────────────────┐  ┌─────────────────────┐
│   BASE DE DATOS     │  │    API REST          │
│   PostgreSQL        │  │    FastAPI           │
│   Registra eventos  │  │    Conecta sistemas  │
│   y alertas         │  │    externos          │
└─────────┬───────────┘  └──────────┬──────────┘
          └──────────────┬──────────┘
                         ▼
          ┌──────────────────────────────┐
          │      DASHBOARD POWER BI      │
          │   KPIs en tiempo real        │
          │   Historial de incidentes    │
          │   Reportes de cumplimiento   │
          └──────────────────────────────┘
```

---

# 5. MÓDULOS DEL SISTEMA

## Módulo 1 — Detección de EPP (Etapa Actual)

**Objetivo:** Determinar si cada trabajador visible en cámara porta el EPP obligatorio.

**Clases detectadas:**
| Clase | Descripción |
|---|---|
| Persona | Trabajador en campo |
| Casco (Hardhat) | EPP compliant ✅ |
| Chaleco de Seguridad | EPP compliant ✅ |
| NO-Casco | Violación detectada ❌ |
| NO-Chaleco | Violación detectada ❌ |

**Resultado por trabajador:** `SEGURO` o `EN RIESGO` + registro de qué EPP falta.

**Tiempo de respuesta:** < 50 ms por fotograma en GPU.

---

## Módulo 2 — Detección de Vehículos

**Objetivo:** Identificar y localizar vehículos pesados en el campo visual.

**Clases detectadas:** Camión, Auto, Maquinaria pesada, Motocicleta.

**Integración:** Los vehículos detectados alimentan al módulo de alertas de proximidad.

---

## Módulo 3 — Tracking Multi-Objeto

**Objetivo:** Mantener la identidad de cada trabajador y vehículo entre fotogramas.

**Beneficio clave:** Permite saber que el trabajador ID-042 estuvo sin casco durante 3 minutos en la zona B, no solo que "alguien" estaba sin casco en un fotograma aislado.

**Tecnología:** ByteTrack — algoritmo de tracking de última generación, robusto a oclusiones parciales y cambios de velocidad.

---

## Módulo 4 — Alertas de Proximidad

**Objetivo:** Detectar situaciones de peligro antes de que ocurra el accidente.

**Zonas de alerta:**

```
[ZONA CRÍTICA] < 3 metros entre persona y vehículo en movimiento
   → Alerta inmediata + sirena + registro de imagen

[ZONA ADVERTENCIA] 3-8 metros entre persona y vehículo
   → Alerta visual en dashboard + registro
```

---

## Módulo 5 — Base de Datos y API

**Objetivo:** Persistir cada evento para auditoría, compliance y análisis.

**Cada registro incluye:**
- Timestamp exacto
- Cámara origen
- Tipo de evento (EPP / Proximidad)
- Imagen capturada del momento
- ID del trabajador (si tracking activo)
- Severidad del evento

**API REST:** Permite integración con sistemas ERP, SCADA, o plataformas de gestión de seguridad ya existentes en la empresa.

---

## Módulo 6 — Dashboard y Reportes

**Herramienta:** Power BI conectado a la base de datos en tiempo real.

**KPIs disponibles:**
- Tasa de cumplimiento de EPP por turno / zona / trabajador
- Número de alertas de proximidad por día
- Mapa de calor de incidentes por zona del sitio
- Ranking de zonas más peligrosas
- Reporte automático para auditorías regulatorias

---

# 6. PLAN DE IMPLEMENTACIÓN Y TIEMPOS

## 6.1 Fases de Desarrollo

### FASE 1 — Detección de EPP *(En Curso)*
**Duración: 5-6 semanas**

| Semana | Actividad |
|---|---|
| 1-2 | Exploración y validación del dataset. Configuración del entorno. |
| 3-4 | Entrenamiento del modelo YOLOv8 (100 épocas). |
| 5 | Evaluación de métricas. Ajuste de umbrales. |
| 6 | Inferencia en imagen y video. Integración lógica SEGURO/EN RIESGO. |

**Entregable:** Modelo funcional con mAP50 > 0.70. Pipeline de video operativo.

---

### FASE 2 — Detección de Vehículos
**Duración: 4 semanas**

| Semana | Actividad |
|---|---|
| 7-8 | Adquisición y preparación del dataset vehicular (BDD100K / COCO). |
| 9 | Entrenamiento y evaluación del modelo de vehículos. |
| 10 | Integración con pipeline existente. Tests combinados. |

**Entregable:** Detección simultánea de personas y vehículos en mismo frame.

---

### FASE 3 — Tracking Multi-Objeto
**Duración: 3-4 semanas**

| Semana | Actividad |
|---|---|
| 11-12 | Integración de ByteTrack con los dos modelos de detección. |
| 13 | Asignación de IDs persistentes. Tests de robustez en videos largos. |
| 14 | Optimización de velocidad. Documentación. |

**Entregable:** Cada persona y vehículo mantiene ID único a través de los frames.

---

### FASE 4 — Alertas de Proximidad
**Duración: 3 semanas**

| Semana | Actividad |
|---|---|
| 15-16 | Motor de cálculo de distancia persona-vehículo. Definición de zonas. |
| 17 | Tests en videos reales del sitio. Calibración de umbrales. |

**Entregable:** Sistema de alertas automático en tiempo real.

---

### FASE 5 — Base de Datos y API
**Duración: 4-5 semanas**

| Semana | Actividad |
|---|---|
| 18-19 | Diseño del esquema PostgreSQL. Implementación ORM SQLAlchemy. |
| 20-21 | Desarrollo de la API REST con FastAPI. Autenticación. |
| 22 | Tests de integración. Documentación de endpoints. |

**Entregable:** API productiva con todos los eventos persistidos y consultables.

---

### FASE 6 — Dashboard, Docker y Deployment
**Duración: 5-6 semanas**

| Semana | Actividad |
|---|---|
| 23-24 | Conexión Power BI a PostgreSQL. Diseño de reportes y KPIs. |
| 25-26 | Dockerización de todos los servicios. Docker Compose. |
| 27-28 | CI/CD pipeline. Deployment en infraestructura cloud (AWS/Azure). |

**Entregable:** Sistema completo, containerizado y desplegado en la nube.

---

## 6.2 Resumen de Timeline de Desarrollo

```
SEMANA:    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
           ├──────────────┤
Fase 1     █  █  █  █  █  █
EPP        └──────────────┘
                           ├──────────┤
Fase 2                     █  █  █  █
Vehículos                  └──────────┘
                                       ├──────────┤
Fase 3                                 █  █  █  █
Tracking                               └──────────┘
                                                   ├──────┤
Fase 4                                             █  █  █
Proximidad                                         └──────┘
                                                          ├──────────┤
Fase 5                                                    █  █  █  █  █
DB + API                                                  └──────────┘
                                                                       ├──────────────┤
Fase 6                                                                 █  █  █  █  █  █
Deploy                                                                 └──────────────┘
```

**TIEMPO TOTAL DE DESARROLLO: 28 semanas (~7 meses)**

---

# 7. TIEMPO DE LLEGADA A PRODUCCIÓN

Una vez finalizado el desarrollo, el proceso de despliegue en el sitio minero requiere:

## Etapa A — Preparación de Infraestructura *(2-3 semanas)*
- Evaluación de red y conectividad en el sitio.
- Instalación o verificación de cámaras IP con soporte RTSP.
- Provisioning del servidor GPU (on-premise o cloud).
- Configuración de la base de datos de producción.

## Etapa B — Instalación y Configuración *(2 semanas)*
- Despliegue de contenedores Docker en el servidor.
- Conexión a las cámaras existentes del sitio.
- Calibración de zonas de alerta según el layout del sitio.
- Configuración de umbrales de confianza para el entorno real.

## Etapa C — Prueba Piloto *(4 semanas)*
- Operación paralela con supervisión humana.
- Ajuste fino del modelo con imágenes del sitio específico.
- Validación de alertas con el equipo de seguridad.
- Recopilación de feedback de operadores.

## Etapa D — Capacitación y Go-Live *(1-2 semanas)*
- Capacitación del equipo de seguridad en el uso del dashboard.
- Capacitación del equipo IT en mantenimiento del sistema.
- Documentación específica del sitio.
- Lanzamiento oficial.

---

## 7.1 Resumen Timeline Producción

```
┌─────────────────────────────────────────────────────────────┐
│  Fin Desarrollo  │  Preparación  │   Prueba    │  Go-Live   │
│   Semana 28      │   3 semanas   │  4 semanas  │  2 semanas │
│                  │               │             │            │
│                  ├───────────────┼─────────────┼────────────┤
│                  │  Infra Setup  │   Piloto    │ Producción │
└─────────────────────────────────────────────────────────────┘

TOTAL POST-DESARROLLO: ~9-11 semanas hasta Go-Live completo
TIEMPO TOTAL (Desarrollo + Producción): ~9-10 meses
```

---

# 8. BENEFICIOS PARA LA EMPRESA

## 8.1 Beneficios de Seguridad

| Beneficio | Impacto Estimado |
|---|---|
| Reducción de accidentes por falta de EPP | 60-80% |
| Reducción de incidentes vehículo-persona | 40-65% |
| Tiempo de detección de infracción | < 1 segundo (vs. minutos o nunca) |
| Cobertura de monitoreo | 100% del tiempo (vs. 10-20% con supervisores) |
| Documentación automática de incidentes | 100% de trazabilidad |

## 8.2 Beneficios Operativos

- **Liberación de supervisores** para tareas de mayor valor agregado.
- **Datos objetivos** para toma de decisiones de seguridad.
- **Historial completo** para auditorías regulatorias sin trabajo manual.
- **Identificación de zonas de riesgo** basada en datos reales, no percepciones.
- **Reportes automáticos** para cumplimiento normativo.

## 8.3 Beneficios Financieros

| Concepto | Ahorro Anual Estimado |
|---|---|
| Reducción de accidentes graves | USD 300,000 – 800,000 |
| Reducción de multas regulatorias | USD 50,000 – 200,000 |
| Optimización de supervisión | USD 80,000 – 150,000 |
| Reducción de primas de seguro | USD 30,000 – 100,000 |
| **TOTAL ESTIMADO** | **USD 460,000 – 1,250,000 / año** |

## 8.4 Beneficios Estratégicos

- **Ventaja competitiva** en licitaciones que requieren altos estándares de seguridad.
- **Certificaciones internacionales** (ISO 45001) más accesibles con datos automatizados.
- **Cultura de seguridad** — cuando los trabajadores saben que el sistema monitorea, el cumplimiento mejora naturalmente.
- **Reputación corporativa** — demostrar inversión tecnológica en seguridad ante inversores, reguladores y comunidades.

---

# 9. ANÁLISIS DE ROI

## Inversión vs. Retorno

```
INVERSIÓN (Año 1)
─────────────────────────────────────────────
Desarrollo del sistema         USD  80,000
Infraestructura (servidores)   USD  15,000
Instalación y capacitación     USD  10,000
Mantenimiento anual            USD  20,000
─────────────────────────────────────────────
TOTAL INVERSIÓN AÑO 1          USD 125,000

AHORRO ESTIMADO AÑO 1
─────────────────────────────────────────────
Escenario conservador          USD 460,000
Escenario optimista            USD 1,250,000
─────────────────────────────────────────────

ROI CONSERVADOR:  +268% en el primer año
ROI OPTIMISTA:    +900% en el primer año
PAYBACK PERIOD:   2 a 4 meses
```

> *Estimaciones basadas en datos de industria minera LATAM e internacional.
> Los valores exactos dependen del tamaño del sitio, número de cámaras y
> frecuencia histórica de accidentes.*

---

# 10. TECNOLOGÍAS UTILIZADAS

| Capa | Tecnología | Por qué |
|---|---|---|
| Detección | YOLOv8 (Ultralytics) | Estado del arte en detección en tiempo real |
| Tracking | ByteTrack | Mejor rendimiento en entornos con oclusión |
| Visión | OpenCV | Biblioteca estándar industrial para video |
| Deep Learning | PyTorch | Framework líder en investigación y producción |
| Backend | FastAPI (Python) | Alta performance, documentación automática |
| Base de Datos | PostgreSQL | Robustez y soporte para análisis temporal |
| Dashboard | Power BI | Adoptado en la mayoría de empresas mineras |
| Contenedores | Docker + Docker Compose | Deployment reproducible y escalable |
| Cloud (futuro) | AWS / Azure | Escalabilidad y redundancia |
| Lenguaje | Python 3.12 | Ecosistema IA más maduro del mercado |

---

# 11. PREGUNTAS FRECUENTES

**¿El sistema requiere reemplazar las cámaras existentes?**
No. Se conecta a cualquier cámara IP con soporte RTSP, que es el estándar de la industria. La mayoría de instalaciones modernas ya lo soportan.

**¿Qué pasa si la conexión a internet falla?**
El sistema puede operar completamente on-premise (en el propio servidor del sitio) sin dependencia de internet. Los datos se sincronizan cuando la conexión se restaura.

**¿Qué tan preciso es el sistema?**
Con el entrenamiento en el dataset de seguridad en construcción, se espera una precisión (mAP50) superior al 75%. Este número mejora cuando se fine-tunea el modelo con imágenes del sitio específico del cliente.

**¿Puede manejar condiciones de poca luz o polvo?**
El rendimiento disminuye en condiciones extremas de visibilidad. Se puede complementar con cámaras infrarrojas o de baja luz. Es una limitación conocida que se documenta y gestiona en el plan de deployment.

**¿El sistema puede identificar a trabajadores individuales?**
En la versión actual, el sistema clasifica trabajadores pero no los identifica por nombre. La integración con sistemas de identificación biométrica es posible en fases futuras.

**¿Cuántas cámaras puede manejar simultáneamente?**
Depende del hardware. Con una GPU RTX 3090, el sistema puede procesar entre 4-8 streams de video en tiempo real (30 FPS cada uno). Para más cámaras, se escala horizontalmente con más servidores.

---

# APÉNDICE — SPEECH DE PRESENTACIÓN

*(Ver documento adjunto: `SmartMine_Vision_AI_Speech.md`)*

---

*Documento preparado por: Emiliano Lescuras*
*SmartMine Vision AI — Proyecto de Portfolio Profesional*
*Contacto: lescurasnana@gmail.com*
