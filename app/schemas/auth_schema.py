from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


ROLES_PERMITIDOS = ["admin", "support", "user"]


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electronico valido")
    password: str = Field(..., min_length=8, description="Contrasena segura")
    role: str = Field(..., description="Rol del usuario: admin, support o user")

    @field_validator("password")
    @classmethod
    def password_segura(cls, v):
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios")
        if not any(c.isupper() for c in v):
            raise ValueError("La contrasena debe tener al menos una mayuscula")
        if not any(c.islower() for c in v):
            raise ValueError("La contrasena debe tener al menos una minuscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contrasena debe tener al menos un numero")
        return v

    @field_validator("role")
    @classmethod
    def role_valido(cls, v):
        if v not in ROLES_PERMITIDOS:
            raise ValueError(f"El rol debe ser uno de: {ROLES_PERMITIDOS}")
        return v

    @field_validator("name")
    @classmethod
    def name_valido(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener minimo 3 caracteres")
        return v.strip()


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electronico registrado")
    password: str = Field(..., description="Contrasena del usuario")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None