from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: str
    role: RoleEnum
    is_active: bool = True

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("email no valido")
        return v.lower().strip()

    @field_validator("name")
    @classmethod
    def validar_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("el nombre debe tener al menos 3 caracteres")
        return v


class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: str
    role: RoleEnum
    is_active: bool

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("email no valido")
        return v.lower().strip()

    @field_validator("name")
    @classmethod
    def validar_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("el nombre debe tener al menos 3 caracteres")
        return v


class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if v is not None:
            if "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("email no valido")
            return v.lower().strip()
        return v

    @field_validator("name")
    @classmethod
    def validar_name(cls, v: str) -> str:
        if v is not None:
            v = v.strip()
            if len(v) < 3:
                raise ValueError("el nombre debe tener al menos 3 caracteres")
        return v


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool


class UserCreatedResponse(BaseModel):
    message: str
    user: UserResponse


class UserUpdatedResponse(BaseModel):
    message: str
    user: UserResponse


class UserDeletedResponse(BaseModel):
    message: str
    user: UserResponse