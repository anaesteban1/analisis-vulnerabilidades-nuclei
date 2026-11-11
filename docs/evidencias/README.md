# Evidencias y capturas pendientes

Este directorio conserva los resultados reales consultados para el artículo de Dev.to y sirve de guía para completar las capturas. No hay imágenes adjuntas todavía; no guardar capturas simuladas ni editar resultados para presentarlos como ejecuciones reales.

## Evidencias recopiladas

- [`render-health.json`](render-health.json): portada y `/health` observados en `https://estadosseguro.onrender.com`, ambos HTTP 200; incluye el JSON `status: ok`, hora, tipo de contenido y cabeceras de salud. Verificación del 11 de noviembre de 2026.
- [`github-actions-42974596625/`](github-actions-42974596625/): archivos descargados del artefacto oficial de la ejecución exitosa más reciente al recopilar el material del artículo, run [42974596625](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei/actions/runs/42974596625), asociada al commit `2298daa`.
  - [`nuclei.jsonl`](github-actions-42974596625/nuclei.jsonl): única coincidencia `estadosseguro-healthcheck`, severidad `info`, en localhost.
  - [`app.log`](github-actions-42974596625/app.log): arranque de Flask y solicitudes GET que recibió el escáner en el runner.
  - [`README.md`](github-actions-42974596625/README.md): procedencia, marcas de tiempo, resumen de Pytest/Nuclei y hash SHA-256 del JSONL.

El artefacto del workflow subido a GitHub tiene retención de 14 días; la copia bajo este directorio permite consultar el resultado con el repositorio. La fila `info` acredita una coincidencia del health check, no una vulnerabilidad.

## Capturas pendientes para el artículo

1. **Figura 1 — Panel de EstadoSeguro:** página principal con estado de servicios e incidencias.
2. **Figura 2 — Búsqueda, filtro y detalle:** una incidencia filtrada y su página de detalle.
3. **Figura 3 — API y health check publicados:** respuestas actuales de `/api/incidencias` y `/health`.
4. **Figura 4 — Resultado de Pytest:** comando y resumen visible `12 passed`, identificando el entorno.
5. **Figura 5 — Resultado de Nuclei:** JSONL real del run 42974596625 con el único hallazgo informativo.
6. **Figura 6 — Workflow de GitHub Actions:** run 42974596625, commit y pasos exitosos.
7. **Figura 7 — Servicio en Render:** estado real del despliegue y plan mostrado en el panel, sin exponer información privada.

Los marcadores aparecen dentro de [`docs/articulo-devto.md`](../articulo-devto.md), junto al lugar exacto donde se insertará cada figura. Guarda las imágenes finales en este directorio con nombres `figura-01.png` a `figura-07.png` y reemplaza cada marcador por la imagen correspondiente.

## Registro de cada evidencia

Al recopilarla, anota en el pie o en el artículo la fecha y hora, el entorno (local, GitHub Actions o Render), el commit asociado y el nombre del archivo. Conserva los originales. No incluyas tokens, claves, cookies ni otros secretos. Los resultados deben corresponder a la ejecución mostrada. Un JSONL sin coincidencias solo acredita que no hubo coincidencias con las plantillas seleccionadas en esa ejecución.
