import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        start_time = time.time()

        response = await call_next(request)

        process_time = round(time.time() - start_time, 4)

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        print(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> {response.status_code} ({process_time}s)"
        )

        return response