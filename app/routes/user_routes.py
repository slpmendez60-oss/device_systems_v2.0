from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.dependencies.database_dependency import get_db
from app.services.user_service import (
    crear_usuario,
    listar_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    actualizar_usuario_parcial,
    eliminar_usuario,
    filtrar_por_rol,
    filtrar_por_estado,
    ordenar_usuarios
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
def listar(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    orden: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if role:
        return filtrar_por_rol(db, role)
    if is_active is not None:
        return filtrar_por_estado(db, is_active)
    if orden:
        return ordenar_usuarios(db, orden)
    return listar_usuarios(db, skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
def obtener(user_id: int, db: Session = Depends(get_db)):
    return obtener_usuario_por_id(db, user_id)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear(data: UserCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, data)

@router.put("/{user_id}", response_model=UserResponse)
def actualizar(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return actualizar_usuario(db, user_id, data)

@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_parcial(user_id: int, data: UserPatch, db: Session = Depends(get_db)):
    return actualizar_usuario_parcial(db, user_id, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(user_id: int, db: Session = Depends(get_db)):
    eliminar_usuario(db, user_id)