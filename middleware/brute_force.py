import json
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, status


BRUTE_FORCE_LIMIT = 5
BLOCK_SECONDS = 15 * 60

_attempts = {}

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "audit.log"


def _client_ip(request) -> str:
    return request.client.host if request.client else "unknown"


def _write_security_log(entry: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check_brute_force(request) -> None:
    ip = _client_ip(request)
    now = time.time()

    data = _attempts.get(ip)

    if not data:
        return

    blocked_until = data.get("blocked_until", 0)

    if blocked_until > now:
        seconds_remaining = int(blocked_until - now)

        _write_security_log({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "blocked_login_attempt",
            "ip": ip,
            "status": 429,
            "seconds_remaining": seconds_remaining
        })

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"IP blocked for {seconds_remaining} seconds"
        )

    if blocked_until and blocked_until <= now:
        _attempts.pop(ip, None)


def record_failed_attempt(request, username: str) -> None:
    ip = _client_ip(request)
    now = time.time()

    data = _attempts.setdefault(ip, {
        "count": 0,
        "blocked_until": 0
    })

    data["count"] += 1

    if data["count"] >= BRUTE_FORCE_LIMIT:
        data["blocked_until"] = now + BLOCK_SECONDS

        _write_security_log({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "brute_force_blocked",
            "ip": ip,
            "username": username,
            "attempts": data["count"],
            "status": 429,
            "block_seconds": BLOCK_SECONDS
        })

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. IP blocked for 15 minutes."
        )

    _write_security_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "failed_login",
        "ip": ip,
        "username": username,
        "attempts": data["count"],
        "status": 401
    })


def record_successful_login(request, username: str) -> None:
    ip = _client_ip(request)
    _attempts.pop(ip, None)

    _write_security_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "successful_login",
        "ip": ip,
        "username": username,
        "status": 200
    })


def get_attempt_count(ip: str) -> int:
    data = _attempts.get(ip)
    if not data:
        return 0
    return data.get("count", 0)
