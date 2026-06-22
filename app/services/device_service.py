from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import Optional
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def crear_dispositivo(db: Session, data: DeviceCreate):
    dispositivo = Device(**data.model_dump())
    try:
        db.add(dispositivo)
        db.commit()
        db.refresh(dispositivo)
        return dispositivo
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")


def listar_dispositivos(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(Device.name.ilike(f"%{search}%"))
    return query.all()


def obtener_dispositivo_por_id(db: Session, device_id: int):
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return dispositivo


def actualizar_dispositivo(db: Session, device_id: int, data: DeviceUpdate):
    dispositivo = obtener_dispositivo_por_id(db, device_id)
    try:
        for campo, valor in data.model_dump().items():
            setattr(dispositivo, campo, valor)
        db.commit()
        db.refresh(dispositivo)
        return dispositivo
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")


def actualizar_dispositivo_parcial(db: Session, device_id: int, data: DevicePatch):
    dispositivo = obtener_dispositivo_por_id(db, device_id)
    try:
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(dispositivo, campo, valor)
        db.commit()
        db.refresh(dispositivo)
        return dispositivo
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")


def eliminar_dispositivo(db: Session, device_id: int):
    dispositivo = obtener_dispositivo_por_id(db, device_id)
    db.delete(dispositivo)
    db.commit()