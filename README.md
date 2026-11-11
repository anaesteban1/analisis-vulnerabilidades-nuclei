# EstadoSeguro

**Panel de incidencias de servicios** desarrollado como proyecto universitario para el curso de Calidad de Software. El repositorio integra una aplicación Flask, pruebas con Pytest, análisis de seguridad con ProjectDiscovery Nuclei y una definición de despliegue para Render.

## Tecnologías

- Python 3.12 y Flask
- HTML5 y CSS3 responsive
- Pytest
- Gunicorn
- GitHub Actions
- ProjectDiscovery Nuclei (`projectdiscovery/nuclei-action@v3`), listado en el [catálogo comunitario de herramientas de escaneo de vulnerabilidades de OWASP](https://community.owasp.org/Vulnerability_Scanning_Tools). La inclusión en la lista no implica aval de OWASP.
- Render Blueprints

## Funcionalidades

- Panel de servicios e incidencias con datos de demostración locales.
- Búsqueda por texto y filtro por estado.
- Página de detalle para cada incidencia.
- API REST: `GET /api/incidencias` y `GET /api/incidencias/<id>`.
- Endpoint `GET /health` para verificación de disponibilidad.
- Validación de filtros, respuestas de error controladas y cabeceras HTTP de seguridad.
- Configuración por entorno para `SECRET_KEY`; modo debug desactivado por defecto.

La aplicación no necesita base de datos, credenciales ni servicios externos.

## Estructura

```text
.
├── .github/workflows/ci-security.yml  # Pruebas y análisis en GitHub Actions
├── .nuclei/templates/                 # Comprobaciones HTTP locales y no destructivas
├── docs/evidencias/                   # Guía para capturas verificables
├── estadosseguro/
│   ├── static/styles.css
│   ├── templates/
│   ├── data.py                        # Incidencias de demostración
│   └── routes.py                      # Vistas web, API y health check
├── tests/                             # Pruebas automatizadas
├── app.py                             # Punto de entrada Flask/Gunicorn
├── render.yaml                        # Blueprint de Render
└── requirements.txt
```

## Instalación y ejecución local

Requiere Python 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = "clave-local-de-desarrollo"
python -m flask --app app run --host 127.0.0.1 --port 5000
```

Abre `http://127.0.0.1:5000`. La API se consulta en `http://127.0.0.1:5000/api/incidencias` y la comprobación de salud en `http://127.0.0.1:5000/health`.

Para producción, inicia el servidor WSGI con:

```sh
gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 60
```

## Pruebas

```sh
python -m pytest -q
```

Las pruebas cubren la página principal, filtros, escape de entrada, límites de parámetros, detalle de incidencias, API, endpoint de salud y cabeceras.

## Análisis de seguridad con Nuclei

El flujo `.github/workflows/ci-security.yml` se ejecuta en `push` a `main`, pull requests y manualmente. Instala dependencias, ejecuta Pytest, inicia Flask ligado explícitamente a `127.0.0.1:5000`, espera a que `/health` responda y llama a la integración oficial `projectdiscovery/nuclei-action@v3`. El workflow entrega los resultados y el log de la aplicación como artefacto descargable `resultados-nuclei`.

El escaneo apunta únicamente a `http://127.0.0.1:5000`, carga plantillas versionadas en `.nuclei/templates`, limita la tasa a 2 solicitudes por segundo, usa concurrencia 1 y desactiva Interactsh y la comprobación de actualizaciones. Las comprobaciones realizan solicitudes GET: una confirma `/health` (hallazgo informativo de disponibilidad) y otra busca la ausencia de cabeceras base en la portada. No se habilitan fuzzing, fuerza bruta ni plantillas de terceros.

El alcance del resultado queda limitado a estas comprobaciones concretas. Un JSONL vacío significa que Nuclei no encontró coincidencias con las plantillas configuradas durante esa ejecución; **no** demuestra ausencia general de vulnerabilidades. Este repositorio aún no tiene resultados de GitHub Actions hasta que el flujo se ejecute en GitHub.

Para ejecutar las mismas comprobaciones localmente, instala Nuclei desde [ProjectDiscovery](https://github.com/projectdiscovery/nuclei) y, en una segunda terminal, usa:

```sh
mkdir -p artifacts
nuclei -u http://127.0.0.1:5000 \
  -t .nuclei/templates \
  -rl 2 -c 1 -timeout 5 -retries 0 \
  -no-interactsh -disable-update-check \
  -jsonl -o artifacts/nuclei.jsonl
```

## Despliegue en Render

`render.yaml` define un servicio web Python 3.12.10, Gunicorn, una clave `SECRET_KEY` generada por Render, chequeo de salud en `/health` y despliegues automáticos solo cuando pasan las verificaciones de CI (`autoDeployTrigger: checksPass`). No se ha creado ni conectado ningún servicio en la nube.

1. Publica el repositorio en GitHub y confirma que las ejecuciones de GitHub Actions estén en verde para la rama que conectarás.
2. En Render, crea un Blueprint nuevo y conecta el repositorio de GitHub. Render leerá `render.yaml`.
3. Revisa el servicio propuesto y confirma la creación desde el panel de Render.
4. Comprueba en la configuración del servicio que el auto despliegue esté en **After CI Checks Pass**. El Blueprint ya declara esta condición.
5. Render verificará `/health` durante los despliegues. Los commits posteriores se desplegarán después de pasar las comprobaciones de GitHub.

La creación del servicio y la conexión de cuentas se realizarán posteriormente desde tu cuenta; este proyecto solo incluye la configuración.

## Evidencias

Consulta [docs/evidencias/README.md](docs/evidencias/README.md) para preparar capturas reales del repositorio, pruebas, flujo y configuración de despliegue. No se incluyen imágenes ni resultados de ejecuciones ficticios.
