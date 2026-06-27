from fastapi import FastAPI, HTTPException, Header, status
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import time

from models.schemas import (
    HealthResponse,
    LoginRequest,
    LoginResponse,
    PredictRequest,
    PredictResponse,
)

app = FastAPI(title="Secure AI Gateway v2")

SECRET = "supersecretkey_minimum32bytes_pad!!"
ALGORITHM = "HS256"
TOKEN_EXP_SECONDS = 3600


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


@app.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    token = create_token(payload.user)

    return {
        "user": payload.user.strip(),
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
