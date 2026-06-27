import os
import time

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Request, status
from jwt import ExpiredSignatureError, InvalidTokenError

from middleware.brute_force import (
    check_brute_force,
    record_failed_attempt,
    record_successful_login,
)
from middleware.logger import AuditMiddleware
from models.schemas import (
    HealthResponse,
    LoginRequest,
    LoginResponse,
    PredictRequest,
    PredictResponse,
)

load_dotenv()

app = FastAPI(title="Secure AI Gateway v2")
app.add_middleware(AuditMiddleware)

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXP_SECONDS = int(os.getenv("TOKEN_EXP_SECONDS", "3600"))

DEMO_USER = os.getenv("DEMO_USER")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")

if not SECRET:
    raise RuntimeError("SECRET_KEY is missing. Please define it in .env.")

if len(SECRET) < 32:
    raise RuntimeError("SECRET_KEY must be at least 32 characters long.")

if not DEMO_USER or not DEMO_PASSWORD:
    raise RuntimeError("DEMO_USER and DEMO_PASSWORD must be defined in .env.")


# -----------------------
# JWT AUTH
# -----------------------

def create_token(user: str) -> str:
    cleaned_user = user.strip()

    if not cleaned_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User cannot be empty"
        )

    now = int(time.time())

    payload = {
        "sub": cleaned_user,
        "iat": now,
        "exp": now + TOKEN_EXP_SECONDS
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(authorization: str | None) -> dict:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format. Use: Bearer <token>"
        )

    token = authorization.split(" ", 1)[1].strip()

    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# -----------------------
# AI SECURITY LAYER
# -----------------------

DANGEROUS_PATTERNS = [
    "ignore previous instructions",
    "jailbreak",
    "reveal system prompt",
    "act as system",
    "developer mode",
    "bypass safety",
    "disable restrictions",
]


def prompt_guard(text: str) -> bool:
    normalized_text = text.lower()

    for pattern in DANGEROUS_PATTERNS:
        if pattern in normalized_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt injection detected"
            )

    return False


# -----------------------
# ROUTES
# -----------------------

@app.get("/", response_model=HealthResponse)
def root():
    return {
        "status": "ok",
        "service": "secure-ai-api-v2"
    }


@app.post("/login", response_model=LoginResponse, tags=["auth"])
def login(body: LoginRequest, request: Request):
    check_brute_force(request)

    if body.user != DEMO_USER or body.password != DEMO_PASSWORD:
        record_failed_attempt(request, body.user)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_token(body.user)

    record_successful_login(request, body.user)

    return {
        "user": body.user.strip(),
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, authorization: str | None = Header(default=None)):
    verify_token(authorization)

    flagged = prompt_guard(payload.text)

    return {
        "input": payload.text,
        "prediction": "safe",
        "confidence": 0.93,
        "flagged": flagged
    }
