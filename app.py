"""Punto de entrada WSGI para EstadoSeguro."""

from estadosseguro import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
