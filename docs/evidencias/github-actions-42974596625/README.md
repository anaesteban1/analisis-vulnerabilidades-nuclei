# Procedencia de la evidencia de GitHub Actions

- Workflow: `Pruebas y análisis de seguridad`
- Run: [42974596625](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei/actions/runs/42974596625)
- Job: `quality-and-security` — [ver job](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei/actions/runs/42974596625/job/130370614191)
- Conclusión: `success`
- Commit: `2298daa1dea042ea38900316747fe8b459b2b534`
- Inicio del run: `2026-11-11 06:44:54 UTC`
- Final del job: `2026-11-11 06:48:13 UTC`
- Aplicación escaneada: `http://127.0.0.1:5000`
- Plataforma observada: GitHub-hosted runner Ubuntu 26.04; Python 3.12.16.

## Resultados registrados

- Pytest: `12 passed in 0.11s` según el log del run.
- Nuclei: v3.11.1; dos plantillas cargadas; un objetivo; dos conexiones HTTP; una coincidencia en 18.377919 ms.
- Coincidencia en `nuclei.jsonl`: `estadosseguro-healthcheck`, severidad `info`, URL coincidente `http://127.0.0.1:5000/health`.
- La comprobación `estadosseguro-missing-security-headers` no produjo coincidencia en este run.
- SHA-256 de `nuclei.jsonl`: `4eee0249d9ea63a44e9090774753a3ce054eace501539cb2223eb35163323bbb`.

## Archivos

- `nuclei.jsonl`: copia del reporte descargado del artefacto `resultados-nuclei`.
- `app.log`: copia del log de Flask incluido en el mismo artefacto. Registra `/health` y `/` consultados desde el runner.

Esta carpeta contiene los archivos devueltos por el run, excepto `app.pid`, que se omitió porque es un dato temporal del proceso sin valor como evidencia técnica. No se generaron capturas para esta ejecución.
