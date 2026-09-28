"""API REST de usuarios (Semana 8). Datos en memoria, sin base de datos."""
from flask import Flask, request, jsonify

app = Flask(__name__)
usuarios = []  # lista en memoria


@app.post("/usuarios")
def crear_usuario():
    datos = request.get_json(silent=True) or {}
    nombre, correo = datos.get("nombre"), datos.get("correo")
    if not nombre or not correo:
        return jsonify(error="Se requieren 'nombre' y 'correo'"), 400
    usuario = {"id": len(usuarios) + 1, "nombre": nombre, "correo": correo}
    usuarios.append(usuario)
    return jsonify(usuario), 201


@app.get("/usuarios")
def listar_usuarios():
    return jsonify(usuarios), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
