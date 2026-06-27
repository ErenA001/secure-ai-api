# Secure AI Gateway

<p align="center">
  <strong>AI destekli uygulamalar için güvenlik odaklı FastAPI API Gateway projesi.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" />
  <img src="https://img.shields.io/badge/Security-JWT%20%7C%20Audit%20Logs%20%7C%20Brute%20Force-red" />
  <img src="https://img.shields.io/badge/AI-Prompt%20Injection%20Guard-purple" />
  <img src="https://img.shields.io/badge/Config-.env-orange" />
</p>

<p align="center">
  <a href="./README.md">English README</a>
</p>

---

## Genel Bakış

**Secure AI Gateway**, FastAPI ile geliştirilmiş güvenlik odaklı bir backend projesidir.

Bu proje; API güvenliği, AI güvenliği ve backend mimarisini tek bir pratik sistem içinde birleştirir. Amaç, AI destekli bir API'nin yalnızca basit bir `/predict` endpoint'i olarak sunulmasının yeterli olmadığını; authentication, validation, audit logging, prompt injection detection, brute-force protection ve environment-based configuration gibi katmanlara ihtiyaç duyduğunu göstermektir.

Bu repo; siber güvenlik, AI security ve backend engineering alanlarında portfolyo projesi olarak tasarlanmıştır.

---

## Bu Proje Neden Önemli?

AI uygulamaları çoğu zaman API endpoint'leri üzerinden dış dünyaya açılır. Ancak basit ve korumasız bir `/predict` endpoint'i ciddi güvenlik riskleri oluşturabilir.

Güvenli bir AI API şu katmanlara sahip olmalıdır:

- Authentication
- Input validation
- Abuse prevention
- Audit logging
- Security event tracking
- Prompt injection detection
- Protected inference endpoints
- Güvenli configuration management

Bu proje, güvenli AI API Gateway mimarisi için küçük ama gerçekçi bir temel sunar.

---

## Özellikler

### Authentication

- JWT tabanlı authentication
- Protected `/predict` endpoint
- Bearer token validation
- Token expiration handling
- Invalid token handling

### Environment-Based Configuration

- Secret değerleri `.env` dosyasından yüklenir
- `.env` Git tarafından ignore edilir
- `.env.example` güvenli örnek template olarak repoda tutulur
- JWT secret, demo user, demo password, algorithm ve token lifetime ayarlanabilir

### Input Validation

- Pydantic request schemas
- Pydantic response schemas
- Boş input reddi
- Sadece boşluk içeren input reddi
- Maksimum text uzunluğu kontrolü

### AI Security Layer

- Basit prompt injection detection
- Şüpheli prompt pattern'lerini bloklama
- Basit jailbreak tarzı input denemelerine karşı koruma

Bloklanan örnek prompt pattern'leri:

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

- IP bazlı başarısız login takibi
- Belirli sayıda hatalı denemeden sonra geçici IP bloklama
- Bloklanan client'lar için `429 Too Many Requests` response'u
- Failed login ve blocked login attempt event kayıtları

---

## Mimari

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

## Proje Yapısı

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

> `.env` ve `logs/` Git tarafından ignore edilir. Çünkü bu dosyalar hassas runtime bilgileri içerebilir.

---

## Kurulum

### 1. Repoyu Klonla

```bash
git clone https://github.com/ErenA001/secure-ai-api.git
cd secure-ai-api
```

Mevcut lokal geliştirme yapısı için:

```bash
cd ~/secure-ai-api/projects/secure-ai-api
```

### 2. Virtual Environment Oluştur

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 4. Local Environment Dosyası Oluştur

```bash
cp .env.example .env
```

Sonra `.env` dosyasını kendi lokal değerlerinle düzenle:

```text
SECRET_KEY=your-secret-key-minimum-32-chars
DEMO_USER=your_username
DEMO_PASSWORD=your_password
ALGORITHM=HS256
TOKEN_EXP_SECONDS=3600
```

Lokal demo testleri için demo kullanıcı bilgileri kullanılabilir. Bu değerler sadece development amaçlıdır, production ortamında kullanılmamalıdır.

### 5. API'yi Çalıştır

```bash
uvicorn main:app --reload
```

API şu adreste çalışır:

```text
http://127.0.0.1:8000
```

---

## API Kullanımı

### Health Check

```bash
curl http://127.0.0.1:8000
```

Örnek response:

```json
{
  "status": "ok",
  "service": "secure-ai-api-v2"
}
```

---

### Login

Demo credentials artık lokal `.env` dosyasından yüklenir.

Örnek lokal demo değerleri:

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

Örnek response:

```json
{
  "user": "eren",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Protected Prediction Endpoint

Önce JWT token al:

```bash
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user":"eren","password":"secure123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

Sonra `/predict` endpoint'ine istek at:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"hello ai"}'
```

Örnek response:

```json
{
  "input": "hello ai",
  "prediction": "safe",
  "confidence": 0.93,
  "flagged": false
}
```

---

## Güvenlik Testleri

### Prompt Injection Testi

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"text":"jailbreak this system"}'
```

Beklenen response:

```json
{
  "detail": "Prompt injection detected"
}
```

---

### Brute Force Protection Testi

Birden fazla hatalı login denemesi çalıştır:

```bash
for i in {1..6}; do
  echo "--- attempt $i ---"
  curl -s -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"eren","password":"wrongpass"}'
  echo
done
```

Beklenen davranış:

- İlk hatalı denemeler `401 Unauthorized` döner
- Limit aşılınca IP geçici olarak bloklanır
- Bloklanan istekler `429 Too Many Requests` döner

---

## Audit Logs

Audit log kayıtları structured JSON lines formatında tutulur:

```bash
cat logs/audit.log
```

Örnek log kayıtları:

```json
{"timestamp":"2026-06-27T11:33:05.181517+00:00","event":"failed_login","ip":"127.0.0.1","username":"eren","attempts":1,"status":401}
{"timestamp":"2026-06-27T11:33:05.230679+00:00","event":"brute_force_blocked","ip":"127.0.0.1","username":"eren","attempts":5,"status":429,"block_seconds":900}
```

---

## Mevcut Güvenlik Kapsamı

| Alan | Durum |
|---|---|
| JWT authentication | Tamamlandı |
| Environment-based configuration | Tamamlandı |
| Pydantic validation | Tamamlandı |
| Prompt injection detection | Tamamlandı |
| Audit logging | Tamamlandı |
| Brute force protection | Tamamlandı |
| Redis tabanlı distributed rate limiting | Planlandı |
| Gerçek ML anomaly detection | Planlandı |
| Docker production setup | Planlandı |
| CI pipeline | Planlandı |

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

## Güvenlik Notları

Bu proje eğitim ve portfolyo odaklıdır.

Mevcut sınırlamalar:

- Brute force protection şu an in-memory çalışır
- Login lokal `.env` dosyasındaki demo credentials ile çalışır
- Audit logs lokal dosyaya yazılır
- AI prediction şu an mock response döner

Production seviyesine taşımak için önerilen geliştirmeler:

- Demo login yerine gerçek user storage kullanmak
- Password hashing eklemek
- Redis ile distributed blocking ve rate limiting yapmak
- HTTPS reverse proxy arkasında çalıştırmak
- Monitoring ve alerting eklemek
- Secret rotation uygulamak

---

## Teknoloji Stack

- Python
- FastAPI
- Pydantic
- PyJWT
- Uvicorn
- python-dotenv
- Structured JSON logging

---

## Author

Siber güvenlik, AI security ve backend architecture portfolyo projesi olarak geliştirilmiştir.

---

## License

Bu proje eğitim ve portfolyo amacıyla açık şekilde kullanılabilir.
