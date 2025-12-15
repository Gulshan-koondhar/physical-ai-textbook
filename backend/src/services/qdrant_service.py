from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class QdrantService:
    """
    Service for managing vector database operations with Qdrant
    """

    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True
        )
        self.collection_name = "physical-ai-book-v1"

    async def create_collection(self):
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists")
        except:
            # Create collection with vector configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),  # Gemini embedding size
                optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000, indexing_threshold=20000)
            )
            print(f"Created collection {self.collection_name}")

    async def upsert_vectors(self, points: List[Dict[str, Any]]):
        """Upsert vectors into the collection"""
        await self.create_collection()  # Ensure collection exists

        # Prepare points for upsert
        qdrant_points = []
        for point in points:
            qdrant_points.append(
                models.PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point["payload"]
                )
            )

        # Upsert the points
        self.client.upsert(
            collection_name=self.collection_name,
            points=qdrant_points
        )

    async def search_vectors(self, query_vector: List[float], limit: int = 10, metadata_filter: Optional[Dict] = None):
        """Search for similar vectors in the collection"""
        # Prepare filters if provided
        search_filter = None
        if metadata_filter:
            filter_conditions = []
            for key, value in metadata_filter.items():
                filter_conditions.append(
                    models.FieldCondition(
                        key=f"metadata.{key}",
                        match=models.MatchValue(value=value)
                    )
                )
            if filter_conditions:
                search_filter = models.Filter(must=filter_conditions)

        # Perform search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
            score_threshold=0.5,  # Minimum relevance score
            query_filter=search_filter
        )

        return results

    async def get_vector_count(self):
        """Get the total count of vectors in the collection"""
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count

# Global instance
qdrant_service = QdrantService()