# Gateway Service - Complete Implementation

API Gateway for IYTE Soru Botu microservices architecture.

## 📁 Directory Structure

```
src/gateway/src/
├── config/
│   └── settings.py              # Configuration with pydantic-settings
├── infrastructure/
│   ├── cache/
│   │   └── redis_client.py      # Redis cache client
│   └── http_client/
│       └── service_client.py    # HTTP client for backend services
├── middleware/
│   ├── auth.py                  # JWT authentication middleware
│   └── rate_limit.py            # Rate limiting middleware
└── presentation/
    ├── routes/
    │   ├── auth_proxy.py        # Proxy to auth service
    │   ├── chat_proxy.py        # Proxy to chat service
    │   ├── document_proxy.py    # Proxy to document service
    │   └── health.py            # Health check endpoints
    └── main.py                  # FastAPI application
```

## ✨ Features

### 1. **Request Proxying**
- Routes requests to appropriate microservices
- Maintains request/response format
- Handles service unavailability gracefully

### 2. **Authentication**
- JWT token verification
- User session caching (5 minutes)
- Token extraction from Authorization header
- Automatic token propagation to backend services

### 3. **Rate Limiting**
- Per-user rate limiting using Redis
- Configurable limits (default: 100 requests/60 seconds)
- Returns 429 Too Many Requests when exceeded
- Rate limit info available per identifier

### 4. **Session Caching**
- Redis-based session storage
- 1-hour session expiration
- Reduces load on auth service
- Fast session lookup

### 5. **CORS Support**
- Configurable allowed origins
- Full credential support
- All methods and headers allowed

### 6. **Health Checks**
- Gateway health endpoint
- Backend service health proxying
- Redis connectivity check
- Component-level status

## 🔌 API Endpoints

### Root
- `GET /` - Service information and endpoint list
- `GET /health` - Gateway health check

### Auth Service Proxy (`/api/v1/auth`)
- `POST /auth/register` - User registration (rate limited)
- `POST /auth/login` - User login (rate limited)
- `GET /auth/health` - Auth service health

### Chat Service Proxy (`/api/v1/chat`) 🔒 Authenticated
- `POST /chat/create` - Create new chat
- `POST /chat/send-message` - Send message
- `GET /chat/` - Get user's chats
- `GET /chat/{chat_id}/messages` - Get chat history
- `GET /chat/health` - Chat service health

### Document Service Proxy (`/api/v1/documents`) 🔒 Authenticated
- `POST /documents/upload` - Upload document
- `GET /documents/` - List user documents
- `GET /documents/{document_id}` - Get document
- `DELETE /documents/{document_id}` - Delete document
- `GET /documents/health` - Document service health

🔒 = Requires JWT authentication

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
# Server
HOST=0.0.0.0
PORT=8000
PROJECT_NAME=IYTE Soru Botu Gateway
API_VERSION=v1

# Service URLs
AUTH_SERVICE_URL=http://localhost:8081
CHAT_SERVICE_URL=http://localhost:8080
DOCUMENT_SERVICE_URL=http://localhost:8082

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
SESSION_EXPIRE_SECONDS=3600

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 🚀 Running the Gateway

### Local Development

```bash
cd src/gateway

# Install dependencies
uv sync

# Run the service
uv run -m src.presentation.main
```

Access at: http://localhost:8000

### With Docker

```bash
# Using docker-compose
docker-compose up -d gateway

# View logs
docker-compose logs -f gateway
```

## 📊 Request Flow

```
Client
  │
  ├─→ POST /api/v1/auth/register
  │     │
  │     ├─→ Rate Limit Check (Redis)
  │     └─→ Forward to Auth Service
  │           └─→ Return Response
  │
  ├─→ POST /api/v1/chat/create (with JWT)
  │     │
  │     ├─→ Verify JWT Token
  │     ├─→ Check Session Cache (Redis)
  │     ├─→ Rate Limit Check (per user)
  │     └─→ Forward to Chat Service
  │           └─→ Return Response
  │
  └─→ GET /api/v1/documents/ (with JWT)
        │
        ├─→ Verify JWT Token
        ├─→ Check Session Cache (Redis)
        ├─→ Rate Limit Check (per user)
        └─→ Forward to Document Service
              └─→ Return Response
```

## 🔐 Security Features

### 1. JWT Verification
- Verifies tokens before forwarding requests
- Caches user data to reduce auth service load
- Automatically rejects expired tokens

### 2. Rate Limiting
- Prevents abuse and DDoS attacks
- Per-user limits for authenticated endpoints
- Per-IP limits for public endpoints
- Configurable thresholds

### 3. Session Management
- Secure session caching
- Automatic expiration
- Session invalidation support

## 🧪 Testing the Gateway

### 1. Test Authentication Flow

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepass123"}'

# Response includes access_token
```

### 2. Test Authenticated Endpoints

```bash
# Use token from registration/login
TOKEN="your_access_token_here"

# Create a chat
curl -X POST http://localhost:8000/api/v1/chat/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat"}'
```

### 3. Test Rate Limiting

```bash
# Make 100+ requests rapidly
for i in {1..101}; do
  curl -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"user$i@example.com\", \"password\": \"pass123\"}"
done

# Should get 429 Too Many Requests after limit
```

### 4. Check Health

```bash
# Gateway health
curl http://localhost:8000/health

# All services health
curl http://localhost:8000/api/v1/auth/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/documents/health
```

## 🔄 Middleware Pipeline

Each request goes through this pipeline:

1. **CORS Middleware** - Handle cross-origin requests
2. **Rate Limit Middleware** - Check request limits
3. **Auth Middleware** - Verify JWT (if required)
4. **Route Handler** - Proxy to backend service
5. **Response** - Return to client

## 📈 Performance Optimizations

1. **Connection Pooling** - httpx async client reuses connections
2. **Session Caching** - Reduces auth service load
3. **Async/Await** - Non-blocking I/O operations
4. **Redis Caching** - Fast session and rate limit lookups

## 🛠️ Adding New Routes

To proxy a new endpoint:

```python
# In appropriate proxy file
@router.post("/new-endpoint")
async def new_endpoint(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(
        request, identifier=user["user_id"]
    )

    # Get request body
    body = await request.json()

    # Forward to service
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    response = await service_client.post(
        "/path/to/endpoint",
        json_data=body,
        headers=headers
    )

    return JSONResponse(
        status_code=response.status_code,
        content=response.json(),
    )
```

## 🐛 Troubleshooting

### Gateway can't connect to Redis
```bash
# Check Redis is running
docker-compose ps gateway-redis

# Test Redis connection
redis-cli -h localhost -p 6380 ping
```

### Backend service unavailable
```bash
# Check service health
curl http://localhost:8081/api/v1/auth/health

# Check docker-compose
docker-compose ps
```

### Rate limiting issues
```bash
# Check Redis keys
redis-cli -h localhost -p 6380
KEYS rate_limit:*

# Clear rate limits
redis-cli -h localhost -p 6380 FLUSHDB
```

## 📦 Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **httpx** - Async HTTP client
- **redis** - Cache and rate limiting
- **pydantic-settings** - Configuration
- **pyjwt** - JWT verification

## 🔜 Future Enhancements

- [ ] Request/Response logging
- [ ] Metrics collection (Prometheus)
- [ ] Circuit breaker pattern
- [ ] Request retries with exponential backoff
- [ ] WebSocket support
- [ ] GraphQL gateway support
- [ ] API versioning support
- [ ] Request transformation
- [ ] Response caching
