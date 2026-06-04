from typing import Optional, List
from app.data import users_db as db
from app.dependencies.user_dependencies import check_email_exists


def list_users(role: Optional[str], is_active: Optional[bool]) -> List[dict]:
    resultado = db.fake_db
    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]
    return resultado


def create_user(name: str, email: str, role: str, is_active: bool) -> dict:
    check_email_exists(email)
    nuevo = {
        "id": db.id_counter,
        "name": name,
        "email": email.lower().strip(),
        "role": role,
        "is_active": is_active,
    }
    db.fake_db.append(nuevo)
    db.id_counter += 1
    return nuevo


def update_user(user: dict, name: str, email: str, role: str, is_active: bool) -> dict:
    check_email_exists(email, exclude_id=user["id"])
    user["name"] = name
    user["email"] = email.lower().strip()
    user["role"] = role
    user["is_active"] = is_active
    return user


def patch_user(user: dict, fields: dict) -> dict:
    for campo, valor in fields.items():
        if campo == "email":
            valor = valor.lower().strip()
        user[campo] = valor
    return user


def delete_user(user: dict) -> dict:
    db.fake_db.remove(user)
    return user