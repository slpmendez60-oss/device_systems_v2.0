from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestion de usuarios del sistema device_systems.",
    version="3.0",
    contact={
        "name": "device_systems",
        "email": "admin@device.com",
    },
)

app.include_router(user_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        errores.append({
            "campo": " -> ".join(str(loc) for loc in error["loc"]),
            "mensaje": error["msg"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "datos de entrada invalidos",
            "detalles": errores,
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "error interno del servidor"},
    )