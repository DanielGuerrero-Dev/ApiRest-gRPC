"""Servidor gRPC de usuarios (guarda los usuarios en usuarios.json)."""
import json
import os
import queue
import threading
from concurrent import futures

import grpc
import usuarios_pb2
import usuarios_pb2_grpc

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json")


class UsuarioService(usuarios_pb2_grpc.UsuarioServiceServicer):
    def __init__(self):
        self.lock = threading.Lock()
        self.suscriptores = []  # una cola por cliente suscrito
        self.usuarios = self._cargar()
        self.siguiente_id = max((u["id"] for u in self.usuarios), default=0) + 1

    def _cargar(self):
        """Lee los usuarios guardados; si no hay archivo, empieza vacío."""
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, encoding="utf-8") as f:
                return json.load(f)
        return []

    def _guardar(self):
        """Escribe la lista completa de usuarios en el archivo."""
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(self.usuarios, f, ensure_ascii=False, indent=2)

    def CrearUsuario(self, request, context):
        """Valida, crea, guarda y notifica a los suscritos."""
        if not request.nombre or not request.correo:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "Se requieren nombre y correo")
        with self.lock:
            resp = usuarios_pb2.UsuarioResponse(
                id=self.siguiente_id, nombre=request.nombre, correo=request.correo)
            self.siguiente_id += 1
            self.usuarios.append(
                {"id": resp.id, "nombre": resp.nombre, "correo": resp.correo})
            self._guardar()
            for q in self.suscriptores:  # notifica a los suscritos
                q.put(resp)
        print(f"[servidor] Usuario creado: {resp.nombre} <{resp.correo}>")
        return resp

    def SuscribirUsuarios(self, request, context):
        """Streaming: envía cada usuario nuevo mientras el cliente siga conectado."""
        q = queue.Queue()
        with self.lock:
            self.suscriptores.append(q)
        try:
            while context.is_active():
                try:
                    yield q.get(timeout=1)
                except queue.Empty:
                    continue
        finally:
            with self.lock:
                self.suscriptores.remove(q)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuarios_pb2_grpc.add_UsuarioServiceServicer_to_server(UsuarioService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[servidor] gRPC escuchando en el puerto 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
