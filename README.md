<div align="center">

# 🔥 FastAPI-Katharsis

**Production-ready FastAPI backend template for building scalable REST APIs**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗄️ **PostgreSQL** | Robust relational database with async support |
| 🔐 **JWT Auth** | Secure token-based authentication |
| ⚡ **Celery** | Distributed background task processing |
| 🐳 **Docker** | Containerized deployment with Docker Compose |
| 🧹 **Pre-commit** | Automated code quality hooks |
| 🧅 **Clean Architecture** | Onion/Hexagonal architecture pattern |

---

## 🏗️ Project Structure

```
📦 FastAPI-Katharsis
├── 📂 src/
│   ├── 📂 presentation/              # Outer layer (API, CLI)
│   │   ├── 📂 api/
│   │   │   ├── 📂 routers/           # FastAPI endpoints (Controllers)
│   │   │   ├── 📂 schemas/           # Pydantic models for Request/Response
│   │   │   └── 📂 dependencies/      # Depends() providers
│   │   └── 📄 main.py                # Application entry point
│   │
│   ├── 📂 application/               # Use cases layer (Application Business Rules)
│   │   ├── 📂 use_cases/             # Action logic (CreateUser, GetOrder, etc.)
│   │   ├── 📂 dto/                   # Data Transfer Objects (pure data)
│   │   └── 📂 interfaces/            # Abstract interfaces (Ports) for repos & services
│   │
│   ├── 📂 domain/                    # Core layer (Enterprise Business Rules)
│   │   ├── 📂 models/                # Business entities (not ORM models!)
│   │   ├── 📂 events/                # Domain events
│   │   ├── 📄 exceptions.py          # Domain-specific errors
│   │   └── 📄 services.py            # Pure domain logic (beyond simple CRUD)
│   │
│   └── 📂 infrastructure/            # Implementation layer (Frameworks & Drivers)
│       ├── 📂 db/
│       │   ├── 📂 models/            # SQLAlchemy/Tortoise ORM models
│       │   ├── 📂 repositories/      # Implementation of application interfaces
│       │   └── 📄 session.py         # Database connection
│       ├── 📂 external/              # External API clients (Stripe, S3, etc.)
│       └── 📄 config.py              # Settings (Pydantic Settings)
│
├── 📂 tests/                         # Test suite
├── 📂 alembic/                       # Database migrations
├── 📄 pyproject.toml                 # Project dependencies & config
└── 🐳 Dockerfile                     # Container definition
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/FastAPI-Katharsis.git
cd FastAPI-Katharsis

# Start with Docker Compose
docker compose up -d

# Or run locally
pip install -e .
uvicorn src.presentation.main:app --reload
```

---

## 📐 Architecture Overview

This project follows **Clean Architecture** (Onion Architecture) principles:

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION                         │
│              (API Routes, Schemas, CLI)                 │
├─────────────────────────────────────────────────────────┤
│                    APPLICATION                          │
│            (Use Cases, DTOs, Interfaces)                │
├─────────────────────────────────────────────────────────┤
│                      DOMAIN                             │
│         (Entities, Events, Business Logic)              │
├─────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE                        │
│          (Database, External Services, Config)          │
└─────────────────────────────────────────────────────────┘
```

> **Dependencies flow inward** — outer layers depend on inner layers, never the reverse.

---

## 🛣️ API Routes

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register a new user | ❌ |
| POST | `/login` | Login and get tokens | ❌ |
| POST | `/refresh` | Refresh access token | ❌ |
| GET | `/me` | Get current user info | ✅ |

### Math Operations (`/api/v1/math`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/factorial` | Calculate factorial of a number | ✅ |
| POST | `/prime` | Check if number is prime | ✅ |
| POST | `/power` | Calculate base^exponent | ✅ |

### Health

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Root endpoint | ❌ |
| GET | `/health` | Health check | ❌ |

### Documentation

| Endpoint | Description |
|----------|-------------|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI schema |

---

<div align="center">

**Built with ❤️ for modern Python development**

</div>
