"""Datos de demostración en memoria; no se requiere infraestructura externa."""

VALID_STATUSES = {"abierta", "en-progreso", "resuelta"}

INCIDENTS = [
    {"id": 1, "title": "Latencia elevada en pagos", "service": "Pagos", "status": "En progreso", "status_key": "en-progreso", "severity": "Alta", "updated": "11 nov 2026, 09:42", "summary": "Algunas operaciones presentan demoras superiores a lo habitual.", "description": "El equipo está revisando los tiempos de respuesta del proveedor de pagos. Las transacciones continúan procesándose y se monitorea la cola de solicitudes.", "owner": "Equipo de plataforma"},
    {"id": 2, "title": "Intermitencia en notificaciones", "service": "Notificaciones", "status": "Abierta", "status_key": "abierta", "severity": "Media", "updated": "11 nov 2026, 09:18", "summary": "El envío de correos puede tardar unos minutos.", "description": "Se investiga una demora intermitente en el procesamiento de notificaciones por correo electrónico.", "owner": "Equipo de comunicaciones"},
    {"id": 3, "title": "Mantenimiento de reportes", "service": "Reportes", "status": "Resuelta", "status_key": "resuelta", "severity": "Baja", "updated": "11 nov 2026, 08:55", "summary": "Servicio restablecido luego de una actualización programada.", "description": "La actualización finalizó correctamente y los reportes vuelven a estar disponibles.", "owner": "Equipo de datos"},
    {"id": 4, "title": "Acceso lento al portal", "service": "Portal web", "status": "Abierta", "status_key": "abierta", "severity": "Media", "updated": "10 nov 2026, 17:30", "summary": "Se observan tiempos de carga más largos en algunas páginas.", "description": "El equipo analiza el rendimiento del portal y recopila métricas para identificar la causa.", "owner": "Equipo web"},
]
