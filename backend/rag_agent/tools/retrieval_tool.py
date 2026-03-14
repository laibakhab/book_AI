import logging
import os
import sys
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models


# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from clients.cohere_client import CohereClient


logger = logging.getLogger(__name__)


class RetrievalTool:
    """
    Tool for retrieving relevant passages from the Qdrant vector database.
    """

    def __init__(self, qdrant_client: QdrantClient, collection_name: str = None):
        """
        Initialize the retrieval tool.

        Args:
            qdrant_client: Instance of QdrantClient
            collection_name: Name of the collection to search in (defaults to env)
        """
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION", "rag_embeddings")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve the top-k most relevant passages for the given query.

        Args:
            query: Query string to search for
            top_k: Number of top results to return

        Returns:
            List of retrieved passages with metadata
        """
        try:
            # First, embed the query using the same model as used for indexing
            # For this implementation, we assume the embeddings are pre-computed
            # In a real implementation, we would generate embedding for the query

            # For now, we'll create a mock embedding (in a real system, use Cohere or similar)
            query_embedding = self._generate_query_embedding(query)

            # Search in Qdrant using query_points (qdrant-client >= 1.12)
            search_response = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                with_payload=True,
            )

            # Format the results
            formatted_results = []
            for hit in search_response.points:
                result = {
                    "id": hit.id,
                    "score": hit.score,
                    "text": hit.payload.get("text", ""),
                    "source": hit.payload.get("source", ""),
                    "page_number": hit.payload.get("page_number"),
                    "section_title": hit.payload.get("section_title", ""),
                    "url": hit.payload.get("url", ""),
                    "title": hit.payload.get("title", "")
                }
                formatted_results.append(result)

            logger.info(f"Retrieved {len(formatted_results)} results for query")
            return formatted_results

        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return []

    def _generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for the query text using Cohere.

        Args:
            query: Query text to embed

        Returns:
            Embedding vector as a list of floats
        """
        try:
            # Initialize Cohere client
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable is required")

            cohere_client = CohereClient(api_key=api_key)

            # Generate embedding for the query
            embedding = cohere_client.generate_embedding(query)

            # Log success
            logger.info(f"Successfully generated embedding for query: {query[:50]}...")

            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding with Cohere: {str(e)}")
            # Fallback to mock embedding if Cohere fails
            logger.warning("Falling back to mock embedding due to Cohere error.")
            import numpy as np
            np.random.seed(abs(hash(query)) % (2**32))
            # Return 768-dim vector to match Cohere embed-multilingual-v2.0
            return np.random.random(768).tolist()

    def validate_collection_exists(self) -> bool:
        """
        Validate that the specified collection exists in Qdrant.

        Returns:
            True if collection exists, False otherwise
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return True
        except Exception as e:
            logger.error(f"Collection {self.collection_name} does not exist: {str(e)}")
            return False