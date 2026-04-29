"""Memory and context management.

This module provides persistent memory and context management for TafySH,
including session history, long-term storage, and intelligent retrieval.

Components:
    - schemas: Memory record types and data classes
    - session: In-memory session/conversation tracking
    - store: Persistent storage backends (SQLite, in-memory)
    - retrieval: Search and retrieval system
    - manager: Unified memory interface
"""

from tafysh.memory.manager import MemoryManager
from tafysh.memory.retrieval import MemoryRetrieval, RetrievalConfig, SemanticRetrieval
from tafysh.memory.schemas import (
    MemoryMetadata,
    MemoryRecord,
    MemoryType,
    SearchResult,
    Turn,
)
from tafysh.memory.session import (
    MultiSessionStore,
    SessionConfig,
    SessionStore,
)
from tafysh.memory.store import (
    InMemoryStore,
    MemoryStore,
    SQLiteMemoryStore,
)

__all__ = [
    # Manager
    "MemoryManager",
    # Schemas
    "MemoryType",
    "MemoryMetadata",
    "MemoryRecord",
    "Turn",
    "SearchResult",
    # Session
    "SessionStore",
    "SessionConfig",
    "MultiSessionStore",
    # Store
    "MemoryStore",
    "SQLiteMemoryStore",
    "InMemoryStore",
    # Retrieval
    "MemoryRetrieval",
    "RetrievalConfig",
    "SemanticRetrieval",
]
