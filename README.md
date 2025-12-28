# 🎓 IYTE Soru Botu - Backend

A FastAPI-based microservices backend application for IYTE Question Bot, enabling students to get instant answers from their course documents using AI.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7-green.svg)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)

## 🛠 Tech Stack

### Core Framework
- **Framework**: FastAPI 0.128.0
- **Language**: Python 3.12+
- **Package Manager**: uv (ultra-fast Python package installer)
- **ASGI Server**: Uvicorn

### Databases
- **PostgreSQL 16** - Auth & Chat services
- **MongoDB 7** - Document storage
- **Redis 7** - Session caching & rate limiting

### AI & Vector Storage
- **Google Gemini API** - AI-powered chat responses
- **ChromaDB** - Vector database for semantic search
- **LangChain** - LLM orchestration framework

### Storage & Communication
- **MinIO** - S3-compatible object storage for documents
- **gRPC** - Inter-service communication
- **httpx** - Async HTTP client

### Development Tools
- **Ruff** - Fast Python linter
- **Mypy** - Static type checker
- **Docker & Docker Compose** - Containerization

## 🏗 Architecture

This project follows **microservices architecture** with **Domain-Driven Design (DDD)** principles:

```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway (8000)                    │
│          Rate Limiting • JWT Auth • CORS                 │
└─────────────┬──────────────┬──────────────┬─────────────┘
              │              │              │
    ┌─────────▼────┐ ┌──────▼───────┐ ┌───▼──────────┐
    │ Auth Service │ │ Chat Service │ │   Document   │
    │    (8081)    │ │    (8080)    │ │   Service    │
    │              │ │              │ │    (8082)    │
    │  PostgreSQL  │ │  PostgreSQL  │ │   MongoDB    │
    │              │ │   ChromaDB   │ │    MinIO     │
    │              │ │   Gemini AI  │ │    gRPC      │
    └──────────────┘ └──────────────┘ └──────────────┘
```

### Services Overview

#### 🔐 **Gateway Service** (Port 8000)
- Single entry point for all client requests
- JWT authentication and validation
- Rate limiting with Redis
- Request routing to microservices
- Session caching

#### 👤 **Auth Service** (Port 8081)
- User registration and authentication
- JWT token generation and refresh
- Password hashing with bcrypt
- Email verification (SMTP)
- PostgreSQL for user data

#### 💬 **Chat Service** (Port 8080)
- AI-powered Q&A using Google Gemini
- Chat history management
- Vector similarity search with ChromaDB
- Document context retrieval via gRPC
- Conversation threading

#### 📄 **Document Service** (Port 8082)
- Document upload and storage (MinIO)
- Document metadata in MongoDB
- File processing and indexing
- gRPC server for document retrieval
- Multi-format support

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12** or higher ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/get-started))
- **uv** - Fast Python package installer ([Install](https://github.com/astral-sh/uv))
- **Git** ([Download](https://git-scm.com/))
- **Google Gemini API Key** ([Get API Key](https://makersuite.google.com/app/apikey))

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/IYTE-Yazilim-Toplulugu/iyte-soru-botu.git
cd iyte-soru-botu
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE=3600
REFRESH_TOKEN_EXPIRE=2592000

# Google AI API
GOOGLE_API_KEY=your-google-gemini-api-key

# MinIO Configuration
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Frontend Configuration
FRONTEND_MAIN_ORIGIN=http://localhost:3000

# SMTP Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 3. Start All Services with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

This will start:
- **Gateway** on port 8000
- **Auth Service** on port 8081
- **Chat Service** on port 8080
- **Document Service** on port 8082
- **PostgreSQL** (Auth DB) on port 5433
- **PostgreSQL** (Chat DB) on port 5432
- **MongoDB** on port 27017
- **Redis** (Gateway) on port 6380
- **Redis** (Chat) on port 6379
- **ChromaDB** on port 8001
- **MinIO** on ports 9000 (API) and 9001 (Console)

### 4. Access the Application

- **API Gateway**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin/admin)
- **ChromaDB**: http://localhost:8001

### 5. Verify Installation

```bash
# Check gateway health
curl http://localhost:8000/health

# Check all services
curl http://localhost:8000/api/v1/auth/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/documents/health
```

## 📁 Project Structure

```
iyte-soru-botu/
├── src/
│   ├── gateway/                    # API Gateway Service
│   │   ├── src/
│   │   │   ├── config/             # Configuration
│   │   │   ├── infrastructure/     # Redis, HTTP clients
│   │   │   ├── middleware/         # Auth, rate limiting
│   │   │   └── presentation/       # Routes, main app
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   ├── services/
│   │   ├── auth/                   # Authentication Service
│   │   │   ├── src/
│   │   │   │   ├── domain/         # Business logic, entities
│   │   │   │   ├── application/    # Use cases, DTOs
│   │   │   │   ├── infrastructure/ # Database, repositories
│   │   │   │   └── presentation/   # API routes, main app
│   │   │   ├── Dockerfile
│   │   │   └── pyproject.toml
│   │   │
│   │   ├── chat/                   # Chat Service
│   │   │   ├── src/
│   │   │   │   ├── domain/         # Chat entities, events
│   │   │   │   ├── application/    # Chat handlers, DTOs
│   │   │   │   ├── infrastructure/ # AI, vector DB, gRPC
│   │   │   │   └── presentation/   # Chat routes
│   │   │   └── pyproject.toml
│   │   │
│   │   └── document/               # Document Service
│   │       ├── src/
│   │       │   ├── domain/         # Document entities
│   │       │   ├── application/    # Document handlers
│   │       │   ├── infrastructure/ # MongoDB, MinIO, gRPC
│   │       │   └── presentation/   # Document routes
│   │       └── pyproject.toml
│   │
│   └── libs/
│       └── shared-kernel/          # Shared domain logic
│           ├── shared_kernel/
│           │   ├── entities/       # Base entities
│           │   ├── events/         # Domain events
│           │   ├── exceptions/     # Common exceptions
│           │   ├── interfaces/     # Repository interfaces
│           │   ├── models/         # API response models
│           │   └── value_objects/  # Value objects
│           └── pyproject.toml
│
├── deployment/
│   └── docker/                     # Production Dockerfiles
│       ├── auth.Dockerfile
│       ├── chat.Dockerfile
│       ├── document.Dockerfile
│       └── gateway.Dockerfile
│
├── docker-compose.yml              # Development orchestration
├── .env.example                    # Environment template
└── README.md
```

### Architecture Layers (DDD)

Each service follows **Clean Architecture** with **Domain-Driven Design**:

- **Domain Layer** - Core business logic, entities, and domain events
- **Application Layer** - Use cases, DTOs, handlers (business orchestration)
- **Infrastructure Layer** - Database, external APIs, messaging
- **Presentation Layer** - API routes, HTTP controllers, serialization

## 👥 Development Workflow

### Running Services Locally

#### Option 1: Run Individual Service

```bash
# Navigate to service directory
cd src/services/auth

# Install dependencies
uv sync

# Run the service
uv run -m src.presentation.main
```

#### Option 2: Run All Services with Docker

```bash
# Build and start all services
docker-compose up --build

# Start specific service
docker-compose up auth

# Rebuild after code changes
docker-compose up --build chat
```

### Working on an Issue

1. **Find your assigned issue** on the Project Board

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/issue-X-task-name
   ```

3. **Make your changes** following DDD principles

4. **Run linting and type checking**:
   ```bash
   # Format code
   ruff format .

   # Check linting
   ruff check .

   # Type checking
   mypy src/
   ```

5. **Test your changes**:
   ```bash
   # Manual testing with curl/Postman
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@iyte.edu.tr", "password": "SecurePass123!"}'
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add user authentication endpoint"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

7. **Push and create Pull Request**:
   ```bash
   git push origin feature/issue-X-task-name
   ```

### Branch Strategy

- `main` - Production-ready code
- `dev` - Development branch (default)
- `feature/issue-X-*` - Feature branches

## 📚 API Documentation

### Base URL
All requests go through the **API Gateway**: `http://localhost:8000`

### Authentication Endpoints

```http
POST   /api/v1/auth/register        # User registration
POST   /api/v1/auth/login           # User login
POST   /api/v1/auth/logout          # User logout
POST   /api/v1/auth/refresh         # Refresh access token
GET    /api/v1/auth/verify-email?token={token}
POST   /api/v1/auth/resend-verification
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/health          # Health check
```

### Chat Endpoints (🔒 Requires Authentication)

```http
POST   /api/v1/chat/create          # Create new chat session
POST   /api/v1/chat/send-message    # Send message to AI
GET    /api/v1/chat/                # Get user's chats
GET    /api/v1/chat/{chat_id}/messages  # Get chat history
DELETE /api/v1/chat/{chat_id}       # Delete chat
GET    /api/v1/chat/health          # Health check
```

### Document Endpoints (🔒 Requires Authentication)

```http
POST   /api/v1/documents/upload     # Upload document (PDF, DOCX, TXT)
GET    /api/v1/documents/           # List user's documents
GET    /api/v1/documents/{document_id}  # Get document details
DELETE /api/v1/documents/{document_id}  # Delete document
GET    /api/v1/documents/health     # Health check
```

🔒 = Requires JWT token in `Authorization: Bearer <token>` header

### Example Usage

#### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@iyte.edu.tr",
    "password": "SecurePass123!",
    "first_name": "Ahmet",
    "last_name": "Yılmaz"
  }'
```

#### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@iyte.edu.tr",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Upload a Document

```bash
TOKEN="your_access_token_here"

curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/document.pdf" \
  -F "title=Linear Algebra Notes" \
  -F "course=MATH201"
```

#### 4. Ask a Question

```bash
curl -X POST http://localhost:8000/api/v1/chat/send-message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "01HW8...",
    "message": "What is eigenvalue decomposition?"
  }'
```

For detailed API documentation with interactive testing, visit:
**Swagger UI**: http://localhost:8000/docs

## 🧪 Testing

### Manual Testing

```bash
# Test authentication flow
./scripts/test-auth.sh

# Test chat flow
./scripts/test-chat.sh

# Test document upload
./scripts/test-documents.sh
```

### Service Health Checks

```bash
# Check all services
docker-compose ps

# Test individual service health
curl http://localhost:8000/api/v1/auth/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/documents/health
```

### Database Connections

```bash
# Connect to Auth DB
docker exec -it iyte-auth-db psql -U postgres -d auth_db

# Connect to Chat DB
docker exec -it iyte-chat-db psql -U postgres -d chat_db

# Connect to MongoDB
docker exec -it iyte-document-db mongosh -u root -p root
```

### Redis Cache

```bash
# Connect to Gateway Redis
docker exec -it iyte-gateway-redis redis-cli

# View cached sessions
KEYS session:*

# View rate limits
KEYS rate_limit:*
```

## 🎨 Coding Standards

### Python Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions small and focused

### Code Formatting

```bash
# Format code with Ruff
ruff format .

# Check linting issues
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

### Type Checking

```bash
# Run Mypy type checker
mypy src/

# Type check specific service
mypy src/services/auth/
```

### Domain-Driven Design

- **Entities** - Objects with identity (User, Chat, Document)
- **Value Objects** - Immutable objects without identity (Email, Password)
- **Aggregates** - Cluster of entities (User Aggregate)
- **Repositories** - Data access abstraction
- **Domain Events** - Significant domain occurrences
- **Use Cases** - Application-specific business rules

### Security Best Practices

- Never log sensitive data (passwords, tokens)
- Validate all user inputs with Pydantic
- Use parameterized queries (SQLModel handles this)
- Hash passwords with bcrypt (cost factor 12+)
- Use ULID for IDs (sortable, time-based UUIDs)
- Follow OWASP Top 10 guidelines

## 🐛 Common Issues

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use docker-compose to stop
docker-compose down
```

### Database Connection Issues

```bash
# Check if databases are running
docker-compose ps

# Restart specific database
docker-compose restart auth-db

# View database logs
docker-compose logs auth-db
```

### Redis Connection Issues

```bash
# Check Redis status
docker-compose ps gateway-redis

# Test Redis connection
docker exec -it iyte-gateway-redis redis-cli ping
```

### MinIO Issues

```bash
# Access MinIO console
open http://localhost:9001

# Check bucket exists
docker exec -it iyte-minio mc ls myminio/

# Recreate bucket
docker-compose restart minio-init
```

### Service Not Responding

```bash
# Check service logs
docker-compose logs -f auth

# Rebuild and restart
docker-compose up --build auth

# Check service health directly
curl http://localhost:8081/api/v1/auth/health
```

## 📦 Dependencies Management

### Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Working with Dependencies

```bash
# Install dependencies
uv sync

# Add new dependency
uv add fastapi

# Add dev dependency
uv add --dev pytest

# Update dependencies
uv lock --upgrade
```

## 📖 Additional Resources

### Framework Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

### AI & Vector DB
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Gemini API](https://ai.google.dev/docs)

### Architecture Patterns
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Microservices Pattern](https://microservices.io/)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is developed by IYTE Yazılım Topluluğu for educational purposes.

## 👨‍💻 Team

**Web Team**: DrHalley, UlasGokkaya, neonid0, Xerkara, AliKemalMiloglu, bdurgut06, ygt-ernsy, ErkanArikan

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact: yazilim@iyte.edu.tr
- Discord: [IYTE Yazılım Topluluğu](https://discord.gg/iyte-yazilim)

---

Made with ❤️ by IYTE Yazılım Topluluğu
