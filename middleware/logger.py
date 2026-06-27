import json
import time
from datetime import datetime, timezone
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "audit.log"


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
            status_code = response.status_code

            event = "ok"
            if status_code >= 400:
                event = "blocked_or_error_response"

            duration_ms = round((time.time() - start_time) * 1000, 2)

            self.write_log({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "method": request.method,
                "path": request.url.path,
                "ip": client_ip,
                "status": status_code,
                "duration_ms": duration_ms,
                "event": event
            })

            return response

        except Exception as exc:
            duration_ms = round((time.time() - start_time) * 1000, 2)

            self.write_log({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "method": request.method,
                "path": request.url.path,
                "ip": client_ip,
                "status": 500,
                "duration_ms": duration_ms,
                "event": "server_exception",
                "error": exc.__class__.__name__
            })

            raise

    @staticmethod
    def write_log(entry: dict):
        LOG_DIR.mkdir(exist_ok=True)

        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
