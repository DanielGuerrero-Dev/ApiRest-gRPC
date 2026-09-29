# ApiRest-gRPC

## Contrato gRPC

Archivo: `GRPC/usuarios.proto`

| Elemento | Tipo | Descripción |
|---|---|---|
| `UsuariosService` | service | Servicio de usuarios |
| `CrearUsuario` | rpc | Recibe `UsuarioRequest`, devuelve `UsuarioResponse` |
| `UsuarioRequest` | message | `nombre` (string), `correo` (string) |
| `UsuarioResponse` | message | `id` (int32), `nombre` (string), `correo` (string), `mensaje` (string) |
