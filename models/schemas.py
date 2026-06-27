from pydantic import BaseModel, Field, field_validator


# -----------------------
# REQUEST SCHEMAS
# -----------------------

class PredictRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Input text for AI analysis"
    )

    @field_validator("text")
    @classmethod
    def no_whitespace_only(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Input cannot be whitespace only")
        return v.strip()


class LoginRequest(BaseModel):
    user: str = Field(..., min_length=1, max_length=64)


# -----------------------
# RESPONSE SCHEMAS
# -----------------------

class HealthResponse(BaseModel):
    status: str
    service: str


class LoginResponse(BaseModel):
    user: str
    access_token: str
    token_type: str = "bearer"


class PredictResponse(BaseModel):
    input: str
    prediction: str
    confidence: float
    flagged: bool = False


class ErrorResponse(BaseModel):
    detail: str
    code: int
