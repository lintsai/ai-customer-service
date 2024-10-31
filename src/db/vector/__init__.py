from typing import Optional, List
import chromadb
from chromadb.config import Settings as ChromaSettings
from src.core.config import settings
from functools import lru_cache

@lru_cache()
def get_vector_store():
    """
    Get vector store instance based on configuration
    Currently supports ChromaDB
    """
    if settings.VECTOR_STORE_TYPE.lower() == "chroma":
        # Initialize ChromaDB with persistent storage
        chroma_client = chromadb.Client(
            ChromaSettings(
                persist_directory="./data/vectordb",
                is_persistent=True
            )
        )
        
        # Get or create collection
        collection = chroma_client.get_or_create_collection(
            name="customer_service_kb",
            metadata={"description": "Customer service knowledge base"}
        )
        
        return collection
    else:
        raise ValueError(f"Unsupported vector store type: {settings.VECTOR_STORE_TYPE}")

class VectorStore:
    def __init__(self):
        self.collection = get_vector_store()

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """Add documents to vector store"""
        return self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query: str,
        n_results: int = 3,
        where: Optional[dict] = None
    ):
        """Search similar documents"""
        return self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

# Create vector store instance
vector_store = VectorStore()