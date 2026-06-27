# Secure AI Gateway

<p align="center">
  <strong>A security-focused FastAPI gateway for AI-powered applications.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" />
  <img src="https://img.shields.io/badge/Security-JWT%20%7C%20Audit%20Logs%20%7C%20Brute%20Force-red" />
  <img src="https://img.shields.io/badge/AI-Prompt%20Injection%20Guard-purple" />
</p>

<p align="center">
  <a href="./README.tr.md">Türkçe README</a>
</p>

---

## Overview

**Secure AI Gateway** is a portfolio-grade backend project that combines API security, AI security, and backend architecture in a single FastAPI application.

It demonstrates how modern AI-enabled APIs can be designed with a **security-first architecture** rather than being exposed as simple unprotected inference endpoints.

---

## Key Features

### Authentication

- JWT-based authentication
- Protected `/predict` endpoint
- Bearer token validation
- Token expiration handling
- Invalid token handling

### Input Validation

- Pydantic request and response schemas
- Required field validation
- Empty input rejection
- Whitespace-only input rejection
- Maximum input length enforcement

### AI Security

- Prompt injection detection
- Suspicious prompt pattern blocking
- Protection against basic jailbreak-style input attempts

Blocked examples include:

```text
jailbreak
ignore previous instructions
reveal system prompt
developer mode
bypass safety
Audit Logging
Structured JSON audit logs
Method, path, IP, status code, and duration tracking
Security event logging
Failed login event tracking
Brute-force blocking event tracking
Brute Force Protection
IP-based failed login tracking
Temporary IP blocking after repeated failed attempts
429 Too Many Requests response for blocked clients
Audit trail for failed and blocked login attempts
Architecture
Client
  |
  v
FastAPI Gateway
  |
  +--> Pydantic Validation
  |
  +--> JWT Authentication
  |
  +--> Brute Force Protection
  |
  +--> Prompt Injection Guard
  |
  +--> AI Prediction Endpoint
  |
  +--> Structured Audit Logs
Project Structure
secure-ai-api/
│
├── main.py
├── requirements.txt
├── README.md
├── README.tr.md
├── .gitignore
│
├── models/
│   ├── __init__.py
│   └── schemas.py
│
├── middleware/
│   ├── __init__.py
│   ├── logger.py
│   ├── brute_force.py
│   ├── audit_logger.py
│   ├── rate_limiter.py
│   └── sanitizer.py
│
├── auth/
│   └── jwt_handler.py
│
├── ai_security/
│   ├── prompt_guard.py
│   └── anomaly_detector.py
│
├── inference/
│   └── model_router.py
│
├── monitoring/
│
├── utils/
│
└── logs/
    └── audit.log

logs/ is ignored by Git because audit logs may contain sensitive runtime information.

Getting Started
1. Clone the Repository
git clone https://github.com/ErenA001/secure-ai-api.git
cd secure-ai-api

For the local development structure used during this project:

cd ~/secure-ai-api/projects/secure-ai-api
2. Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run the API
uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000
API Usage
Health Check
curl http://127.0.0.1:8000

Example response:

{
  "status": "ok",
  "service": "secure-ai-api-v2"
}
Login

Demo credentials:

user: eren
password: secure123

Request:

curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user":"eren","password":"secure123"}'

Example response:

{
  "user": "eren",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
Protected Prediction Endpoint

First, get a JWT token:

TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user":"eren","password":"secure123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

Then call /predict:

curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"hello ai"}'

Example response:

{
  "input": "hello ai",
  "prediction": "safe",
  "confidence": 0.93,
  "flagged": false
}
Security Tests
Prompt Injection Test
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"jailbreak this system"}'

Expected response:

{
  "detail": "Prompt injection detected"
}
Brute Force Protection Test

Run multiple failed login attempts:

for i in {1..6}; do
  echo "--- attempt $i ---"
  curl -s -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"eren","password":"wrongpass"}'
  echo
done

Expected behavior:

Initial failed attempts return 401 Unauthorized
After the configured limit, the IP is temporarily blocked
Blocked requests return 429 Too Many Requests
Audit Logs

Audit logs are written as structured JSON lines:

cat logs/audit.log

Example log entries:

{"timestamp":"2026-06-27T11:33:05.181517+00:00","event":"failed_login","ip":"127.0.0.1","username":"eren","attempts":1,"status":401}
{"timestamp":"2026-06-27T11:33:05.230679+00:00","event":"brute_force_blocked","ip":"127.0.0.1","username":"eren","attempts":5,"status":429,"block_seconds":900}
Current Security Scope
Area	Status
JWT authentication	Implemented
Pydantic validation	Implemented
Prompt injection detection	Implemented
Audit logging	Implemented
Brute force protection	Implemented
Redis-based distributed rate limiting	Planned
Real ML anomaly detection	Planned
Docker production setup	Planned
CI pipeline	Planned
Roadmap
 FastAPI application scaffold
 JWT authentication
 Pydantic schemas
 Protected AI prediction endpoint
 Prompt injection guard
 Structured audit logging
 Brute force login protection
 Redis-based rate limiting
 Real anomaly detection model
 Docker and Docker Compose setup
 GitHub Actions CI
 Prometheus metrics
 Kubernetes deployment example
Security Notes

This is an educational and portfolio-focused project.

Current limitations:

Brute force protection is in-memory
Login uses demo credentials
JWT secret is hardcoded for development
Audit logs are local files
AI prediction is currently mocked

Recommended production improvements:

Move secrets to environment variables
Replace demo login with real user storage
Add password hashing
Use Redis for distributed blocking and rate limiting
Add HTTPS behind a reverse proxy
Add monitoring and alerting
Tech Stack
Python
FastAPI
Pydantic
PyJWT
Uvicorn
Structured JSON logging
Author

Built as a cybersecurity, AI security, and backend architecture portfolio project.

License

This project is open for educational and portfolio use.
