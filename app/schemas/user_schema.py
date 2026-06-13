from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

ROLES_PERMITIDOS = ["admin", "support", "user"]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v) < 3:
            raise ValueError("El nombre debe tener minimo 3 caracteres")
        return v

    @field_validator("role")
    @classmethod
    def role_valido(cls, v):
        if v not in ROLES_PERMITIDOS:
            raise ValueError(f"El rol debe ser uno de: {ROLES_PERMITIDOS}")
        return v

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v) < 3:
            raise ValueError("El nombre debe tener minimo 3 caracteres")
        return v

    @field_validator("role")
    @classmethod
    def role_valido(cls, v):
        if v not in ROLES_PERMITIDOS:
            raise ValueError(f"El rol debe ser uno de: {ROLES_PERMITIDOS}")
        return v

class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError("El nombre debe tener minimo 3 caracteres")
        return v

    @field_validator("role")
    @classmethod
    def role_valido(cls, v):
        if v is not None and v not in ROLES_PERMITIDOS:
            raise ValueError(f"El rol debe ser uno de: {ROLES_PERMITIDOS}")
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}