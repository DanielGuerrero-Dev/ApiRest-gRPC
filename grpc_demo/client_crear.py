import sys
import grpc
import usuarios_pb2
import usuarios_pb2_grpc

nombre = sys.argv[1] if len(sys.argv) > 1 else "Ana"
correo = sys.argv[2] if len(sys.argv) > 2 else "ana@correo.com"

with grpc.insecure_channel("localhost:50051") as canal:
    stub = usuarios_pb2_grpc.UsuarioServiceStub(canal)  # el "stub" del cliente
    resp = stub.CrearUsuario(usuarios_pb2.UsuarioRequest(nombre=nombre, correo=correo))
    print(f"Creado -> id={resp.id} nombre={resp.nombre} correo={resp.correo}")
