"""
Qdrant client wrapper for the RAG retrieval pipeline testing tool.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class QdrantClientWrapper:
    """Wrapper for Qdrant client to perform vector searches."""

    def __init__(self, url: str = None, api_key: str = None, vector_size: int = 768):
        """
        Initialize the Qdrant client.

        Args:
            url: Qdrant URL. If not provided, will try to read from environment variable.
            api_key: Qdrant API key. If not provided, will try to read from environment variable.
            vector_size: Size of the vectors (default: 4096 to match Cohere embeddings)
        """
        if url is None:
            url = os.getenv("QDRANT_URL", "")

        if api_key is None:
            api_key = os.getenv("QDRANT_API_KEY", "")

        if not url:
            raise ValueError("Qdrant URL is required. Please provide it or set QDRANT_URL environment variable.")

        if not api_key:
            raise ValueError("Qdrant API key is required. Please provide it or set QDRANT_API_KEY environment variable.")

        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )

        # Store connection details for error handling
        self.url = url
        self.api_key = api_key
        self.vector_size = vector_size  # Store the expected vector size

    def ensure_collection_exists(self, collection_name: str, recreate_if_exists: bool = False):
        """
        Ensure the collection exists with the correct vector size.

        Args:
            collection_name: Name of the collection to check/create
            recreate_if_exists: If True, deletes and recreates the collection even if it exists
        """
        try:
            # Check if collection exists
            collection_exists = self.check_collection_exists(collection_name)

            if collection_exists and recreate_if_exists:
                logger.info(f"Deleting existing collection '{collection_name}' to recreate with correct dimensions...")
                self.client.delete_collection(collection_name=collection_name)
                collection_exists = False

            if not collection_exists:
                # Create collection with correct vector size for Cohere embeddings
                logger.info(f"Creating collection '{collection_name}' with vector size {self.vector_size}...")
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=self.vector_size, distance=models.Distance.COSINE)
                )
                logger.info(f"Collection '{collection_name}' created successfully.")
            else:
                # Verify the existing collection has the right vector size
                collection_info = self.client.get_collection(collection_name)
                vector_config = collection_info.config.params
                if hasattr(vector_config, 'size'):
                    # For older versions of Qdrant client
                    actual_size = vector_config.size
                elif hasattr(vector_config, 'vectors'):
                    # For newer versions of Qdrant client
                    vector_details = vector_config.vectors
                    if isinstance(vector_details, dict) and 'size' in vector_details:
                        actual_size = vector_details['size']
                    elif hasattr(vector_details, 'size'):
                        actual_size = vector_details.size
                    else:
                        # Handle case with named vectors
                        actual_size = next(iter(vector_details.values())).size if vector_details else None
                else:
                    actual_size = None

                if actual_size != self.vector_size:
                    logger.warning(f"Collection '{collection_name}' exists with incorrect vector size ({actual_size}). Deleting and recreating...")
                    self.client.delete_collection(collection_name=collection_name)

                    # Create collection with correct vector size for Cohere embeddings
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(size=self.vector_size, distance=models.Distance.COSINE)
                    )
                    logger.info(f"Collection '{collection_name}' recreated with correct vector size {self.vector_size}.")
        except Exception as e:
            error_msg = f"Error ensuring collection exists '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def search(self,
               collection_name: str,
               query_vector: List[float],
               top_k: int = 5,
               with_payload: bool = True) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the specified collection.

        Args:
            collection_name: Name of the collection to search in
            query_vector: The query vector to search for
            top_k: Number of top results to return (default: 5)
            with_payload: Whether to return payload with the results (default: True)

        Returns:
            List of search results, each containing id, score, and payload

        Raises:
            Exception: If there are connection issues or other errors
        """
        # Validate vector size before search
        if len(query_vector) != self.vector_size:
            raise ValueError(f"Query vector dimension mismatch. Expected: {self.vector_size}, Got: {len(query_vector)}")

        try:
            # Using query_points which replaces search in qdrant-client >= 1.12
            search_response = self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=top_k,
                with_payload=with_payload,
            )

            # Format results to a more accessible format
            formatted_results = []
            for hit in search_response.points:
                formatted_results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload if hit.payload else {}
                })

            return formatted_results
        except Exception as e:
            error_msg = f"Error searching Qdrant collection '{collection_name}': {str(e)}"
            logger.error(error_msg)

            # Check if this is a connection error
            if "connection" in str(e).lower() or "timeout" in str(e).lower() or "refused" in str(e).lower():
                raise ConnectionError(f"Connection error with Qdrant at {self.url}: {str(e)}")
            elif "unauthorized" in str(e).lower() or "forbidden" in str(e).lower():
                raise PermissionError(f"Authentication error with Qdrant at {self.url}: incorrect API key")
            elif "not found" in str(e).lower() or "collection" in str(e).lower():
                raise ValueError(f"Collection '{collection_name}' does not exist or is not accessible")
            else:
                raise Exception(error_msg)

    def check_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in Qdrant.

        Args:
            collection_name: Name of the collection to check

        Returns:
            True if collection exists, False otherwise
        """
        try:
            self.client.get_collection(collection_name)
            return True
        except Exception as e:
            logger.debug(f"Collection '{collection_name}' does not exist: {str(e)}")
            return False

    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a collection.

        Args:
            collection_name: Name of the collection to get info for

        Returns:
            Collection information or None if collection doesn't exist
        """
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                "name": collection_info.config.params.vectors_count,
                "vector_count": collection_info.config.params.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info for '{collection_name}': {str(e)}")
            return None

    def is_connection_available(self) -> bool:
        """
        Check if the Qdrant connection is available.

        Returns:
            True if connection is available, False otherwise
        """
        try:
            # Attempt to get cluster info as a simple connectivity check
            self.client.get_collections()
            logger.info(f"Successfully connected to Qdrant at {self.url}")
            return True
        except Exception as e:
            logger.error(f"Could not connect to Qdrant at {self.url}: {str(e)}")
            return False