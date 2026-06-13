# device_systems API v3.0

API REST para la gestion de usuarios del sistema device_systems con persistencia de datos mediante SQLAlchemy y SQLite.

## Estructura del proyecto

![estructura](images2/estructura_proyecto.png)

## Base de datos generada

![base_datos](images2/base_datos.png)

## Swagger UI

![swagger](images2/swagger.png)

## Pruebas de endpoints

### Prueba 1 - Crear usuario valido (POST /users) - 201
![crear_usuario](images2/crear_usuario.png)

### Prueba 2 - Email repetido (POST /users) - 400
![email_repetido](images2/email_repetido.png)

### Prueba 3 - Listar usuarios (GET /users) - 200
![listar_usuarios](images2/listar_usuarios.png)

### Prueba 4 - Consultar por ID (GET /users/1) - 200
![consultar_usuario_id](images2/consultar_usuario_id.png)

### Prueba 5 - Usuario inexistente (GET /users/999) - 404
![usuario_inexistente](images2/usuario_inexistente.png)

### Prueba 6 - Filtrar por rol (GET /users?role=admin) - 200
![filtrar_rol](images2/filtrar_rol.png)

### Prueba 7 - Filtrar activos (GET /users?is_active=true) - 200
![filtrar_usuarios_activos](images2/filtrar_usuarios_activos.png)

### Prueba 8 - Actualizar completo (PUT /users/1) - 200
![actualizar_put](images2/actualizar_put.png)

### Prueba 9 - Actualizar parcial (PATCH /users/1) - 200
![actualizar_patch](images2/actualizar_patch.png)

### Prueba 10 - Eliminar usuario (DELETE /users/1) - 204
![eliminar_usuario](images2/eliminar_usuario.png)

### Prueba 11 - Verificar eliminado (GET /users/1) - 404
![verificar_usuario_eliminado](images2/verificar_usuario_eliminado.png)

## Diferencia entre modelo SQLAlchemy y schema Pydantic

El modelo SQLAlchemy representa la tabla en la base de datos. Define las columnas, tipos de datos y restricciones a nivel de base de datos como nullable, unique y primary key. Es la capa que se comunica directamente con SQLite.

El schema Pydantic define la estructura de datos para la entrada y salida de la API. Aplica validaciones a nivel de aplicacion como longitud minima, formato de email y valores permitidos para el rol. No tiene relacion directa con la base de datos.

## Reflexion final

Usar persistencia en una API REST es fundamental porque los datos no se pierden cuando el servidor se reinicia. En la version anterior los usuarios se guardaban en memoria y se borraban al detener el servidor. Con SQLAlchemy y SQLite los datos quedan almacenados en un archivo fisico, lo que permite que la API funcione como una aplicacion real. Ademas el uso de un ORM facilita las operaciones sobre la base de datos sin necesidad de escribir SQL directamente.