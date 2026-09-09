# Registro de Decisiones de Arquitectura (ADR)

Cada ADR documenta una decisión técnica: el contexto, qué se decidió, qué se descartó y por qué. Sirve para que nadie tenga que reconstruir el razonamiento meses después — incluido en la defensa final.

---

## ADR-001: Streamlit como interfaz web

**Estado:** Aceptado (Semana 1)

**Contexto:** El sistema necesita una interfaz web accesible para que el equipo comercial ingrese datos y reciba un presupuesto, dentro de un cronograma de 3 meses con 6 estudiantes.

**Decisión:** Usar Streamlit para la interfaz.

**Por qué:** Permite construir una aplicación web funcional en Python puro, sin necesidad de un desarrollo frontend separado (HTML/CSS/JS), priorizando velocidad de entrega dado el tiempo disponible.

**Alternativas descartadas:** React + Node.js — descartado por la complejidad y el tiempo de desarrollo que insumiría, innecesario para una herramienta comercial interna en esta etapa.

**Consecuencias:** Menor personalización visual que un frontend a medida. Limita las opciones de deploy (ver ADR-005).

---

## ADR-002: Motor de reglas explícito en vez de Machine Learning

**Estado:** Aceptado (Semana 1)

**Contexto:** El cálculo del presupuesto podría abordarse con un modelo predictivo entrenado sobre datos históricos, o con reglas de negocio explícitas.

**Decisión:** Implementar el cálculo como reglas y multiplicadores explícitos.

**Por qué:** Los datos históricos disponibles todavía no alcanzan en volumen ni calidad para entrenar un modelo confiable. Un motor de reglas es además reproducible y auditable, lo cual es un requerimiento no funcional del sistema (RNF03).

**Alternativas descartadas:** Modelo de Machine Learning — queda planteado como evolución futura, condicionado a tener más datos históricos limpios.

**Consecuencias:** El sistema no aprende ni mejora solo; cualquier ajuste de precios requiere editar la tabla de multiplicadores (ver ADR-004).

---

## ADR-003: FPDF para la exportación de presupuestos

**Estado:** Aceptado (Semana 1)

**Contexto:** El presupuesto final debe entregarse al cliente en un formato profesional y descargable.

**Decisión:** Usar la librería FPDF (Python) para generar el PDF.

**Por qué:** Es liviana, no requiere servicios externos y se integra directo en el motor Python sin dependencias de infraestructura adicionales.

**Alternativas descartadas:** Herramientas externas de generación de documentos (por ejemplo, servicios de terceros vía API) — hubieran agregado una dependencia de infraestructura innecesaria para un MVP.

**Consecuencias:** El diseño del PDF es más limitado que con un motor de plantillas HTML-a-PDF; suficiente para el alcance actual.

---

## ADR-004: Tabla de multiplicadores externalizada (JSON, no hardcodeada)

**Estado:** Aceptado (Semana 5)

**Contexto:** Los costos base y multiplicadores de precio cambian con el tiempo y no deberían requerir modificar el código fuente para actualizarse.

**Decisión:** Externalizar los valores a `data/multiplicadores.json`, leído por el motor de cálculo en cada ejecución.

**Por qué:** Permite versionar los cambios de precios de forma independiente del código, y es un primer paso hacia que el equipo comercial pueda ajustar valores sin depender de un redeploy completo.

**Alternativas descartadas:** Mantener los valores hardcodeados en `motor_calculo.py` — descartado porque viola el requerimiento de datos RD01 (tabla editable) y dificulta el mantenimiento.

**Consecuencias:** Hoy el archivo sigue viviendo en el repositorio: cambiarlo todavía requiere un commit y un redeploy. Evaluar en v0.3.0/v0.4.0 si se migra a una fuente editable desde la propia interfaz (ver conversación de equipo sobre alimentar la tabla desde Excel).

---

## ADR-005: Streamlit Community Cloud como plataforma de deploy (alcance evaluado)

**Estado:** Aceptado (Semana 1) — **distinto de la visión de producto a futuro**

**Contexto:** El sistema necesita estar accesible vía web para el equipo comercial, dentro del alcance evaluado en Práctica Profesionalizante.

**Decisión:** Desplegar en Streamlit Community Cloud.

**Por qué:** Es gratuito, se integra directo con el repositorio de GitHub, y es compatible de forma nativa con aplicaciones Streamlit (proceso persistente con WebSocket).

**Alternativas descartadas:** Netlify — **no es técnicamente compatible con Streamlit** para el alcance evaluado: Netlify está pensado para sitios estáticos y funciones serverless de corta duración, no para procesos persistentes con conexión WebSocket abierta, que es lo que Streamlit requiere.

**Nota importante:** El documento de visión de producto a futuro (SOW, sección 9) menciona Netlify como plataforma de deploy de la versión final. Esa decisión corresponde a un escenario donde el frontend deja de ser Streamlit — no es aplicable al sistema actual. Este ADR documenta la decisión vigente para el alcance evaluado; cualquier cambio de framework de frontend en el futuro debería registrarse como un nuevo ADR.

**Consecuencias:** El deploy queda atado a las limitaciones de Streamlit Community Cloud (recursos compartidos, sin garantías de SLA). Suficiente para el alcance de esta materia.
