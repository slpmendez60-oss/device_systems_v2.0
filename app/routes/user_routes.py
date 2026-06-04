from fastapi import APIRouter, Response, Depends, HTTPException
from typing import Optional, List

from app.schemas.user_schema import (
    UserCreate, UserUpdate, UserPatch,
    UserResponse, UserCreatedResponse, UserUpdatedResponse, UserDeletedResponse,
    RoleEnum,
)
from app.dependencies.user_dependencies import get_user_or_404, get_api_info
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=List[UserResponse], summary="Listar usuarios")
def get_users(
    response: Response,
    role: Optional[RoleEnum] = None,
    is_active: Optional[bool] = None,
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    return user_service.list_users(
        role=role.value if role else None,
        is_active=is_active,
    )


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user_by_id(
    response: Response,
    user: dict = Depends(get_user_or_404),
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    return user


@router.post("", response_model=UserCreatedResponse, status_code=201, summary="Crear usuario")
def create_user(
    user_data: UserCreate,
    response: Response,
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    nuevo = user_service.create_user(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role.value,
        is_active=user_data.is_active,
    )
    return {"message": "usuario creado", "user": nuevo}


@router.put("/{user_id}", response_model=UserUpdatedResponse, summary="Actualizar usuario completo")
def update_user(
    user_data: UserUpdate,
    response: Response,
    user: dict = Depends(get_user_or_404),
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    actualizado = user_service.update_user(
        user=user,
        name=user_data.name,
        email=user_data.email,
        role=user_data.role.value,
        is_active=user_data.is_active,
    )
    return {"message": "usuario actualizado", "user": actualizado}


@router.patch("/{user_id}", response_model=UserUpdatedResponse, summary="Actualizar usuario parcialmente")
def patch_user(
    user_data: UserPatch,
    response: Response,
    user: dict = Depends(get_user_or_404),
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    fields = user_data.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="debe enviar al menos un campo para actualizar")
    if "role" in fields and fields["role"] is not None:
        fields["role"] = fields["role"].value
    actualizado = user_service.patch_user(user=user, fields=fields)
    return {"message": "usuario actualizado parcialmente", "user": actualizado}


@router.delete("/{user_id}", response_model=UserDeletedResponse, summary="Eliminar usuario")
def delete_user(
    response: Response,
    user: dict = Depends(get_user_or_404),
    info: dict = Depends(get_api_info),
):
    response.headers["X-App-Name"] = info["app"]
    response.headers["X-API-Version"] = info["version"]
    eliminado = user_service.delete_user(user=user)
    return {"message": "usuario eliminado", "user": eliminado}