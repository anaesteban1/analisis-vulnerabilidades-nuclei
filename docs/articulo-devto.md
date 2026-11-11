---
title: "EstadoSeguro: análisis web seguro con Nuclei, GitHub Actions y Render"
published: false
description: "Un caso práctico de DevSecOps con Flask: pruebas automatizadas, dos comprobaciones HTTP controladas con Nuclei y despliegue gratuito en Render."
tags: python, flask, devsecops, security
---

# EstadoSeguro: análisis web seguro con Nuclei, GitHub Actions y Render

¿Cómo se puede integrar un análisis web automatizado en un proyecto pequeño sin convertir el pipeline en un escaneo indiscriminado? En EstadoSeguro respondimos esa pregunta con un panel Flask de incidencias de servicios, una suite de Pytest y dos plantillas HTTP propias de Nuclei ejecutadas contra una instancia temporal en `127.0.0.1`.

El proyecto forma parte de un trabajo universitario del curso de Calidad de Software. Su propósito es mostrar un flujo que cualquiera pueda revisar: código y pruebas en GitHub, comprobaciones de seguridad reproducibles y un servicio desplegado en Render. Los resultados que aparecen aquí corresponden a ejecuciones verificables; el alcance del escaneo se describe junto con sus límites.

**Repositorio:** [anaesteban1/analisis-vulnerabilidades-nuclei](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei)  
**Aplicación:** [estadosseguro.onrender.com](https://estadosseguro.onrender.com/)  
**Workflow:** [última ejecución exitosa de GitHub Actions](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei/actions/runs/42974596625)

<!-- CAPTURA PENDIENTE: Figura 1. Insertarla aquí, al terminar la introducción. -->
> **Captura pendiente — Figura 1: Panel de EstadoSeguro.** Insertar una captura real de la página principal donde se vean el estado de servicios y algunas incidencias de demostración. Evitar mostrar datos del navegador que no aporten al artículo.

*Figura 1. Panel principal de EstadoSeguro con los servicios e incidencias de demostración.*

## El proyecto y su superficie de prueba

EstadoSeguro es una aplicación Flask sin base de datos ni servicios externos en tiempo de ejecución. Utiliza datos locales de demostración y ofrece una interfaz responsive en español. Desde el panel se pueden buscar incidencias, filtrarlas por estado y abrir la vista detallada.

Las rutas principales son:

| Ruta | Uso |
| --- | --- |
| `/` | Panel de servicios, incidencias, búsqueda y filtro por estado. |
| `/incidencias/<id>` | Vista detallada de una incidencia. |
| `/api/incidencias` | Consulta JSON; admite `q` y `estado`. |
| `/api/incidencias/<id>` | Consulta JSON de una incidencia. |
| `/health` | Verificación de disponibilidad, devuelve estado `ok`. |

Los parámetros de búsqueda están acotados: `q` admite hasta 100 caracteres y `estado` se valida contra una lista permitida. Las respuestas de error de la API son JSON; las páginas HTML usan plantillas Jinja. El servidor añade Content Security Policy, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` y `Permissions-Policy`. La configuración desactiva debug por defecto y toma `SECRET_KEY` del entorno.

La aplicación publicada respondió HTTP 200 en la portada y en `/health`. La evidencia JSON de la revisión de salud registra el cuerpo `{"servicio":"EstadoSeguro","status":"ok"}` y la fecha y hora de observación: `docs/evidencias/render-health.json`.

<!-- CAPTURA PENDIENTE: Figura 2. Insertarla después de la tabla de rutas. -->
> **Captura pendiente — Figura 2: Búsqueda, filtro y detalle.** Insertar una captura real de una incidencia filtrada y otra de su vista detallada. Puede ser un montaje de dos capturas propias, identificando cada estado sin alterar el contenido.

*Figura 2. Búsqueda y filtrado de incidencias, junto con la vista de detalle.*

<!-- CAPTURA PENDIENTE: Figura 3. Insertarla aquí, después del resultado de salud desplegado. -->
> **Captura pendiente — Figura 3: API y health check publicados.** Insertar capturas reales de una respuesta JSON de `/api/incidencias` y de `https://estadosseguro.onrender.com/health`. La segunda debe mostrar el HTTP 200 y el JSON `status: ok`.

*Figura 3. Respuestas HTTP de la API y del health check en la aplicación publicada.*

## Pruebas de calidad con Pytest

La suite contiene 12 pruebas que comprueban la página principal, la búsqueda y el filtro, el escape de entradas HTML, la longitud máxima del parámetro, el rechazo de estados desconocidos, las vistas de detalle, las respuestas JSON de la API y las cabeceras de seguridad.

La ejecución local realizada para preparar este artículo terminó con **12 passed**. En la última ejecución exitosa de GitHub Actions, Pytest también terminó con **12 passed en 0,11 s**. Este resultado confirma que esos casos pasaron en ese commit; no sustituye pruebas de carga ni una auditoría exhaustiva.

<!-- CAPTURA PENDIENTE: Figura 4. Insertarla después del párrafo de resultados de Pytest. -->
> **Captura pendiente — Figura 4: Resultado de Pytest.** Insertar una captura sin recortar la línea de comando ni el resumen final `12 passed`; indicar si corresponde a ejecución local o a GitHub Actions.

*Figura 4. Suite de Pytest: 12 pruebas completadas correctamente.*

## Nuclei: pruebas HTTP pequeñas y dirigidas

Nuclei permite definir comprobaciones como plantillas YAML. El proyecto está incluido en el [catálogo comunitario de herramientas de escaneo de vulnerabilidades de OWASP](https://community.owasp.org/Vulnerability_Scanning_Tools). Esa lista informa sobre herramientas disponibles; OWASP aclara que la inclusión no implica su aval.

Para este trabajo añadimos dos plantillas en `.nuclei/templates/`:

1. `estadoseguro-health.yaml` solicita `GET /health` y registra una coincidencia de severidad informativa cuando recibe HTTP 200 y el cuerpo contiene `"status":"ok"`.
2. `missing-security-headers.yaml` solicita `GET /` y genera una coincidencia de severidad baja si falta alguna de estas cabeceras: Content Security Policy, `X-Content-Type-Options` o `X-Frame-Options`.

La primera plantilla acredita que la ruta de salud responde; su resultado **no es una vulnerabilidad**. La segunda es una comprobación puntual de configuración de cabeceras y no representa cobertura general de seguridad.

## Integración en GitHub Actions

El workflow `.github/workflows/ci-security.yml` se ejecuta en cada push a `main`, pull request o lanzamiento manual. Instala dependencias, ejecuta Pytest, inicia Flask ligado a `127.0.0.1:5000`, espera que `/health` responda y después llama a la [integración oficial `projectdiscovery/nuclei-action@v3`](https://github.com/projectdiscovery/nuclei-action/blob/v3/README.md). La versión 3 de la acción acepta argumentos CLI mediante `args`; el flujo usa esa interfaz.

Los argumentos del escaneo son:

```text
-u http://127.0.0.1:5000
-t .nuclei/templates
-rl 2 -c 1 -timeout 5 -retries 0
-no-interactsh -disable-update-check
-jsonl -o artifacts/nuclei.jsonl
```

El objetivo del análisis automático es exclusivamente `127.0.0.1`. Las plantillas hacen solicitudes GET, la tasa está limitada a dos solicitudes por segundo, la concurrencia es uno y se deshabilitan Interactsh y las comprobaciones de actualización. El workflow no usa el escáner para explorar el dominio público de Render.

### Resultado real registrado

Al recopilar estas evidencias, antes de publicar el artículo, la ejecución exitosa más reciente era el run **42974596625**, asociado al commit `2298daa` (`deploy: fuerza plan gratuito en Render`). Se ejecutó el 11 de noviembre de 2026, entre `06:44:54` y `06:48:13 UTC`. El job terminó en `success`; su registro muestra 12 pruebas aprobadas, dos plantillas cargadas, un objetivo y dos conexiones HTTP. Nuclei v3.11.1 informó una coincidencia.

El archivo JSONL del artefacto contiene una sola fila: `estadosseguro-healthcheck`, severidad `info`, con coincidencia en `http://127.0.0.1:5000/health`. La plantilla de cabeceras no produjo coincidencias. Por tanto, en ese run **no se reportaron hallazgos de vulnerabilidad con las dos comprobaciones seleccionadas**. No es evidencia de que la aplicación esté libre de vulnerabilidades fuera de ese alcance.

El artefacto original de la ejecución se conserva durante 14 días en Actions. También copiamos el JSONL y el log de Flask a `docs/evidencias/github-actions-42974596625/` para que el artículo mantenga una referencia al resultado. El archivo conserva datos de la respuesta local (incluidas cabeceras HTTP); puede inspeccionarse directamente en el repositorio.

<!-- CAPTURA PENDIENTE: Figura 5. Insertarla después del resumen cuantitativo del escaneo. -->
> **Captura pendiente — Figura 5: Resultado de Nuclei.** Insertar una captura real del artefacto `nuclei.jsonl` de la ejecución 42974596625. Debe ser legible la coincidencia informativa de `/health`; no editar ni recrear el resultado.

*Figura 5. Salida JSONL real de Nuclei: una coincidencia informativa del health check.*

<!-- CAPTURA PENDIENTE: Figura 6. Insertarla después de este párrafo. -->
> **Captura pendiente — Figura 6: Workflow exitoso.** Insertar una captura de GitHub Actions donde se vea el run 42974596625, el commit asociado y el estado `success` de pruebas, health check, análisis Nuclei y carga de artefactos.

*Figura 6. Ejecución exitosa del workflow de calidad y seguridad en GitHub Actions.*

## Despliegue en Render

`render.yaml` define un único servicio web Python con `plan: free`, instala dependencias mediante `pip install -r requirements.txt` y ejecuta Gunicorn en el puerto que Render proporciona mediante `$PORT`. Render consulta `/health` como health check y `autoDeployTrigger: checksPass` condiciona los despliegues a las verificaciones de CI. El secreto `SECRET_KEY` se genera en Render.

La URL publicada respondió correctamente durante la comprobación descrita antes. La respuesta de salud confirma disponibilidad en ese momento; no equivale a una prueba de seguridad del despliegue. Tampoco se afirma aquí que Nuclei haya escaneado `estadosseguro.onrender.com`: el run documentado solo analizó el servidor local del runner.

Los servicios gratuitos de Render pueden suspenderse tras 15 minutos sin tráfico y usan un sistema de archivos efímero. EstadoSeguro usa datos de demostración en memoria, así que el proyecto no depende de persistencia local. ([Detalles del nivel gratuito de Render](https://render.com/docs/free), [especificación de Blueprints](https://render.com/docs/blueprint-spec)).

<!-- CAPTURA PENDIENTE: Figura 7. Insertarla al final de la sección de Render. -->
> **Captura pendiente — Figura 7: Servicio publicado en Render.** Insertar una captura real del panel de Render que muestre el servicio EstadoSeguro, el último despliegue y el plan configurado. Ocultar identificadores privados, menús de facturación y cualquier secreto.

*Figura 7. Servicio EstadoSeguro desplegado en Render con el plan y estado visibles.*

## Conclusiones y límites

Este caso conecta comportamiento observable y automatización: las pruebas ejercitan la aplicación, el health check evita escanear un proceso que no inició correctamente y Nuclei valida dos propiedades HTTP concretas en un objetivo local. El artefacto descargable guarda las coincidencias y el log del servidor, lo que hace posible revisar el resultado después del run.

La lectura responsable del informe también importa. Una coincidencia `info` confirma disponibilidad; la ausencia de coincidencia en la plantilla de cabeceras solo se refiere a las cabeceras evaluadas y a esa respuesta. Para ampliar cobertura harían falta nuevas comprobaciones justificadas y un alcance explícito, no ejecutar indiscriminadamente más plantillas contra el dominio desplegado.

## Referencias

- [Código y configuración de EstadoSeguro en GitHub](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei)
- [Ejecución 42974596625 y artefacto de Actions](https://github.com/anaesteban1/analisis-vulnerabilidades-nuclei/actions/runs/42974596625)
- [Nuclei Action oficial, rama v3](https://github.com/projectdiscovery/nuclei-action/blob/v3/README.md)
- [Catálogo comunitario OWASP de herramientas de escaneo](https://community.owasp.org/Vulnerability_Scanning_Tools)
- [Render Blueprint YAML Reference](https://render.com/docs/blueprint-spec)
- [Render: despliegue gratuito y limitaciones](https://render.com/docs/free)
