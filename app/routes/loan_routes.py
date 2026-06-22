from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.dependencies.database_dependency import get_db
from app.services.loan_service import (
    crear_prestamo,
    listar_prestamos,
    listar_prestamos_con_detalle,
    obtener_prestamo_por_id,
    devolver_prestamo
)

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("", response_model=List[LoanResponse])
def listar(
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return listar_prestamos(db, status, user_email, device_type)


@router.get("/details", response_model=List[LoanDetailResponse])
def listar_detalle(
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    prestamos = listar_prestamos_con_detalle(db, status, user_email, device_type)
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


@router.get("/{loan_id}", response_model=LoanResponse)
def obtener(loan_id: int, db: Session = Depends(get_db)):
    return obtener_prestamo_por_id(db, loan_id)


@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def crear(data: LoanCreate, db: Session = Depends(get_db)):
    return crear_prestamo(db, data)


@router.patch("/{loan_id}/return", response_model=LoanResponse)
def devolver(loan_id: int, db: Session = Depends(get_db)):
    return devolver_prestamo(db, loan_id)