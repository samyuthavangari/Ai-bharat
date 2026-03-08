# 🇮🇳 JanSahay AI

**Voice-First Multilingual AI Assistant for Government Scheme Access in India**

> Helping 1.4 billion citizens discover government schemes, check eligibility, and get application guidance — in their own language.

## 🎯 What It Does

| Feature | Description |
|---------|-------------|
| 🎤 **Voice First** | Speak in Hindi, Bengali, Tamil, Telugu, or Marathi |
| 🌐 **6 Languages** | Full UI + NLP in English, Hindi, Bengali, Tamil, Telugu, Marathi |
| 🤖 **AI Recommendations** | ML-powered scheme matching based on user profile |
| ✅ **Eligibility Check** | Instant pass/fail with detailed reasons |
| 📋 **Document Guide** | What documents you need + how to get them |
| 💬 **WhatsApp Bot** | Full functionality via WhatsApp (Twilio) |
| 📶 **Low Bandwidth** | Redis caching, GZip, CDN — works in slow networks |
| 📊 **Analytics Dashboard** | Admin panel with usage metrics and trends |

## 🏗️ Architecture

```
React Frontend ←→ Nginx ←→ FastAPI Backend ←→ PostgreSQL / Redis
                                    ↕
                            Google Cloud Speech (Voice)
                            Twilio (WhatsApp)
```

## 📂 Project Structure

```
jansahay-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # 8 API route modules
│   │   ├── auth/            # OAuth 2.0 + RBAC
│   │   ├── middleware/      # Rate limiting
│   │   ├── models/          # SQLAlchemy ORM (User, Scheme, Analytics)
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Core AI services (NLP, Voice, ML, Eligibility)
│   │   ├── seed/            # 30+ real scheme data
│   │   ├── config.py        # Environment config
│   │   ├── database.py      # Async PostgreSQL
│   │   ├── redis_client.py  # Redis cache utilities
│   │   └── main.py          # FastAPI app entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # 5 pages (Home, Schemes, Eligibility, Chat, Dashboard)
│   │   ├── index.css        # Premium dark theme design system
│   │   ├── services/api.js  # API client
│   │   └── i18n/            # 6-language translations
│   ├── Dockerfile
│   └── nginx.conf
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/dashboards/
├── docs/                    # 8 technical documents
├── docker-compose.yml       # 7-service stack
├── nginx.conf               # Reverse proxy + load balancer
└── .github/workflows/ci.yml # CI/CD pipeline
```

## 🚀 Quick Start

### Development (Local)

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# 2. Frontend
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)

```bash
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3001
```

### AWS Deployment

See [docs/deployment.md](docs/deployment.md) for full AWS ECS deployment guide.

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System design with Mermaid diagrams |
| [Database Schema](docs/database-schema.md) | ER diagram + table details |
| [API Reference](docs/api-reference.md) | All 25+ endpoints |
| [ML Model Design](docs/ml-model-design.md) | NLP, Recommendation, Eligibility engines |
| [Deployment](docs/deployment.md) | AWS step-by-step guide |
| [Cost Estimation](docs/cost-estimation.md) | 3-tier pricing ($135 → $7,992/mo) |
| [Scalability](docs/scalability.md) | 10K → 10M users plan |
| [Security](docs/security.md) | OWASP compliance + encryption |

## 🏛️ 30+ Government Schemes

PM-KISAN, Ayushman Bharat, PMAY, Ujjwala, MGNREGA, Jan Dhan, MUDRA, Sukanya Samriddhi, Skill India, Atal Pension, Kisan Credit Card, Free Ration, Ladli Behna, and many more.

## 🛡️ Security

- HTTPS/TLS 1.3 everywhere
- OAuth 2.0 + JWT authentication
- bcrypt password hashing (12 rounds)
- RBAC (citizen, admin, gov_official)
- Rate limiting (60 req/min)
- Input validation (Pydantic)
- OWASP Top 10 compliant

## 📜 License

Built with ❤️ for Bharat
