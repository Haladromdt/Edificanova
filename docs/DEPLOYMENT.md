# Runbook de Despliegue — EdificaNova

Alcance: despliegue en **Streamlit Community Cloud**, plataforma definida para el sistema evaluado en Práctica Profesionalizante (ver ADR-005). No aplica a la visión de producto a futuro (que contempla otro stack de frontend).

## Prerrequisitos

- [ ] Repositorio en GitHub, rama `main` actualizada con el tag que se va a desplegar.
- [ ] `requirements.txt` en la raíz del proyecto, con todas las dependencias necesarias.
- [ ] Cuenta en [share.streamlit.io](https://share.streamlit.io) vinculada al repositorio de GitHub del equipo.
- [ ] Todos los tests en verde (`pytest tests/ -v`) sobre el commit que se va a desplegar.

## Pasos para desplegar

1. Verificar que `main` esté al día con el tag correspondiente:
   ```bash
   git checkout main
   git pull origin main
   git log --oneline -1   # confirmar que corresponde al tag esperado
   ```
2. Ingresar a [share.streamlit.io](https://share.streamlit.io) con la cuenta del equipo.
3. Crear una nueva app (o seleccionar la existente si ya fue desplegada antes):
   - Repositorio: el del equipo.
   - Branch: `main`.
   - Archivo principal: `app.py`.
4. Streamlit Cloud instala automáticamente las dependencias de `requirements.txt` y levanta la app.
5. Verificar manualmente después del deploy:
   - [ ] La app carga sin errores.
   - [ ] Se puede generar una cotización de prueba de punta a punta.
   - [ ] El PDF se descarga correctamente.
6. Compartir la URL pública generada con el equipo y documentarla en el README.

## Actualizar un deploy existente

Streamlit Community Cloud redeploya automáticamente ante cada push a `main`. Para forzar un redeploy manual (por ejemplo, si cambió solo `data/multiplicadores.json`):

1. Ir al panel de la app en Streamlit Cloud.
2. "Reboot app" desde el menú de la aplicación.

## Rollback (si algo sale mal después de un deploy)

1. Identificar el último tag estable anterior:
   ```bash
   git tag --list
   ```
2. Revertir `main` a ese tag:
   ```bash
   git checkout main
   git reset --hard vX.Y.Z   # tag estable anterior
   git push origin main --force
   ```
3. Reboot manual de la app en Streamlit Cloud (paso anterior).
4. Documentar el incidente: qué falló, en qué tag, y crear un Issue para el fix antes de re-intentar el deploy.

**Importante:** `--force` reescribe el historial de `main`. Usar solo en coordinación con todo el equipo, nunca sin avisar.

## Checklist previo a cada deploy (copiar en el Issue/PR de deploy)

- [ ] Tests en verde
- [ ] `requirements.txt` actualizado
- [ ] `CHANGELOG.md` actualizado con la nueva versión
- [ ] Tag de Git creado sobre `main`
- [ ] Verificación manual post-deploy (paso 5) completada
