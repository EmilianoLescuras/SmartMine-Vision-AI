# OPSIA · Monitoreo Inteligente de Seguridad Operacional

**Presentación institucional y propuesta de programa piloto**

| | |
|---|---|
| Documento | Propuesta de colaboración — Programa Piloto de Visión Artificial |
| Preparado para | **[Nombre de la empresa]** |
| Versión | 1.0 · Julio 2026 |
| Emitido por | OPSIA — San Juan / Buenos Aires, Argentina |
| Contacto | opsia.cv@gmail.com · opsia-cv.netlify.app |
| Clasificación | Confidencial — para uso exclusivo del destinatario |

---

## 1. Resumen ejecutivo

Las operaciones mineras cuentan con infraestructura extensa de videovigilancia cuyo
potencial preventivo permanece sin explotar: el video se graba, pero no se analiza.
OPSIA incorpora una capa de inteligencia artificial sobre las cámaras existentes que
detecta, en tiempo real y sin hardware adicional, el cumplimiento de elementos de
protección personal (EPP), la presencia y tipo de maquinaria pesada, y situaciones de
proximidad riesgosa entre personas y equipos.

**Qué proponemos en concreto:** un programa piloto de cuatro semanas, acotado y de
bajo compromiso, que procesa video grabado de la propia operación y entrega un informe
de cumplimiento con evidencia trazable. El piloto no requiere integración con sistemas,
no interfiere con la operación y permite evaluar la tecnología con datos propios antes
de cualquier decisión de adopción.

**Por qué OPSIA:** tecnología de detección propia — no reventa de servicios de terceros
— entrenada sobre más de 48.000 anotaciones de entornos industriales, un equipo con
base en San Juan que conoce el territorio minero, y una política estricta de evidencia:
toda métrica presentada en este documento proviene de mediciones internas documentadas.

---

## 2. El problema operacional

**2.1. La supervisión visual humana no escala.** Un sitio minero típico opera decenas
de cámaras en portería, accesos, talleres, planta y rajo. La literatura de
videovigilancia documenta que la atención humana sostenida frente a monitores se
degrada en pocos minutos; en la práctica, el CCTV se usa de manera forense — para
reconstruir el incidente después de ocurrido — y no preventiva.

**2.2. El EPP falla en el momento menos visible.** Las referencias internacionales de
seguridad ocupacional (OSHA y literatura HSE) asocian la mayoría de los incidentes
graves con ausencia o uso incorrecto de EPP. Las recorridas y controles por muestreo
capturan una fracción mínima de las infracciones reales, y el registro manual llega
tarde y sin evidencia objetiva.

**2.3. La interacción persona–equipo es el riesgo crítico.** Los eventos de proximidad
entre personal a pie y equipo pesado en movimiento evolucionan de infracción a
incidente en segundos: ninguna cadena humana de aviso opera en esa ventana temporal.

**2.4. El costo de la brecha.** Días perdidos, investigación de incidentes, impacto en
índices de frecuencia y gravedad, primas de ART, observaciones de auditoría y — el
costo mayor — el daño a las personas. La información para prevenir gran parte de estos
eventos ya está siendo capturada por las cámaras; falta la capa que la entienda.

---

## 3. La solución OPSIA

Plataforma de análisis de video por inteligencia artificial, compuesta por tres
capacidades sobre un mismo motor de detección:

| Capacidad | Descripción | Salida operativa |
|---|---|---|
| **Cumplimiento de EPP** | Detección por trabajador de casco, chaleco reflectivo, lentes, botas y guantes, mediante cruce geométrico persona–elemento. | Estado SEGURO / INSEGURO / REVISAR por persona; índice de cumplimiento por zona, turno y contratista. |
| **Maquinaria y proximidad** | Reconocimiento de camionetas, volquetes, excavadoras, retroexcavadoras, motoniveladoras, rodillos y cisternas; radios de riesgo configurables. | Alertas de proximidad persona–equipo; control de ingreso vehicular a zonas restringidas. |
| **Evidencia y reporte** | Registro de cada evento con imagen, marca de tiempo, cámara y zona. | Reportes exportables por período, área o contratista, aptos para auditoría interna y externa. |

**Principios de diseño:**

- **Sin hardware nuevo:** integración por protocolos estándar (RTSP/ONVIF) con el CCTV
  existente.
- **Latencia operativa:** de la cámara a la alerta en menos de dos segundos en
  modalidad de monitoreo continuo.
- **Privacidad por diseño:** el sistema no realiza reconocimiento facial ni
  identificación de individuos; detecta condiciones de seguridad, no identidades.
  Difuminado de rostros configurable en reportes.

---

## 4. Seguridad de la información y despliegue

Sección dirigida a las áreas de Sistemas y Seguridad de la Información.

- **Modalidades de despliegue:** (a) procesamiento en infraestructura del cliente
  (on-premise, opción recomendada para faena), (b) nube privada del cliente, o
  (c) nube gestionada por OPSIA. En la modalidad on-premise, **el video no abandona
  la red de la operación** en ningún momento.
- **Datos tratados:** flujos de video de cámaras designadas y metadatos de detección
  (clase, coordenadas, tiempo, cámara). No se procesan datos biométricos ni se
  construyen perfiles de individuos.
- **Retención:** configurable según política del cliente; por defecto se conservan
  únicamente los recortes de evidencia asociados a eventos, no el video continuo.
- **Marco normativo:** tratamiento de datos conforme a la Ley 25.326 de Protección de
  Datos Personales; el enfoque del sistema es compatible con los principios de la
  legislación de higiene y seguridad aplicable a la actividad minera (Ley 19.587,
  Dto. 249/07) y con sistemas de gestión ISO 45001, a los que aporta registro objetivo
  y trazable.
- **Confidencialidad:** OPSIA suscribe acuerdos de confidencialidad (NDA) previos a la
  recepción de cualquier material del cliente. El uso de video del cliente para mejora
  de modelos sólo procede con autorización expresa y por escrito.

---

## 5. Programa piloto propuesto

Diseñado para evaluar la tecnología con datos reales de la operación, con esfuerzo
mínimo del cliente y sin integración con sistemas productivos.

**5.1. Alcance**

| Parámetro | Definición |
|---|---|
| Duración | 4 semanas desde la recepción del material |
| Insumo requerido | 8 a 16 horas de video grabado de 3 a 5 cámaras designadas por el cliente (accesos, portería, zonas de tránsito persona–equipo) |
| Procesamiento | Análisis fuera de línea en infraestructura de OPSIA o del cliente, a elección |
| Interferencia con la operación | Ninguna |
| Costo | Bonificado — el piloto es la instancia de validación mutua |

**5.2. Cronograma**

| Semana | Actividad |
|---|---|
| 1 | Firma de NDA · recepción de material · calibración por cámara |
| 2–3 | Procesamiento, control de calidad de detecciones y análisis |
| 4 | Entrega del informe · presentación de resultados al equipo HSE · propuesta de siguiente etapa |

**5.3. Entregables**

1. **Informe de cumplimiento EPP** sobre el período analizado: índice general y
   desagregado por cámara/zona, con distribución horaria.
2. **Registro de eventos de proximidad** persona–equipo detectados, con evidencia
   (imagen y marca de tiempo de cada evento).
3. **Galería de evidencia** de infracciones representativas, apta para uso en
   capacitación interna.
4. **Evaluación técnica de cobertura:** qué detecta el sistema en las condiciones
   reales de las cámaras del cliente (iluminación, ángulos, distancia) y qué
   requeriría ajuste.
5. **Propuesta dimensionada** para una eventual etapa de monitoreo continuo, con
   alcance y costos basados en los datos relevados.

**5.4. Criterios de éxito** — acordados en el inicio; propuesta base:

- Detección correcta de personas y EPP verificada por muestreo conjunto con el equipo
  HSE del cliente sobre un subconjunto de eventos.
- Identificación de al menos un patrón operativo accionable (franja horaria, zona o
  dinámica de incumplimiento) no evidente para la supervisión actual.
- Informe entregado dentro del plazo comprometido.

---

## 6. Hoja de ruta del servicio

| Etapa | Servicio | Descripción |
|---|---|---|
| 1 | **Auditoría** (este piloto) | Análisis de video grabado; informe de cumplimiento en 72 h una vez calibrado el sitio. |
| 2 | **Monitoreo continuo** | Procesamiento en vivo, tablero operacional multi-sitio, alertas en tiempo real al equipo HSE, reportes por turno y contratista. |
| 3 | **Enterprise** | Integración con sistemas HSE corporativos, SSO, SLA dedicado, procesamiento on-premise y modelos entrenados a medida del uniforme y los procedimientos de la compañía. |

El cliente avanza de etapa únicamente cuando los resultados de la anterior lo
justifican. No se requieren compromisos de largo plazo para iniciar.

---

## 7. Tecnología

- **Modelos de detección propios**, entrenados sobre un corpus curado de más de
  48.000 anotaciones de entornos industriales y mineros, con pipeline documentado de
  auditoría de calidad de datos y trazabilidad completa de cada decisión de curaduría.
- **26 clases detectadas** simultáneamente por un único modelo: personas, cinco
  categorías de EPP y sus ausencias, siete tipos de vehículo industrial-minero y
  elementos de señalización.
- **Rendimiento en tiempo real** (24+ cuadros por segundo) sobre hardware de
  servidor estándar; costo operativo por cámara bajo y predecible.
- **Demostración verificable:** demostración con detecciones reales del modelo —
  sin ediciones ni montajes — presentada en la reunión de trabajo. La web
  institucional (opsia-cv.netlify.app) exhibe una simulación ilustrativa de la
  interfaz de operador, identificada como tal.
- **Mejora continua:** el sistema está diseñado para incorporar datos del sitio de
  cada cliente (previa autorización expresa), lo que incrementa la precisión sobre
  las condiciones particulares de esa operación: uniformes corporativos, flota
  específica, condiciones de luz y polvo.

Indicadores citados provenientes de evaluaciones internas documentadas sobre conjuntos
de validación independientes. La documentación técnica de respaldo está disponible
bajo NDA.

---

## 8. Quiénes somos

OPSIA es una empresa argentina de visión artificial aplicada a seguridad industrial,
fundada por un equipo de ingeniería con base en San Juan y Buenos Aires.

Dos de sus fundadores, **Emiliano Lescuras** y **Felipe Bridge**, son sanjuaninos:
crecieron en la provincia que hoy concentra el desarrollo minero más dinámico del
país y conocen de primera mano el peso económico, social y humano de la actividad.
Esa cercanía define la tesis de la empresa: la nueva generación de proyectos mineros
argentinos — con inversiones y horizontes de operación de décadas — demandará
estándares de seguridad de clase mundial, y la tecnología para sostenerlos se
construye mejor desde el territorio que desde afuera.

| Fundador | Rol | Perfil |
|---|---|---|
| **Maximiliano Lombardia** | Ingeniería y Producto | Estudiante de Ingeniería en Inteligencia Artificial (Universidad de Palermo). Software Engineer en Mercado Libre desde hace cuatro años, con experiencia en sistemas de gran escala: arquitectura, confiabilidad y operación de software en producción. Base: Buenos Aires. |
| **Felipe Bridge** | Operaciones y Comercial | Estudiante de Ingeniería en Inteligencia Artificial (Universidad de Palermo), con varios años de experiencia profesional como AI Engineer en soluciones aplicadas de machine learning. Sanjuanino; lidera la relación con clientes y el desarrollo de negocio en la región. Base: San Juan. |
| **Emiliano Lescuras** | Machine Learning y Datos | Estudiante de Ingeniería en Data Science (Universidad de Palermo), con experiencia profesional y proyectos propios de visión por computadora de punta a punta. Responsable de los modelos de detección y del pipeline de datos de OPSIA. Sanjuanino. Base: San Juan. |

**Nuestra regla de trabajo:** ninguna afirmación sin evidencia. Las métricas se miden,
las demostraciones son salidas reales del modelo y lo que aún está en desarrollo se
comunica como tal.

---

## 9. Preguntas frecuentes

**¿Sirven nuestras cámaras actuales?** En general, sí: el sistema se integra con la
mayoría de las cámaras IP mediante RTSP u ONVIF. El piloto incluye la evaluación de
aptitud de las cámaras designadas.

**¿Dónde se procesa el video?** A elección del cliente: en su infraestructura
(recomendado), en su nube o en la de OPSIA. Para el piloto alcanza con la entrega de
archivos de video grabado.

**¿El sistema identifica personas?** No. Detecta condiciones de seguridad (presencia
de EPP, proximidad a equipos), no identidades. No hay reconocimiento facial.

**¿Funciona de noche, con polvo o lluvia?** Los modelos se entrenan con condiciones
industriales adversas. El piloto es precisamente la instancia para medir el desempeño
en las condiciones reales de cada cámara, y así lo informamos: con datos, no con
promesas.

**¿Qué necesita OPSIA de nuestra parte para empezar?** Un referente del área HSE,
la firma del NDA y el material de video descrito en 5.1. Nada más.

---

## 10. Próximo paso

Proponemos una reunión de trabajo de 30 minutos con el área de Seguridad e Higiene
para presentar la demostración, relevar las condiciones del sitio y, de existir
interés, dejar acordado el alcance del piloto en esa misma instancia.

**OPSIA**
opsia.cv@gmail.com · opsia-cv.netlify.app
San Juan · Buenos Aires — Argentina

*Este documento es confidencial y ha sido preparado exclusivamente para su
destinatario. Su contenido no constituye asesoramiento legal ni compromiso
contractual; los alcances definitivos se establecen en la propuesta de servicios
correspondiente.*
