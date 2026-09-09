# Guía de contribución

Convenciones de trabajo para el equipo Buen Codigo en el proyecto EdificaNova. Formaliza lo definido en la sección 6 del SOW.

## Ramas

- `main` — siempre estable. Refleja exactamente lo entregado en cada hito evaluado.
- `develop` — integración de features antes de pasar a `main`.
- `feature/nombre-corto` — una rama por historia de usuario o tarea concreta. Ejemplos: `feature/motor-calculo`, `feature/export-pdf`, `feature/historico-cotizaciones`.

Nunca se commitea directo a `main`. `develop` se mergea a `main` solo al cerrar un hito del cronograma.

## Flujo de trabajo

1. Crear la rama desde `develop`: `git checkout develop && git checkout -b feature/nombre-corto`
2. Trabajar y commitear siguiendo la convención de abajo.
3. Pushear la rama y abrir un Pull Request hacia `develop`.
4. Al menos un integrante de otro subequipo revisa el PR antes de mergear (aunque el equipo sea chico, esto deja registro de decisiones en los comentarios).
5. Al cerrar un hito del cronograma: `develop` → `main`, y se tagea la versión.

## Commits (Conventional Commits)

Formato: `tipo: descripción breve en infinitivo o imperativo`

| Tipo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un bug |
| `test:` | Agregar o modificar tests |
| `refactor:` | Cambio de estructura sin cambiar comportamiento |
| `docs:` | Cambios en documentación |
| `chore:` | Tareas de mantenimiento (dependencias, configuración) |

Ejemplos:
```
feat: extraer motor de cálculo a módulo testeable
test: agregar casos de valores límite para m2
fix: corregir validación de distancia negativa
docs: actualizar README con instrucciones de deploy
```

## Versionado (SemVer)

- **MAJOR** (`v1.x.x` → `v2.x.x`): cambio grande de arquitectura o alcance.
- **MINOR** (`v0.1.x` → `v0.2.x`): nueva funcionalidad completa, alineada a un hito del cronograma.
- **PATCH** (`v0.2.0` → `v0.2.1`): correcciones o ajustes menores que no agregan funcionalidad.

Cada tag se crea sobre `main`, después del merge de `develop`:

```bash
git checkout main
git merge develop
git tag -a v0.X.0 -m "Descripción breve del hito"
git push origin main --tags
```

Antes de tagear, verificar:
- [ ] Todos los tests pasan (`pytest tests/ -v`)
- [ ] `requirements.txt` está actualizado si se agregaron dependencias
- [ ] El `CHANGELOG.md` tiene la entrada correspondiente

## Issues y tablero

Cada historia de usuario o bug se carga como Issue, con:
- Título corto y descriptivo
- Criterio de aceptación (formato Dado/Cuando/Entonces)
- A qué hito/tag pertenece
- Subequipo responsable

El tablero (GitHub Projects) refleja el estado: `To do` → `In progress` → `In review` → `Done`.
