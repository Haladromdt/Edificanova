# EdificaNova

Sistema de cotización automatizada y generación de presupuestos para una empresa constructora. Digitaliza un proceso que hoy se hace a mano, reduciendo el tiempo de respuesta al cliente y el riesgo de error humano en el cálculo de márgenes.

**Equipo:** Buen Codigo — Práctica Profesionalizante, Comisión B.1, ISPC.
**Versión actual:** v0.2.0 — ver [CHANGELOG.md](./CHANGELOG.md).

## Qué resuelve

El proceso manual de cotización tarda entre 45 y 60 minutos y tiene riesgo de error humano en el cálculo. EdificaNova lo reduce a menos de un minuto, aplicando reglas de negocio de forma consistente y exportando un presupuesto en PDF.

Ver el detalle de requerimientos y pain points en [`docs/EA1_Documento_Requerimientos.docx`](./docs/) y el alcance completo del proyecto en [`docs/SOW.docx`](./docs/).

## Estructura del proyecto

```
edificanova/
├── app.py                      # Interfaz web (Streamlit) — solo captura y muestra, no calcula
├── core/
│   └── motor_calculo.py        # Lógica de negocio pura, testeada de forma aislada
├── data/
│   └── multiplicadores.json    # Tabla de costos y multiplicadores, editable sin tocar código
├── tests/
│   └── test_motor_calculo.py   # Suite de tests con pytest
├── docs/                       # Documentación del proyecto (este paquete)
├── assets/                     # Material de presentación / defensa
├── requirements.txt
└── README.md
```

## Cómo correrlo

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Se abre en `http://localhost:8501`.

## Cómo correr los tests

Desde la raíz del proyecto (no desde `tests/`):

```bash
pytest tests/ -v
```

## Documentación del proyecto

| Documento | Contenido |
|---|---|
| [`docs/SOW.docx`](./docs/) | Alcance, cronograma, roles, versionado, roadmap |
| [`docs/EA1_Documento_Requerimientos.docx`](./docs/) | Requerimientos funcionales, no funcionales, de datos |
| [`docs/adr/`](./docs/adr/) | Por qué se tomó cada decisión técnica clave |
| [`docs/TEST_PLAN.md`](./docs/TEST_PLAN.md) | Estrategia y casos de prueba |
| [`docs/DATA_DICTIONARY.md`](./docs/DATA_DICTIONARY.md) | Estructura de los datos del sistema |
| [`docs/DEPLOYMENT.md`](./docs/DEPLOYMENT.md) | Cómo desplegar y hacer rollback |
| [`docs/RISK_REGISTER.xlsx`](./docs/) | Seguimiento vivo de riesgos |
| [`docs/MANUAL_DE_USUARIO.docx`](./docs/) | Guía para el equipo comercial |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Convenciones de ramas, commits y versionado |
| [`CHANGELOG.md`](./CHANGELOG.md) | Historial de versiones |

## Estado actual

- ✅ Motor de cálculo aislado y testeado (8 tests, v0.2.0)
- ✅ Tabla de multiplicadores externalizada (JSON)
- ✅ Exportación a PDF
- ⏳ Persistencia del histórico de cotizaciones (v0.3.0)
- ⏳ Deploy público (v0.3.0)
