# OPSIA — Visión Artificial para Operaciones Seguras

**Documento institucional y comercial · Julio 2026 · Confidencial**
Contacto: opsia.cv@gmail.com · opsia-cv.netlify.app · San Juan / Buenos Aires, Argentina

---

## 1. Resumen ejecutivo

OPSIA convierte las cámaras que las empresas industriales **ya tienen instaladas** en un
sistema de monitoreo inteligente de seguridad: detección de elementos de protección
personal (EPP), reconocimiento de maquinaria pesada y alertas de proximidad
persona–vehículo, en tiempo real y sin hardware nuevo.

Nacimos en San Juan — el corazón de la minería argentina — con una convicción simple:
**la seguridad de un operario no puede depender de cuántos monitores alcanza a mirar un
supervisor.** Un sitio industrial promedio opera más de 40 cámaras; la atención humana
sostenida sobre monitores cae a los pocos minutos. Las cámaras ya ven todo. Nosotros
hacemos que entiendan.

Hoy contamos con **tecnología propia funcionando**: modelos de detección entrenados y
validados sobre más de 48.000 anotaciones de entornos industriales reales, capaces de
detectar simultáneamente personas, casco, chaleco reflectivo, botas, lentes, guantes y
siete tipos de vehículo minero. Buscamos **2 o 3 operaciones para un programa piloto**
que valide el sistema sobre video real de sus sitios.

---

## 2. Quiénes somos y de dónde venimos

OPSIA la fundamos tres estudiantes de ingeniería de la Universidad de Palermo que nos
conocimos compartiendo la misma obsesión: aplicar inteligencia artificial a problemas
del mundo físico, no solo a pantallas.

**Emiliano Lescuras y Felipe Bridge son sanjuaninos.** Crecieron viendo cómo la minería
se convertía en el motor económico de su provincia: Veladero, Gualcamayo, y ahora la
nueva ola de proyectos de cobre que posiciona a San Juan como uno de los distritos
mineros más importantes de Sudamérica para las próximas décadas. Para ellos la minería
nunca fue una industria lejana — es la industria de su tierra, y vieron en ella un
negocio extraordinario a largo plazo: una actividad en plena expansión, con inversiones
de décadas, estándares de seguridad cada vez más exigentes y una adopción tecnológica
que recién comienza. **Donde otros ven camiones y polvo, ellos vieron datos sin
explotar y vidas que proteger.**

**Maximiliano Lombardia** aporta la otra mitad de la ecuación: la experiencia de
construir software que funciona a escala real, forjada en años de trabajo en una de las
empresas tecnológicas más grandes de Latinoamérica.

La combinación define a OPSIA: conocimiento del territorio minero, ingeniería de IA de
primer nivel y disciplina de software industrial.

---

## 3. El problema

Las operaciones industriales invirtieron millones en infraestructura de cámaras — y ese
video, en su enorme mayoría, **nadie lo mira**.

- **60% de los incidentes graves** involucran EPP ausente o incorrecto (referencias
  OSHA / literatura HSE).
- **Una infracción de proximidad se convierte en incidente en segundos** — mucho menos
  de lo que tarda cualquier supervisión humana en reaccionar.
- **Más de 40 cámaras por sitio** es la norma; la atención humana sostenida frente a
  monitores se degrada a los pocos minutos. La supervisión visual continua, con
  personas, es materialmente imposible.
- El registro de cumplimiento (para auditorías, ART, contratistas) se construye a mano,
  con planillas y recorridas — costoso, incompleto y siempre después de los hechos.

El resultado: la seguridad depende de la suerte y de muestreos. El video que podría
prevenir el próximo incidente ya existe — pero es ciego.

---

## 4. La solución OPSIA

Tres capas de inteligencia sobre las cámaras que ya operan:

**① Cumplimiento de EPP, persona por persona.**
Detección de casco, chaleco reflectivo, lentes, botas, guantes y protección auditiva.
Estado SEGURO / INSEGURO / REVISAR por trabajador, calculado cruzando geométricamente
cada persona con los elementos detectados.

**② Maquinaria y proximidad.**
Reconocimiento de camionetas, volquetes, excavadoras, retroexcavadoras, motoniveladoras,
rodillos y cisternas. Alertas cuando una persona entra al radio de riesgo de un equipo
en movimiento, y control de acceso vehicular a zonas restringidas.

**③ Evidencia y reportes.**
Cada infracción queda registrada con frame, hora y zona. Reportes de cumplimiento por
turno, área o contratista, exportables y listos para auditoría.

**Principios de diseño:**
- **Cero hardware nuevo:** integración por RTSP/ONVIF con el CCTV existente.
- **Privacidad por diseño:** sin reconocimiento facial de identidad; procesamiento
  on-premise disponible — el video puede no salir nunca de la infraestructura del
  cliente; difuminado de rostros configurable en reportes.
- **De la cámara a la alerta en menos de dos segundos.**

---

## 5. Tecnología propia (no un envoltorio de APIs)

- Modelos de detección **entrenados por nosotros** sobre un corpus curado de más de
  **48.000 anotaciones** de entornos industriales reales, con pipeline propio de
  auditoría de datos, limpieza y trazabilidad (cada dato descartado queda registrado
  con su motivo).
- **26 clases** detectadas simultáneamente: personas, 5 categorías de EPP y sus
  ausencias, 7 tipos de vehículo industrial-minero y auxiliares de señalización.
- Demostración con **detecciones reales del modelo** (no montajes) sobre video de
  referencia de mina a cielo abierto — se presenta en reunión; la web institucional
  exhibe una simulación de interfaz identificada como tal.
- Inferencia eficiente: el modelo corre en tiempo real (24+ FPS) y puede desplegarse
  en servidores modestos del cliente — el costo operativo por cámara es bajo y
  predecible.
- Roadmap técnico definido y honesto: ampliación del corpus con datos de sitio de cada
  cliente (con consentimiento), detección de protección auditiva y uniforme
  corporativo a medida, y modelos específicos por operación en el plan Enterprise.

---

## 6. Cómo trabajamos con un cliente

**Cómo empezamos — sin fricción:**
① Llamada de 30 minutos → ② Auditoría piloto sobre video de SU operación →
③ Propuesta con números reales de su sitio.

| Servicio | Qué incluye | Para quién |
|---|---|---|
| **Auditoría** | Análisis de video grabado. Reporte de cumplimiento y hallazgos en 72 h. Sin integración en tiempo real. | El punto de partida ideal: valor concreto en días, sin tocar la operación. |
| **Monitoreo continuo** | Procesamiento en vivo, dashboard operacional multi-sitio y alertas en el momento para el equipo HSE. Reportes por turno y contratista. | Operaciones que quieren pasar de auditar a prevenir. |
| **Enterprise** | Integración con sistemas HSE existentes, SSO, SLA dedicado, procesamiento on-premise y modelos a medida del uniforme y procedimientos de la empresa. | Compañías multi-sitio con requisitos corporativos. |

---

## 7. Mercado y visión de largo plazo

La ventana de oportunidad es excepcional y tiene décadas por delante:

- **San Juan y la nueva minería argentina.** La cartera de proyectos de cobre en
  desarrollo (San Juan, Mendoza, Salta, Jujuy) implica inversiones de decenas de miles
  de millones de dólares y décadas de operación — cada una con cientos de cámaras y
  estándares de seguridad de clase mundial que cumplir. Cobertura inicial de OPSIA:
  San Juan · Mendoza · Salta · Jujuy · Neuquén · Río Negro · Buenos Aires.
- **Regulación y presión social crecientes** sobre seguridad laboral: el cumplimiento
  verificable deja de ser un diferencial y pasa a ser una exigencia.
- **El mismo motor sirve a industrias adyacentes:** construcción, oil & gas y otras
  operaciones pesadas comparten el problema y la solución — las reglas cambian, el
  modelo no.
- **Ventaja del local:** somos de acá. Entendemos la operación, el idioma, los tiempos
  y la realidad de las empresas de la región — y estamos a un auto de distancia del
  sitio, no a un océano.

La visión: ser la capa de visión artificial estándar de la industria pesada del país,
empezando por la minería sanjuanina y creciendo con ella.

---

## 8. El equipo

**Maximiliano Lombardia — Co-fundador · Ingeniería & Producto**
Estudiante de Ingeniería en Inteligencia Artificial (Universidad de Palermo). Software
Engineer en **Mercado Libre desde hace 4 años**, donde construye sistemas que atienden a
millones de usuarios: esa disciplina de ingeniería a escala — código confiable,
monitoreo, arquitectura — es la que aplica a la plataforma OPSIA. Perfil técnico sólido
con fuertes habilidades de comunicación y trabajo en equipo. Base: Buenos Aires.

**Felipe Bridge — Co-fundador · Operaciones & Comercial**
Estudiante de Ingeniería en Inteligencia Artificial (Universidad de Palermo), con varios
años de experiencia profesional como **AI Engineer** construyendo soluciones de machine
learning aplicadas. Sanjuanino: combina el conocimiento técnico con la lectura del
territorio y de los actores de la industria minera local. Encabeza la relación con
clientes y el desarrollo de negocio. Base: San Juan.

**Emiliano Lescuras — Co-fundador · Machine Learning & Datos**
Estudiante de Ingeniería en Data Science (Universidad de Palermo), con experiencia
profesional y un historial de proyectos propios de visión por computadora de punta a
punta: curaduría de datasets industriales, entrenamiento, evaluación rigurosa y
despliegue. Es el responsable de los modelos de detección de OPSIA y del pipeline de
datos que los alimenta. Sanjuanino. Base: San Juan.

Los tres compartimos una regla que atraviesa todo lo que hacemos, del código al
marketing: **ninguna afirmación sin evidencia.** Nuestras métricas son medidas, nuestras
demos son detecciones reales del modelo, y lo que todavía no está listo se dice.

---

## 9. Estado actual y próximos pasos

**Hoy (julio 2026):**
- Modelo de detección v0.2 entrenado y validado (26 clases; EPP como objeto con
  precisión alta; vehículos mineros principales operativos).
- Pipeline completo de datos: auditoría, limpieza con trazabilidad, corpus reproducible.
- Demostración funcional con detecciones reales del modelo (material disponible para
  reuniones comerciales).
- Presencia comercial: web institucional, identidad de marca, canal de contacto.

**Próximos 6 meses:**
- **Programa piloto con 2-3 operaciones** (auditoría sobre video real del cliente) —
  el objetivo comercial central de este documento.
- Entrenamiento de la siguiente generación de modelos en GPU con corpus ampliado.
- Incorporación de protección auditiva y uniforme corporativo al alcance de detección.
- Constitución formal de la empresa y marco legal de datos (Ley 25.326 / GDPR).

**La invitación:** si su operación tiene cámaras y un compromiso serio con la seguridad,
la auditoría piloto es la forma de ver el valor con SUS datos, en 72 horas, sin
integración ni riesgo.

---

## 10. Contacto

**OPSIA — AI Vision for Mining**
📧 opsia.cv@gmail.com
🌐 opsia-cv.netlify.app
📍 San Juan · Buenos Aires — Argentina

*Documento confidencial preparado para presentación comercial. Los indicadores técnicos
citados provienen de mediciones internas documentadas; las referencias de industria
citan OSHA y literatura HSE.*
