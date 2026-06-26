from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.models.user_model import User
from app.services.user_service import (
    criar_usuario_direto,
    listar_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    actualizar_usuario_parcial,
    eliminar_usuario,
    filtrar_por_rol,
    filtrar_por_estado,
    ordenar_usuarios
)
from app.schemas.loan_schema import LoanDetailResponse
from app.services.loan_service import obtener_prestamos_por_usuario

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse])
@limiter.limit("30/minute")
def listar(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    orden: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if role:
        return filtrar_por_rol(db, role)
    if is_active is not None:
        return filtrar_por_estado(db, is_active)
    if orden:
        return ordenar_usuarios(db, orden)
    return listar_usuarios(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def obtener(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return obtener_usuario_por_id(db, user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return criar_usuario_direto(db, data)


@router.put("/{user_id}", response_model=UserResponse)
def actualizar(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return actualizar_usuario(db, user_id, data)


@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_parcial(
    user_id: int,
    data: UserPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return actualizar_usuario_parcial(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    eliminar_usuario(db, user_id)


@router.get("/{user_id}/loans", response_model=List[LoanDetailResponse])
def prestamos_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    prestamos = obtener_prestamos_por_usuario(db, user_id)
    return [
        LoanDetailResponse(
            loan_id=p.id,
            status=p.status,
            loan_date=p.loan_date,
            return_date=p.return_date,
            user=p.user,
            device=p.device
        )
        for p in prestamos
    ]