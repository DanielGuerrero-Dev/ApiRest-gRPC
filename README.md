# ApiRest-gRPC

## Contrato gRPC

Archivo: `grpc_demo/usuarios.proto`

| Elemento | Tipo | Descripción |
|---|---|---|
| `UsuarioService` | service | Servicio de usuarios |
| `CrearUsuario` | rpc | Recibe `UsuarioRequest`, devuelve `UsuarioResponse` |
| `ListarUsuarios` | rpc | Recibe `ListarRequest`, devuelve `ListarResponse` |
| `SuscribirUsuarios` | rpc (stream) | Recibe `SuscripcionRequest`, devuelve un flujo de `UsuarioResponse` |
| `UsuarioRequest` | message | `nombre` (string), `correo` (string) |
| `UsuarioResponse` | message | `id` (int32), `nombre` (string), `correo` (string), `mensaje` (string) |
| `ListarRequest` | message | vacío |
| `ListarResponse` | message | `usuarios` (lista de `UsuarioResponse`) |
| `SuscripcionRequest` | message | vacío |

## Generar el código

Desde la carpeta `grpc_demo` ejecutar:

    py -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. usuarios.proto

Genera `usuarios_pb2.py` (mensajes) y `usuarios_pb2_grpc.py` (servicio).
