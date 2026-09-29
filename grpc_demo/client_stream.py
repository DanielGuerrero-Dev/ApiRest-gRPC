import grpc
import usuarios_pb2
import usuarios_pb2_grpc

with grpc.insecure_channel("localhost:50051") as canal:
    stub = usuarios_pb2_grpc.UsuarioServiceStub(canal)
    print("Suscrito. Esperando usuarios nuevos... (Ctrl+C para salir)")
    try:
        for u in stub.SuscribirUsuarios(usuarios_pb2.SuscripcionRequest()):
            print(f"[STREAM] id={u.id} nombre={u.nombre} correo={u.correo}")
    except KeyboardInterrupt:
        pass
