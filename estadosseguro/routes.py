"""Rutas de EstadoSeguro."""

from flask import Blueprint, abort, jsonify, render_template, request

from .data import INCIDENTS, VALID_STATUSES

bp = Blueprint("main", __name__)


def filtered_incidents(query="", status=""):
    query = query.strip().casefold()
    status = status.strip().casefold()
    if len(query) > 100:
        abort(400, description="La búsqueda no puede superar 100 caracteres")
    if status and status not in VALID_STATUSES:
        abort(400, description="El filtro de estado no es válido")
    return [
        incident for incident in INCIDENTS
        if (not status or incident["status_key"] == status)
        and (not query or query in " ".join(str(value) for value in incident.values()).casefold())
    ]


@bp.get("/")
def index():
    query = request.args.get("q", "")
    status = request.args.get("estado", "")
    incidents = filtered_incidents(query, status)
    services = sorted({incident["service"] for incident in INCIDENTS})
    return render_template("index.html", incidents=incidents, query=query, status=status, services=services)


@bp.get("/incidencias/<int:incident_id>")
def incident_detail(incident_id):
    incident = next((item for item in INCIDENTS if item["id"] == incident_id), None)
    if incident is None:
        abort(404)
    return render_template("detail.html", incident=incident)


@bp.get("/api/incidencias")
def api_incidents():
    incidents = filtered_incidents(request.args.get("q", ""), request.args.get("estado", ""))
    return jsonify(incidencias=incidents, total=len(incidents))


@bp.get("/api/incidencias/<int:incident_id>")
def api_incident_detail(incident_id):
    incident = next((item for item in INCIDENTS if item["id"] == incident_id), None)
    if incident is None:
        return jsonify(error="Incidencia no encontrada"), 404
    return jsonify(incidencia=incident)


@bp.get("/health")
def health():
    return jsonify(status="ok", servicio="EstadoSeguro"), 200
