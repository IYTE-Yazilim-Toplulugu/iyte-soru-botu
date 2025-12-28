from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.entities import Document
from src.domain.interfaces import IDocumentRepository
from src.domain.value_objects import DocumentMetadata, FileReference
from src.domain.enums import DocumentStatus, DocumentType
from src.infrastructure.data.mongodb import mongodb_client


class DocumentRepository(IDocumentRepository):
    """MongoDB repository implementation for Document aggregate."""

    def __init__(self):
        self._collection: AsyncIOMotorCollection = mongodb_client.get_collection(
            "documents"
        )

    async def add(self, entity: Document) -> None:
        """Add a new document."""
        doc_dict = self._to_dict(entity)
        await self._collection.insert_one(doc_dict)

    async def get_by_id(self, id: str) -> Optional[Document]:
        """Get a document by ID."""
        doc_dict = await self._collection.find_one({"_id": id})
        return self._to_entity(doc_dict) if doc_dict else None

    async def update(self, entity: Document) -> None:
        """Update a document."""
        doc_dict = self._to_dict(entity)
        await self._collection.update_one({"_id": entity.id}, {"$set": doc_dict})

    async def delete(self, id: str) -> None:
        """Delete a document."""
        await self._collection.delete_one({"_id": id})

    async def find_by_user_id(self, user_id: str) -> List[Document]:
        """Find all documents for a user."""
        cursor = self._collection.find({"user_id": user_id})
        documents = []
        async for doc_dict in cursor:
            documents.append(self._to_entity(doc_dict))
        return documents

    async def find_by_user_and_status(
        self, user_id: str, status: str
    ) -> List[Document]:
        """Find documents by user and status."""
        cursor = self._collection.find({"user_id": user_id, "status": status})
        documents = []
        async for doc_dict in cursor:
            documents.append(self._to_entity(doc_dict))
        return documents

    def _to_entity(self, doc_dict: dict) -> Document:
        """Convert MongoDB document to domain entity."""
        return Document(
            id=doc_dict["_id"],
            user_id=doc_dict["user_id"],
            metadata=DocumentMetadata(
                filename=doc_dict["metadata"]["filename"],
                file_size=doc_dict["metadata"]["file_size"],
                content_type=doc_dict["metadata"]["content_type"],
            ),
            file_reference=FileReference(
                bucket=doc_dict["file_reference"]["bucket"],
                path=doc_dict["file_reference"]["path"],
                url=doc_dict["file_reference"]["url"],
            ),
            status=DocumentStatus(doc_dict["status"]),
            document_type=DocumentType(doc_dict["document_type"]),
            parsed_content=doc_dict.get("parsed_content"),
            error_message=doc_dict.get("error_message"),
            created_at=doc_dict["created_at"],
            updated_at=doc_dict.get("updated_at"),
        )

    def _to_dict(self, entity: Document) -> dict:
        """Convert domain entity to MongoDB document."""
        return {
            "_id": entity.id,
            "user_id": entity.user_id,
            "metadata": {
                "filename": entity.metadata.filename,
                "file_size": entity.metadata.file_size,
                "content_type": entity.metadata.content_type,
            },
            "file_reference": {
                "bucket": entity.file_reference.bucket,
                "path": entity.file_reference.path,
                "url": entity.file_reference.url,
            },
            "status": entity.status.value,
            "document_type": entity.document_type.value,
            "parsed_content": entity.parsed_content,
            "error_message": entity.error_message,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
