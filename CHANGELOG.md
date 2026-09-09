# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/). Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Pendiente para v0.3.0
- Persistencia del histórico de cotizaciones.
- Extracción de `generar_pdf()` a módulo aislado (`core/pdf_generator.py`).
- Despliegue en Streamlit Community Cloud.

## [v0.2.0] — Motor de cálculo (Semana 5-7)

### Agregado
- Módulo `core/motor_calculo.py` con la función pura `calcular_presupuesto()`, sin dependencia de Streamlit.
- Tabla de multiplicadores externalizada en `data/multiplicadores.json` (antes hardcodeada en el código).
- Suite de tests con `pytest` (8 tests): cálculo por sistema constructivo, comparación de modalidades de entrega, validación de inputs inválidos, valores límite.
- Manejo de errores en la interfaz ante datos inválidos (`st.error` en vez de excepción sin capturar).

### Cambiado
- `app.py` ahora importa y usa `calcular_presupuesto()` en vez de calcular el presupuesto de forma inline.

## [v0.1.0] — Esqueleto funcional (Semana 3-4)

### Agregado
- Interfaz de Streamlit con formulario de datos del cliente y especificaciones del proyecto.
- Cálculo inicial de presupuesto (inline, sin separación de módulos todavía).
- Exportación básica a PDF con FPDF.
- Estructura de ramas `main`/`develop` y tablero de Issues.

## [v0.0.0] — Requerimientos y arquitectura (Semana 1-2)

### Agregado
- Documento de requerimientos (EA1): funcionales, no funcionales, de datos, trazados a pain points.
- Diagrama de arquitectura de alto nivel.
- Justificación de decisiones técnicas iniciales.
