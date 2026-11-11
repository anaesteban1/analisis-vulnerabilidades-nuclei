# Guía para recopilar evidencias

Este directorio queda preparado para las capturas reales del artículo técnico y el video. No guardar capturas simuladas ni editar resultados para presentarlos como ejecuciones reales.

## Capturas sugeridas

1. **Aplicación local:** panel completo en el navegador mostrando servicios e incidencias.
2. **Filtros y detalle:** una búsqueda aplicada y una incidencia abierta en su página de detalle.
3. **API y salud:** respuestas reales de `/api/incidencias` y `/health` (por ejemplo, desde navegador o cliente HTTP).
4. **Pruebas:** terminal con `python -m pytest -q` y su resumen íntegro.
5. **GitHub Actions:** ejecución terminada del workflow, commit asociado y pasos con su estado visible.
6. **Artefacto Nuclei:** página de artefactos del run y contenido descargado de `nuclei.jsonl`; describir exactamente lo que muestre esa ejecución.
7. **Render:** Blueprint/servicio creado por el usuario, configuración de auto despliegue y estado real del health check, solo después de conectarlo.

## Registro de cada evidencia

Al recopilarla, anota en el pie o en el artículo la fecha y hora, el entorno (local, GitHub Actions o Render), el commit asociado y el nombre del archivo. Conserva los originales. No incluyas tokens, claves, cookies ni otros secretos. Los resultados deben corresponder a la ejecución mostrada; un archivo vacío de Nuclei solo acredita que no hubo coincidencias con las plantillas seleccionadas en esa ejecución.
