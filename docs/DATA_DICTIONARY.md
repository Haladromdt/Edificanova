# Diccionario de Datos — EdificaNova

## `data/multiplicadores.json`

Tabla de costos base y multiplicadores, consumida por `core/motor_calculo.py`. Editable sin modificar el código fuente.

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| `costo_base_m2` | número (float) | Costo base de construcción por metro cuadrado, antes de multiplicadores | `280000` |
| `costo_flete_km` | número (float) | Costo logístico por kilómetro de distancia | `1500` |
| `sistema_constructivo` | objeto | Multiplicador según sistema constructivo. Claves: `E.E` (Económico), `W.F` (Wood Frame), `S.F` (Steel Frame) | `{"E.E": 1.0, "W.F": 1.15, "S.F": 1.25}` |
| `modalidad_entrega` | objeto | Multiplicador según modalidad de entrega. Claves: `OBRA GRIS`, `LLAVE EN MANO` | `{"OBRA GRIS": 1.0, "LLAVE EN MANO": 1.40}` |

**Regla de negocio:** `precio_m2_aplicado = costo_base_m2 × multiplicador_sistema × multiplicador_entrega`

**Nota abierta del equipo:** hoy este archivo vive en el repositorio (requiere commit + redeploy para actualizarse). Está en evaluación migrarlo a un archivo Excel subido desde la propia interfaz, para que el equipo comercial lo actualice sin depender de Git (ver ADR-004).

---

## Resultado del cálculo (`calcular_presupuesto()`)

Estructura que devuelve el motor de cálculo, consumida por la interfaz y por la generación de PDF.

| Campo | Tipo | Descripción |
|---|---|---|
| `precio_m2_aplicado` | float | Precio final por m² después de aplicar multiplicadores |
| `costo_construccion` | float | `m2 × precio_m2_aplicado` |
| `recargo_logistica` | float | `distancia × costo_flete_km` |
| `total` | float | `costo_construccion + recargo_logistica` |

---

## Histórico de cotizaciones (propuesto para v0.3.0 — aún no implementado)

Estructura propuesta para la tabla/registro que persistirá cada cotización generada (resuelve RF05/RD02 del documento de requerimientos).

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | entero, autoincremental | Identificador único de la cotización |
| `fecha` | fecha (ISO 8601) | Fecha de generación |
| `cliente` | texto | Nombre del cliente |
| `m2` | float | Superficie cotizada |
| `sistema_constructivo` | texto | Sistema elegido (`E.E`, `W.F`, `S.F`) |
| `modalidad_entrega` | texto | Modalidad elegida |
| `distancia_km` | float | Distancia logística ingresada |
| `total` | float | Presupuesto total generado |

**Formato de almacenamiento a definir en v0.3.0:** SQLite o CSV — ver discusión en el subequipo de Datos/Exportación antes de implementar.

---

## Inputs del formulario (interfaz, `app.py`) que no impactan el cálculo

Estos campos se capturan y se muestran en el PDF, pero **no afectan el precio calculado** — es una decisión de diseño pendiente de revisión con el equipo (ver guía de arquitectura):

- `tipologia` (AMERICANA / MINIMALISTA / CABAÑA)
- `revestimiento` (LADRILLO / PIEDRA NATURAL / MADERA)
- `ubicacion` (ciudad, usada solo como dato informativo, no para calcular distancia)
- `pago` (forma de pago consultada, informativo)
