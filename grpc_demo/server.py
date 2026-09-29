"""Servidor gRPC de usuarios."""
import queue
import threading
from concurrent import futures

import grpc

import usuarios_pb2
import usuarios_pb2_grpc


class UsuarioService(usuarios_pb2_grpc.UsuarioServiceServicer):
    def __init__(self):
        self.lock = threading.Lock()
        self.siguiente_id = 1
        self.suscriptores = []  # una cola por cliente suscrito

    def CrearUsuario(self, request, context):
        """Valida, crea el usuario y notifica a los suscritos."""
        if not request.nombre or not request.correo:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "Se requieren nombre y correo")
        with self.lock:
            resp = usuarios_pb2.UsuarioResponse(
                id=self.siguiente_id, nombre=request.nombre, correo=request.correo)
            self.siguiente_id += 1
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
