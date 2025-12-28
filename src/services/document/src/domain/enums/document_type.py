from enum import Enum


class DocumentType(str, Enum):
    """Document file type."""

    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"
    POWERPOINT = "powerpoint"
    TEXT = "text"
    IMAGE = "image"
    OTHER = "other"
