"""Data models for LEA (Learning Environment)."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LeaClass:
    """
    Represents a class in LEA.
    
    Reference: omnivox-crawler/src/types/LeaClass.ts
    """
    code: str                               # Course code (e.g., "420-3A4-DW")
    title: str                              # Course title
    teacher: str                            # Teacher name
    section: str                            # Section number
    schedule: list[str]                     # List of schedule strings
    grade: Optional[str] = None             # Current grade (e.g., "85.5%")
    average: Optional[float] = None         # Class average
    median: Optional[float] = None          # Class median
    distributed_documents: int = 0          # Number of new documents
    distributed_assignments: int = 0        # Number of new assignments
    
    def __repr__(self) -> str:
        return f"LeaClass(code='{self.code}', title='{self.title}', grade={self.grade})"


@dataclass
class Document:
    """
    Represents a document in LEA.
    
    Reference: omnivox-crawler/src/modules/lea/LeaClassDocuments.ts
    """
    name: str                               # Document name
    description: str                        # Document description
    posted: str                             # Date posted
    viewed: bool                            # Whether document has been viewed
    
    def __repr__(self) -> str:
        status = "✓" if self.viewed else "✗"
        return f"Document({status} '{self.name}', posted: {self.posted})"


@dataclass
class Category:
    """
    Represents a category of documents in LEA.
    
    Reference: omnivox-crawler/src/modules/lea/LeaClassDocuments.ts
    """
    name: str                               # Category name
    documents: list[Document]               # List of documents in category
    
    def __repr__(self) -> str:
        return f"Category('{self.name}', {len(self.documents)} documents)"


@dataclass
class ClassDocumentSummary:
    """
    Represents a summary of documents for a class.
    
    Reference: omnivox-crawler/src/modules/lea/LeaDocumentSummary.ts
    """
    name: str                               # Class name
    available_documents: str                # Number of available documents
    href: str                               # Link to documents page
    
    def __repr__(self) -> str:
        return f"ClassDocumentSummary('{self.name}', {self.available_documents} docs)"
