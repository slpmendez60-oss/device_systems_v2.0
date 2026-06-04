from typing import List

fake_db: List[dict] = [
    {"id": 1, "name": "Carlos Mendez", "email": "carlos@gmail.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Ana Torres", "email": "ana@gmail.com", "role": "support", "is_active": True},
    {"id": 3, "name": "Luis Gomez", "email": "luis@gmail.com", "role": "user", "is_active": False},
    {"id": 4, "name": "Maria Rios", "email": "maria@gmail.com", "role": "user", "is_active": True},
]

id_counter = 5