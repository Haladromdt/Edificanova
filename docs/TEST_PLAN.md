# Plan de Testing — EdificaNova

## Objetivo

Garantizar que el motor de cálculo (la pieza más crítica del sistema, ligada directamente al pain point PP2 — riesgo de error humano en márgenes) sea correcto, reproducible y no se rompa silenciosamente al evolucionar el proyecto.

## Alcance de esta versión (v0.2.0)

Se testea de forma automatizada únicamente el motor de cálculo (`core/motor_calculo.py`), por ser una función pura, aislada de la interfaz, y por representar el mayor riesgo de negocio si falla.

No se testea todavía de forma automatizada: la interfaz de Streamlit, la generación de PDF, ni la persistencia (porque esta última aún no existe). Estos se prueban manualmente hasta que existan como módulos aislados.

## Estrategia

- **Framework:** `pytest`.
- **Tipo de test:** pruebas unitarias sobre funciones puras, sin mocks de Streamlit ni de archivos (se inyecta la tabla de multiplicadores directamente en los tests para no depender del JSON real).
- **Momento de ejecución:** antes de cada Pull Request y obligatorio antes de tagear una versión (ver `CONTRIBUTING.md`).
- **Criterio de salida:** 100% de los tests en verde antes de cualquier tag de versión.

## Casos de prueba definidos (Evidencia de Testeo de Software)

| # | Nombre | Objetivo | Estado |
|---|---|---|---|
| 1 | Cálculo correcto de presupuesto según sistema constructivo | Verificar que el motor aplique el multiplicador correcto según el sistema constructivo | ✅ Automatizado |
| 2 | Validación de campos obligatorios/inválidos | Verificar que el sistema rechace sistema, entrega, m² o distancia inválidos | ✅ Automatizado |
| 3 | Generación correcta del PDF | Verificar que el PDF exportado coincida con lo calculado | ⏳ Manual — automatizar en v0.3.0 cuando `pdf_generator.py` se extraiga como módulo aislado |
| 4 | Registro en histórico de cotizaciones | Verificar que cada cotización quede guardada con sus datos correctos | ⏳ Pendiente — depende de que exista la persistencia (v0.3.0) |
| 5 | Cálculo con valores límite | Verificar comportamiento ante m² muy bajo o muy alto | ✅ Automatizado |

## Tests adicionales de robustez (más allá de los 5 casos mínimos)

- Comparación de modalidad "Obra Gris" vs. "Llave en Mano" (la segunda debe ser siempre más cara).
- Rechazo de sistema constructivo desconocido.
- Rechazo de modalidad de entrega desconocida.
- Rechazo de distancia negativa.

## Cómo correr los tests

```bash
pytest tests/ -v
```

## Próximos pasos (v0.3.0)

1. Extraer `generar_pdf()` a `core/pdf_generator.py` y agregar el caso de prueba 3.
2. Diseñar `storage/historico.py` con una interfaz testeable (inyección de una base de datos en memoria para tests) y agregar el caso de prueba 4.
3. Evaluar tests de integración end-to-end una vez que exista el flujo completo (interfaz → cálculo → PDF → histórico).
