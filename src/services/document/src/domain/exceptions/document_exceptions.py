from shared_kernel import DomainException


class DocumentNotFoundException(DomainException):
    """Raised when a document is not found."""

    def __init__(self, document_id: str):
        super().__init__(f"Document not found: {document_id}")


class DocumentUploadFailedException(DomainException):
    """Raised when document upload fails."""

    def __init__(self, message: str = "Failed to upload document"):
        super().__init__(message)


class DocumentAccessDeniedException(DomainException):
    """Raised when user doesn't have access to a document."""

    def __init__(self, document_id: str):
        super().__init__(f"Access denied to document: {document_id}")


class StorageException(DomainException):
    """Raised when storage operation fails."""

    def __init__(self, message: str):
        super().__init__(f"Storage error: {message}")
