from fastapi import HTTPException
from app.data.users_db import fake_db


def get_user_or_404(user_id: int) -> dict:
    for user in fake_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="usuario no encontrado")


def check_email_exists(email: str, exclude_id: int = None) -> None:
    email = email.lower().strip()
    for user in fake_db:
        if user["email"] == email:
            if exclude_id is None or user["id"] != exclude_id:
                raise HTTPException(status_code=400, detail="el correo ya esta registrado")


def get_api_info() -> dict:
    return {
        "app": "device_systems",
        "version": "2.0",
    }