# Document Service - Complete Implementation

Document management service with MongoDB and MinIO storage for IYTE Soru Botu.

## 📁 Directory Structure

```
src/services/document/src/
├── domain/                          # Business Logic Layer
│   ├── entities/
│   │   └── document.py             # Document AggregateRoot
│   ├── value_objects/
│   │   ├── document_metadata.py    # File metadata (name, size, type)
│   │   └── file_reference.py       # MinIO storage reference
│   ├── enums/
│   │   ├── document_status.py      # Status enum (pending, processing, etc.)
│   │   └── document_type.py        # Type enum (pdf, word, excel, etc.)
│   ├── events/
│   │   ├── document_uploaded.py    # Upload event
│   │   └── document_deleted.py     # Delete event
│   ├── interfaces/
│   │   ├── document_repository.py  # Repository interface
│   │   └── storage_service.py      # MinIO interface
│   └── exceptions/
│       └── document_exceptions.py  # Domain exceptions
├── application/                     # Use Cases Layer
│   ├── commands/
│   │   ├── upload_document.py      # Upload command + handler
│   │   └── delete_document.py      # Delete command + handler
│   └── queries/
│       ├── get_user_documents.py   # List documents query
│       └── get_document.py         # Get document query
├── infrastructure/                  # Technical Implementation
│   ├── data/
│   │   ├── mongodb.py              # MongoDB client
│   │   └── repositories/
│   │       └── document_repository.py # MongoDB repository
│   ├── storage/
│   │   └── minio_service.py        # MinIO service
│   └── config/
│       └── settings.py             # Configuration
└── presentation/                    # HTTP API Layer
    ├── routes/
    │   └── documents.py            # FastAPI routes
    └── main.py                     # Application entry point
```

## ✨ Shared-Kernel Integration

All components use shared-kernel classes:

- ✅ **Entities**: `Document` extends `AggregateRoot[str]`
- ✅ **Value Objects**: `DocumentMetadata`, `FileReference` extend `ValueObject`
- ✅ **Events**: `DocumentUploadedEvent`, `DocumentDeletedEvent` extend `DomainEvent`
- ✅ **Repository**: `IDocumentRepository` extends `IRepository[str, Document]`
- ✅ **CQRS**: Commands/Queries implement `IRequest[ApiResponse[T]]`
- ✅ **Handlers**: Extend `IRequestHandler[Command, Response]`
- ✅ **Responses**: Use `ApiResponse[T]` and `ResponseCode`
- ✅ **Exceptions**: Extend `DomainException`

## 🎯 Features

### 1. **Document Upload**
- Multipart file upload support
- Automatic file validation (size, type)
- MinIO storage integration
- MongoDB metadata storage
- File size limit: 100 MB

### 2. **Document Download**
- Streaming file download
- Presigned URL generation
- Content-Disposition headers
- Access control

### 3. **Document Management**
- List user documents
- Get document details
- Soft delete with event
- Status tracking

### 4. **Storage Management**
- MinIO object storage
- Automatic bucket creation
- File existence checks
- Secure file URLs

### 5. **Status Tracking**
```python
class DocumentStatus(str, Enum):
    PENDING = "pending"      # Just uploaded
    PROCESSING = "processing" # Being processed
    COMPLETED = "completed"   # Ready to use
    FAILED = "failed"         # Processing failed
    DELETED = "deleted"       # Soft deleted
```

## 🔌 API Endpoints

### Document Management (`/api/v1/documents`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a document |
| GET | `/` | List user's documents |
| GET | `/{document_id}` | Get document details |
| GET | `/{document_id}/download` | Download document file |
| DELETE | `/{document_id}` | Delete document |
| GET | `/health` | Health check |

## 🗄️ MongoDB Schema

### Documents Collection

```json
{
  "_id": "01HQXXX...",
  "user_id": "01HQXXX...",
  "metadata": {
    "filename": "report.pdf",
    "file_size": 1024000,
    "content_type": "application/pdf"
  },
  "file_reference": {
    "bucket": "documents",
    "path": "users/01HQXXX.../report.pdf",
    "url": "/documents/01HQXXX.../download"
  },
  "status": "completed",
  "document_type": "pdf",
  "parsed_content": "...",
  "error_message": null,
  "created_at": "2025-01-15T10:00:00",
  "updated_at": "2025-01-15T10:01:00"
}
```

## 📦 MinIO Storage Structure

```
documents/
└── users/
    └── {user_id}/
        ├── file1.pdf
        ├── file2.docx
        └── file3.xlsx
```

## 🔧 Configuration

### Environment Variables

```env
# MongoDB
MONGODB_URL=mongodb://root:root@localhost:27017/
MONGODB_DATABASE=document_db

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=documents
MINIO_SECURE=false

# Server
HOST=0.0.0.0
PORT=8082
GRPC_PORT=50051
```

## 🚀 Running the Service

### Local Development

```bash
cd src/services/document

# Install dependencies
uv sync

# Run the service
uv run -m src.presentation.main
```

Access at: http://localhost:8082

### With Docker

```bash
# Using docker-compose
docker-compose up -d document

# View logs
docker-compose logs -f document
```

## 🧪 Testing the API

### 1. Upload a Document

```bash
curl -X POST http://localhost:8082/api/v1/documents/upload \
  -F "file=@/path/to/document.pdf" \
  -F "user_id=test-user"
```

Response:
```json
{
  "code": "SUCCESS",
  "message": "Document uploaded successfully",
  "data": {
    "document_id": "01HQXXX...",
    "filename": "document.pdf",
    "status": "pending"
  }
}
```

### 2. List Documents

```bash
curl http://localhost:8082/api/v1/documents/
```

### 3. Get Document Details

```bash
curl http://localhost:8082/api/v1/documents/{document_id}
```

### 4. Download Document

```bash
curl -O http://localhost:8082/api/v1/documents/{document_id}/download
```

### 5. Delete Document

```bash
curl -X DELETE http://localhost:8082/api/v1/documents/{document_id}
```

## 📊 Document Lifecycle

```
┌─────────┐
│ Upload  │
└────┬────┘
     │
     ▼
┌─────────────┐
│  PENDING    │ ──────┐
└─────────────┘       │
                      │
                      ▼
              ┌──────────────┐
              │  PROCESSING  │
              └──────┬───────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
  ┌─────────────┐        ┌─────────────┐
  │  COMPLETED  │        │   FAILED    │
  └──────┬──────┘        └─────────────┘
         │
         │ (soft delete)
         ▼
  ┌─────────────┐
  │   DELETED   │
  └─────────────┘
```

## 🔐 Security Features

### 1. File Validation
- File size limits (100 MB max)
- Content type validation
- Filename sanitization

### 2. Access Control
- User ownership checks
- Document access validation
- Soft delete support

### 3. Storage Security
- MinIO bucket policies
- Presigned URLs with expiration
- Secure file paths

## 📦 Dependencies

```toml
dependencies = [
    "fastapi>=0.128.0",          # Web framework
    "uvicorn>=0.40.0",           # ASGI server
    "motor>=3.0.0",              # Async MongoDB driver
    "minio>=7.2.0",              # MinIO client
    "python-multipart>=0.0.9",   # File upload support
    "python-ulid>=3.1.0",        # ID generation
    "pydantic-settings>=2.0.0",  # Configuration
    "shared-kernel",             # DDD library
    "grpcio>=1.60.0",            # gRPC support
    "grpcio-tools>=1.60.0",      # gRPC tools
]
```

## 🔜 Future Enhancements

### Document Processing
- [ ] PDF text extraction
- [ ] OCR for scanned documents
- [ ] Document preview generation
- [ ] Thumbnail creation

### gRPC Service
- [ ] Document processing service
- [ ] Batch upload support
- [ ] Real-time status updates
- [ ] Inter-service communication

### Advanced Features
- [ ] Document versioning
- [ ] Sharing and permissions
- [ ] Full-text search (Elasticsearch)
- [ ] Document tags and categories
- [ ] Virus scanning
- [ ] Compression support

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check MongoDB is running
docker-compose ps document-db

# Test connection
mongosh mongodb://root:root@localhost:27017/
```

### MinIO Connection Issues

```bash
# Check MinIO is running
docker-compose ps minio

# Access MinIO console
http://localhost:9001

# Test with mc client
mc alias set local http://localhost:9000 minioadmin minioadmin
mc ls local
```

### File Upload Fails

```bash
# Check bucket exists
mc ls local/documents

# Check permissions
mc policy get local/documents
```

## 📈 Performance Considerations

### MongoDB
- Index on `user_id` for fast lookups
- Index on `status` for filtering
- Connection pooling

### MinIO
- Bucket per user option for scaling
- CDN integration for downloads
- Multipart upload for large files

### API
- Streaming responses for downloads
- Async MongoDB operations
- Connection reuse

## 🧪 Integration with Other Services

### Chat Service
```python
# Chat can reference documents
# gRPC call to get document content for RAG
```

### Gateway
```python
# Routes document requests
# Validates JWT tokens
# Rate limiting per user
```

## 📚 Domain Events

### DocumentUploadedEvent
```python
{
    "document_id": "01HQXXX...",
    "user_id": "01HQXXX...",
    "filename": "report.pdf",
    "file_size": 1024000,
    "occurred_at": "2025-01-15T10:00:00"
}
```

### DocumentDeletedEvent
```python
{
    "document_id": "01HQXXX...",
    "user_id": "01HQXXX...",
    "deleted_at": "2025-01-15T11:00:00",
    "occurred_at": "2025-01-15T11:00:00"
}
```

## 🎉 Summary

The Document Service provides:

✅ Complete DDD implementation
✅ MongoDB for metadata
✅ MinIO for file storage
✅ File upload/download
✅ Document management
✅ Access control
✅ Status tracking
✅ Domain events
✅ Ready for gRPC integration

All services are now complete and ready to run! 🚀
