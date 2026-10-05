# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/). Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Pendiente para v0.5.0
- Modelo predictivo de probabilidad de cierre (dataset constructora, 4000 filas).
- Integración de predicción en la UI de cotización.
- Despliegue en Streamlit Community Cloud.

## [v0.4.0] — Módulo PDF aislado (Semana 10)

### Agregado
- Módulo `core/pdf_generator.py` con la función pura `generar_pdf()`, sin dependencia de Streamlit ni de `app.py`.
- Suite de tests `tests/test_pdf_generator.py` con 8 casos (TC-P01 a TC-P08): tipo de retorno, tamaño mínimo, firma PDF, variación por cliente, variación por total, PDFs distintos entre sí, distancia 0 y m² mínimo.

### Cambiado
- `app.py` elimina la función `generar_pdf()` inline y la reemplaza por el import de `core.pdf_generator`.
- `app.py` elimina los imports directos de `fpdf` y `datetime` (ahora encapsulados en el módulo).

## [v0.3.0] — Persistencia del histórico (Semana 8-9)

### Agregado
- Módulo `core/historico.py` con las funciones `guardar_cotizacion()` y `leer_historico()`.
- Persistencia automática de cada cotización generada en `data/historico.csv`.
- Sección "📋 Histórico de Cotizaciones" en la interfaz: tabla con las últimas 10 cotizaciones.
- Suite de tests `tests/test_historico.py` con 8 casos (TC-H01 a TC-H08): creación de archivo, encabezado, acumulación de filas, integridad de datos, histórico vacío, filtro `ultimas`, validación de campos obligatorios y fecha automática.

### Cambiado
- `app.py` llama a `guardar_cotizacion()` tras cada presupuesto calculado exitosamente.
- `[Unreleased]` actualizado: se mueven las tareas completadas a esta versión.

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
