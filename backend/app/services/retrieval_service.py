import os
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_huggingface import HuggingFaceEmbeddings

class RetrievalService:
    def __init__(self, qdrant_url: str = None):
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.collection_name = "knowledge_base"
        self.client = QdrantClient(url=self.qdrant_url)
        self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def search_evidence(self, query: str, category: Optional[str] = None, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant policy or historical evidence in the vector database.
        """
        query_vector = self.embeddings_model.embed_query(query)
        
        query_filter = None
        if category:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(value=category)
                    )
                ]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k
        ).points
        
        evidence = []
        for hit in results:
            evidence.append({
                "score": hit.score,
                "text": hit.payload.get("text"),
                "category": hit.payload.get("category"),
                "source": hit.payload.get("source")
            })
            
        return evidence

# Singleton instance
retrieval_service = RetrievalService()
