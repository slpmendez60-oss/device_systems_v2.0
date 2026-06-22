from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


def obtener_prestamo_por_id(db: Session, loan_id: int):
    prestamo = db.query(Loan).filter(Loan.id == loan_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return prestamo


def listar_prestamos(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    query = db.query(Loan).join(Loan.user).join(Loan.device)
    condiciones = []
    if status:
        condiciones.append(Loan.status == status)
    if user_email:
        condiciones.append(User.email.ilike(f"%{user_email}%"))
    if device_type:
        condiciones.append(Device.device_type.ilike(f"%{device_type}%"))
    if condiciones:
        query = query.filter(and_(*condiciones))
    return query.all()


def listar_prestamos_con_detalle(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    return listar_prestamos(db, status, user_email, device_type)


def obtener_prestamos_por_usuario(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def obtener_prestamos_por_dispositivo(db: Session, device_id: int):
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()


def crear_prestamo(db: Session, data: LoanCreate):
    usuario = db.query(User).filter(User.id == data.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    dispositivo = db.query(Device).filter(Device.id == data.device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not dispositivo.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no esta disponible")

    prestamo = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        status="active"
    )
    dispositivo.is_available = False
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def devolver_prestamo(db: Session, loan_id: int):
    prestamo = obtener_prestamo_por_id(db, loan_id)
    if prestamo.status == "returned":
        raise HTTPException(status_code=409, detail="El prestamo ya fue devuelto")

    prestamo.status = "returned"
    prestamo.return_date = datetime.utcnow()

    dispositivo = db.query(Device).filter(Device.id == prestamo.device_id).first()
    if dispositivo:
        dispositivo.is_available = True

    db.commit()
    db.refresh(prestamo)
    return prestamo