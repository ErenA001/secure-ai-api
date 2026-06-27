# Secure AI Gateway

<p align="center">
  <strong>A security-focused FastAPI gateway for AI-powered applications.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" />
  <img src="https://img.shields.io/badge/Security-JWT%20%7C%20Audit%20Logs%20%7C%20Brute%20Force-red" />
  <img src="https://img.shields.io/badge/AI-Prompt%20Injection%20Guard-purple" />
  <img src="https://img.shields.io/badge/Config-.env-orange" />
</p>

<p align="center">
  <a href="./README.tr.md">Türkçe README</a>
</p>

---

## Overview

**Secure AI Gateway** is a security-focused backend project built with FastAPI.

It combines API security, AI security, and backend architecture in one practical system. The project demonstrates how an AI-powered API can be protected with authentication, validation, audit logging, prompt injection detection, brute-force login protection, and environment-based configuration.

This repository is designed as a portfolio-grade project for cybersecurity, AI security, and backend engineering.

---

## Why This Project Matters

AI applications are commonly exposed through API endpoints. However, exposing a simple `/predict` endpoint without security controls creates serious risks.

A secure AI API should include:

- Authentication
- Input validation
- Abuse prevention
- Audit logging
- Security event tracking
- Prompt injection detection
- Protected inference endpoints
- Safe configuration management

This project provides a compact but realistic foundation for building secure AI API gateways.

---

## Features

### Authentication

- JWT-based authentication
- Protected `/predict` endpoint
- Bearer token validation
- Token expiration handling
- Invalid token handling

### Environment-Based Configuration

- Secrets are loaded from `.env`
- `.env` is ignored by Git
- `.env.example` is included as a safe template
- JWT secret, demo user, demo password, algorithm, and token lifetime are configurable

### Input Validation

- Pydantic request schemas
- Pydantic response schemas
- Empty input rejection
- Whitespace-only input rejection
- Maximum text length enforcement

### AI Security Layer

- Basic prompt injection detection
- Suspicious prompt pattern blocking
- Protection against simple jailbreak-style input attempts

Blocked prompt examples include:

```text
jailbreak
ignore previous instructions
reveal system prompt
developer mode
bypass safety
```

### Audit Logging

- Structured JSON audit logs
- Request method tracking
- Request path tracking
- Client IP logging
- Status code logging
- Request duration logging
- Security event logging

### Brute Force Protection

- IP-based failed login tracking
- Temporary IP blocking after repeated failed attempts
- `429 Too Many Requests` response for blocked clients
- Audit trail for failed and blocked login attempts

---

## Architecture

```text
Client
  |
  v
FastAPI Gateway
  |
  +--> .env Configuration
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
```

---

## Project Structure

```text
secure-ai-api/
│
├── main.py
├── requirements.txt
├── README.md
├── README.tr.md
├── .env.example
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
```

> `.env` and `logs/` are ignored by Git because they may contain sensitive runtime information.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ErenA001/secure-ai-api.git
cd secure-ai-api
```

For the current local development structure:

```bash
cd ~/secure-ai-api/projects/secure-ai-api
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Local Environment File

```bash
cp .env.example .env
```

Then edit `.env` with your local values:

```text
SECRET_KEY=your-secret-key-minimum-32-chars
DEMO_USER=your_username
DEMO_PASSWORD=your_password
ALGORITHM=HS256
TOKEN_EXP_SECONDS=3600
```

For local demo testing, the project can use demo credentials. These values are for development only and should not be used in production.

### 5. Run the API

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## API Usage

### Health Check

```bash
curl http://127.0.0.1:8000
```

Example response:

```json
{
  "status": "ok",
  "service": "secure-ai-api-v2"
}
```

---

### Login

Demo credentials are loaded from your local `.env` file.

Example local demo values:

```text
DEMO_USER=eren
DEMO_PASSWORD=secure123
```

Request:

```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user":"eren","password":"secure123"}'
```

Example response:

```json
{
  "user": "eren",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Protected Prediction Endpoint

First, get a JWT token:

```bash
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user":"eren","password":"secure123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

Then call `/predict`:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"hello ai"}'
```

Example response:

```json
{
  "input": "hello ai",
  "prediction": "safe",
  "confidence": 0.93,
  "flagged": false
}
```

---

## Security Tests

### Prompt Injection Test

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"jailbreak this system"}'
```

Expected response:

```json
{
  "detail": "Prompt injection detected"
}
```

---

### Brute Force Protection Test

Run multiple failed login attempts:

```bash
for i in {1..6}; do
  echo "--- attempt $i ---"
  curl -s -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"eren","password":"wrongpass"}'
  echo
done
```

Expected behavior:

- Initial failed attempts return `401 Unauthorized`
- After the configured limit, the IP is temporarily blocked
- Blocked requests return `429 Too Many Requests`

---

## Audit Logs

Audit logs are written as structured JSON lines:

```bash
cat logs/audit.log
```

Example log entries:

```json
{"timestamp":"2026-06-27T11:33:05.181517+00:00","event":"failed_login","ip":"127.0.0.1","username":"eren","attempts":1,"status":401}
{"timestamp":"2026-06-27T11:33:05.230679+00:00","event":"brute_force_blocked","ip":"127.0.0.1","username":"eren","attempts":5,"status":429,"block_seconds":900}
```

---

## Current Security Scope

| Area | Status |
|---|---|
| JWT authentication | Implemented |
| Environment-based configuration | Implemented |
| Pydantic validation | Implemented |
| Prompt injection detection | Implemented |
| Audit logging | Implemented |
| Brute force protection | Implemented |
| Redis-based distributed rate limiting | Planned |
| Real ML anomaly detection | Planned |
| Docker production setup | Planned |
| CI pipeline | Planned |

---

## Roadmap

- [x] FastAPI application scaffold
- [x] JWT authentication
- [x] Environment-based configuration
- [x] Pydantic schemas
- [x] Protected AI prediction endpoint
- [x] Prompt injection guard
- [x] Structured audit logging
- [x] Brute force login protection
- [ ] Redis-based rate limiting
- [ ] Real anomaly detection model
- [ ] Docker and Docker Compose setup
- [ ] GitHub Actions CI
- [ ] Prometheus metrics
- [ ] Kubernetes deployment example

---

## Security Notes

This is an educational and portfolio-focused project.

Current limitations:

- Brute force protection is in-memory
- Login uses local demo credentials from `.env`
- Audit logs are local files
- AI prediction is currently mocked

Recommended production improvements:

- Replace demo login with real user storage
- Add password hashing
- Use Redis for distributed blocking and rate limiting
- Add HTTPS behind a reverse proxy
- Add monitoring and alerting
- Rotate secrets regularly

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- PyJWT
- Uvicorn
- python-dotenv
- Structured JSON logging

---

## Author

Built as a cybersecurity, AI security, and backend architecture portfolio project.

---

## License

This project is open for educational and portfolio use.
