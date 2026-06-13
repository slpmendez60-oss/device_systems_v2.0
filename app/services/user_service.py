from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

def crear_usuario(db: Session, data: UserCreate):
    usuario = User(**data.model_dump())
    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def obtener_usuario_por_id(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def obtener_usuario_por_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def actualizar_usuario(db: Session, user_id: int, data: UserUpdate):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        for campo, valor in data.model_dump().items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

def actualizar_usuario_parcial(db: Session, user_id: int, data: UserPatch):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

def eliminar_usuario(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()

def filtrar_por_rol(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()

def filtrar_por_estado(db: Session, is_active: bool):
    return db.query(User).filter(User.is_active == is_active).all()

def ordenar_usuarios(db: Session, orden: str = "name"):
    if orden == "created_at":
        return db.query(User).order_by(User.created_at).all()
    return db.query(User).order_by(User.name).all()