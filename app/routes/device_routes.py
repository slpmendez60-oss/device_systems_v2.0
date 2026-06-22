from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.dependencies.database_dependency import get_db
from app.services.device_service import (
    crear_dispositivo,
    listar_dispositivos,
    obtener_dispositivo_por_id,
    actualizar_dispositivo,
    actualizar_dispositivo_parcial,
    eliminar_dispositivo
)
from app.services.loan_service import obtener_prestamos_por_dispositivo

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=List[DeviceResponse])
def listar(
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return listar_dispositivos(db, device_type, is_available, brand, search)


@router.get("/{device_id}", response_model=DeviceResponse)
def obtener(device_id: int, db: Session = Depends(get_db)):
    return obtener_dispositivo_por_id(db, device_id)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def crear(data: DeviceCreate, db: Session = Depends(get_db)):
    return crear_dispositivo(db, data)


@router.put("/{device_id}", response_model=DeviceResponse)
def actualizar(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)):
    return actualizar_dispositivo(db, device_id, data)


@router.patch("/{device_id}", response_model=DeviceResponse)
def actualizar_parcial(device_id: int, data: DevicePatch, db: Session = Depends(get_db)):
    return actualizar_dispositivo_parcial(db, device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(device_id: int, db: Session = Depends(get_db)):
    eliminar_dispositivo(db, device_id)


@router.get("/{device_id}/loans", response_model=List[LoanDetailResponse])
def historial_prestamos(device_id: int, db: Session = Depends(get_db)):
    prestamos = obtener_prestamos_por_dispositivo(db, device_id)
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