device_systems API v2.0

API REST para gestion de usuarios con FastAPI. CRUD completo con manejo de errores, codigos HTTP, Dependency Injection y documentacion Swagger/OpenAPI.

Estructura del proyecto

device_systems/
|__ app/
|   |__ main.py
|   |__ schemas/
|   |   |__ user_schema.py
|   |__ routes/
|   |   |__ user_routes.py
|   |__ services/
|   |   |__ user_service.py
|   |__ dependencies/
|   |   |__ user_dependencies.py
|   |__ data/
|       |__ users_db.py
|__ images/
|__ requirements.txt
|__ README.md


Instalacion

pip install -r requirements.txt

Ejecucion

python -m uvicorn app.main:app --reload

Documentacion

Swagger UI: http://127.0.0.1:8000/docs
ReDoc:       http://127.0.0.1:8000/redoc

Endpoints

GET    /users                    lista todos los usuarios
GET    /users?role=admin         filtra por rol
GET    /users?is_active=true     filtra por estado
GET    /users/{user_id}          obtiene usuario por id
POST   /users                    crea un nuevo usuario
PUT    /users/{user_id}          actualiza usuario completo
PATCH  /users/{user_id}          actualiza usuario parcialmente
DELETE /users/{user_id}          elimina un usuario

Codigos de estado HTTP

200   operacion exitosa
201   usuario creado
400   datos invalidos o correo duplicado o patch vacio
404   usuario no encontrado
422   error de validacion Pydantic

Ejemplo POST

{
    "name": "Sofia Castro",
    "email": "sofia@device.com",
    "role": "user",
    "is_active": true
}

Ejemplo PUT

{
    "name": "Carlos Actualizado",
    "email": "carlos2@device.com",
    "role": "support",
    "is_active": true
}

Ejemplo PATCH

{
    "role": "admin"
}

Roles permitidos

admin
support
user

Cabeceras de respuesta

X-App-Name: device_systems
X-API-Version: 2.0

Dependency Injection

Se usa Depends() para reutilizar logica comun entre endpoints:

get_user_or_404     busca un usuario por ID y lanza 404 si no existe
check_email_exists  verifica si un correo ya esta registrado
get_api_info        retorna metadatos de la API para las cabeceras

Cada endpoint recibe estas dependencias como parametros y FastAPI las ejecuta automaticamente antes de la funcion principal.

Manejo de errores

Los errores se controlan con HTTPException y manejadores personalizados:

404   usuario no encontrado via get_user_or_404 en dependencies
400   correo duplicado en servicios, patch vacio en rutas
422   validacion automatica de Pydantic con manejador personalizado
500   manejador generico para errores inesperados

Servidor corriendo

![arrancando_servidor](images/arrancando_servidor.png)

Capturas de Swagger UI

![Swagger_UI](images/Swagger_UI.png)

Capturas de ReDoc

![ReDoc](images/ReDoc.png)

Evidencia GET /users

![get_users](images/get_users.png)
![get_users2](images/get_users2.png)

Evidencia GET /users/{user_id}

![get_user_by_id](images/get_user_by_id.png)
![get_user_by_id2](images/get_user_by_id2.png)

Evidencia POST /users

![post_users](images/post_users.png)
![post_users2](images/post_users2.png)

Evidencia PUT /users/{user_id}

![put_users](images/put_users.png)
![put_users2](images/put_users2.png)

Evidencia PATCH /users/{user_id}

![patch_users](images/patch_users.png)
![patch_users2](images/patch_users2.png)

Evidencia DELETE /users/{user_id}

![delete_users](images/delete_users.png)
![delete_users2](images/delete_users2.png)

Evidencia error 404

![error_404](images/error_404.png)
![error2_404](images/error2_404.png)

Evidencia error correo duplicado

![error_duplicado](images/error_duplicado.png)
![error_duplicado2](images/error_duplicado2.png)

Evidencia error validacion

![error_validacion](images/error_validacion.png)
![error_validacion2](images/error_validacion2.png)

Evidencia error patch vacio

![error_patch_vacio](images/error_patch_vacio.png)
![error_patch_vacio2](images/error_patch_vacio2.png)

Reflexion

La evolucion de device_systems hacia un CRUD completo demostro como FastAPI permite escalar una API de forma ordenada. La separacion en capas, rutas, servicios, dependencias y datos, hace que el codigo sea mas facil de mantener y extender. El uso de Depends() elimino la duplicacion de logica como la busqueda de usuarios por ID o la validacion de correos. El manejo de errores con HTTPException y manejadores personalizados garantiza que la API siempre responda de forma predecible. Los codigos HTTP correctos en cada operacion hacen que la API sea intuitiva para cualquier cliente que la consuma.