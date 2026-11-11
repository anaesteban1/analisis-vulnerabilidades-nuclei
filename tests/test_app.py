def test_home_displays_demo_services_and_incidents(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "EstadoSeguro" in response.get_data(as_text=True)
    assert "Latencia elevada en pagos" in response.get_data(as_text=True)
    assert "Notificaciones" in response.get_data(as_text=True)


def test_home_search_and_status_filters(client):
    response = client.get("/?q=pagos&estado=en-progreso")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Latencia elevada en pagos" in body
    assert "Intermitencia en notificaciones" not in body


def test_home_escapes_search_input(client):
    response = client.get("/?q=%3Cscript%3Ealert(1)%3C/script%3E")

    assert response.status_code == 200
    assert b"<script>alert(1)</script>" not in response.data


def test_search_parameter_length_is_limited(client):
    response = client.get("/?q=" + "a" * 101)

    assert response.status_code == 400


def test_unknown_status_is_rejected(client):
    response = client.get("/api/incidencias?estado=desconocido")

    assert response.status_code == 400
    assert response.json["error"] == "El filtro de estado no es válido"


def test_incident_detail_page(client):
    response = client.get("/incidencias/1")

    assert response.status_code == 200
    assert "Equipo de plataforma" in response.get_data(as_text=True)


def test_missing_incident_page_returns_404(client):
    response = client.get("/incidencias/999")

    assert response.status_code == 404
    assert "No encontramos esa página" in response.get_data(as_text=True)


def test_api_lists_and_filters_incidents(client):
    response = client.get("/api/incidencias?estado=abierta")

    assert response.status_code == 200
    assert response.json["total"] == 2
    assert all(row["status_key"] == "abierta" for row in response.json["incidencias"])


def test_api_returns_single_incident(client):
    response = client.get("/api/incidencias/1")

    assert response.status_code == 200
    assert response.json["incidencia"]["title"] == "Latencia elevada en pagos"


def test_api_missing_incident_returns_json_404(client):
    response = client.get("/api/incidencias/999")

    assert response.status_code == 404
    assert response.json["error"] == "Incidencia no encontrada"


def test_health_endpoint_and_security_headers(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok", "servicio": "EstadoSeguro"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_unknown_api_route_returns_json(client):
    response = client.get("/api/no-existe")

    assert response.status_code == 404
    assert response.is_json
