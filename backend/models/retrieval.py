"""
Retrieval logic for the RAG retrieval pipeline testing tool.
"""

import time
from typing import List, Dict, Any, Optional


def validate_query_text(query: str) -> bool:
    """
    Validate the query text according to the data model.

    Args:
        query: The query text to validate

    Returns:
        True if valid, False otherwise
    """
    if not query or not query.strip():
        return False
    return True


def validate_query_embedding(embedding: List[float], expected_dimension: Optional[int] = None) -> bool:
    """
    Validate the query embedding according to the data model.

    Args:
        embedding: The embedding vector to validate
        expected_dimension: Expected dimension of the embedding (if known)

    Returns:
        True if valid, False otherwise
    """
    if not embedding:
        return False
    if not isinstance(embedding, list):
        return False
    if not all(isinstance(val, (int, float)) for val in embedding):
        return False
    if expected_dimension is not None and len(embedding) != expected_dimension:
        return False
    return True


def validate_retrieved_chunk(chunk: Dict[str, Any]) -> bool:
    """
    Validate the retrieved chunk according to the data model.

    Args:
        chunk: The chunk to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(chunk, dict):
        return False

    # Check similarity score is between 0 and 1
    sim_score = chunk.get('similarity_score')
    if sim_score is not None and (not isinstance(sim_score, (int, float)) or sim_score < 0 or sim_score > 1):
        return False

    # Check source URL format if present
    source_url = chunk.get('source_url')
    if source_url and not isinstance(source_url, str):
        return False

    return True


def validate_retrieval_result(result: Dict[str, Any]) -> bool:
    """
    Validate the retrieval result according to the data model.

    Args:
        result: The retrieval result to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(result, dict):
        return False

    # Check top_k is a positive integer
    top_k = result.get('top_k')
    if top_k is not None and (not isinstance(top_k, int) or top_k <= 0):
        return False

    # Validate execution time if present
    exec_time = result.get('execution_time_ms')
    if exec_time is not None and (not isinstance(exec_time, (int, float)) or exec_time < 0):
        return False

    # Validate all results in the results list
    results_list = result.get('results', [])
    if not isinstance(results_list, list):
        return False

    for chunk in results_list:
        if not validate_retrieved_chunk(chunk):
            return False

    return True


class PerformanceMetrics:
    """Class to track and store performance metrics."""

    def __init__(self):
        self.query_times = []
        self.avg_embedding_time = 0.0
        self.avg_search_time = 0.0
        self.cache_hits = 0
        self.total_requests = 0

    def add_query_time(self, query_time_ms: float):
        """Add a query response time to the metrics."""
        self.query_times.append(query_time_ms)
        self.total_requests += 1

    def get_avg_response_time(self) -> float:
        """Calculate the average response time."""
        if not self.query_times:
            return 0.0
        return sum(self.query_times) / len(self.query_times)

    def get_p95_response_time(self) -> float:
        """Calculate the 95th percentile response time."""
        if not self.query_times:
            return 0.0
        sorted_times = sorted(self.query_times)
        index = int(0.95 * len(sorted_times))
        return sorted_times[index] if index < len(sorted_times) else sorted_times[-1]

    def get_throughput(self, time_window_minutes: float = 1) -> float:
        """Calculate requests per minute."""
        if not self.query_times:
            return 0.0
        # Assuming all requests happen within the time window for simplicity
        return self.total_requests / time_window_minutes if time_window_minutes > 0 else 0.0


class RetrievalService:
    """Service class to handle the retrieval logic."""

    def __init__(self):
        # Import here to avoid circular dependencies
        from clients.cohere_client import CohereClient
        from clients.qdrant_client import QdrantClientWrapper
        from config.settings import settings

        self.cohere_client = CohereClient()
        # Initialize Qdrant client with 4096 dimensions for Cohere embed-english-v2.0 model (actual dimension from API)
        self.qdrant_client = QdrantClientWrapper(vector_size=4096)
        self.settings = settings
        self.performance_metrics = PerformanceMetrics()

        # Ensure collection exists with correct vector dimensions on initialization
        self.qdrant_client.ensure_collection_exists(self.settings.QDRANT_COLLECTION, recreate_if_exists=True)

    def retrieve(self,
                 query: str,
                 collection_name: str = None,
                 top_k: int = None) -> Dict[str, Any]:
        """
        Perform the retrieval process: generate query embedding and search Qdrant.

        Args:
            query: The query text to search for
            collection_name: Name of the Qdrant collection to search in (defaults to settings)
            top_k: Number of top results to return (defaults to settings)

        Returns:
            Dictionary containing query, results, execution time, and metadata
        """
        if collection_name is None:
            collection_name = self.settings.QDRANT_COLLECTION

        if top_k is None:
            top_k = self.settings.DEFAULT_TOP_K

        # Validate top_k is within acceptable bounds (from config settings)
        if top_k < self.settings.MIN_TOP_K or top_k > self.settings.MAX_TOP_K:
            raise ValueError(f"top_k value must be between {self.settings.MIN_TOP_K} and {self.settings.MAX_TOP_K}")

        # Validate query text
        if not validate_query_text(query):
            raise ValueError("Invalid query text: Query cannot be empty or only whitespace")

        start_time = time.time()

        # Generate embedding for the query
        embedding_start = time.time()
        try:
            query_embedding = self.cohere_client.generate_embedding(query)
        except Exception as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                raise ConnectionError(f"Connection error with Cohere API: {str(e)}")
            elif "invalid" in str(e).lower() or "authentication" in str(e).lower():
                raise PermissionError(f"Authentication error with Cohere API: invalid API key or quota exceeded")
            else:
                raise Exception(f"Error generating query embedding: {str(e)}")
        embedding_time = (time.time() - embedding_start) * 1000  # Convert to ms

        # Validate the embedding
        if not validate_query_embedding(query_embedding):
            raise ValueError("Invalid query embedding generated")

        # Search in Qdrant
        search_start = time.time()
        try:
            search_results = self.qdrant_client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k
            )
        except ConnectionError as ce:
            raise ce  # Propagate connection errors
        except PermissionError as pe:
            raise pe  # Propagate permission errors
        except ValueError as ve:
            # This might be the collection not found error
            if "does not exist" in str(ve):
                raise ve  # Propagate value errors related to collections
            raise
        except Exception as e:
            # Handle other edge cases
            if "no relevant matches" in str(e) or "no results" in str(e).lower():
                # Edge case: Query with no relevant matches in vector database
                return {
                    "query": query,
                    "query_embedding_model": self.cohere_client.model_name,
                    "collection": collection_name,
                    "top_k": top_k,
                    "results": [],
                    "execution_time_ms": (time.time() - start_time) * 1000,
                    "embedding_time_ms": embedding_time,
                    "search_time_ms": (time.time() - search_start) * 1000,
                    "performance_metrics": {
                        "avg_response_time_ms": self.performance_metrics.get_avg_response_time(),
                        "p95_response_time_ms": self.performance_metrics.get_p95_response_time(),
                        "throughput_requests_per_minute": self.performance_metrics.get_throughput()
                    },
                    "timestamp": time.time()
                }
            raise e
        search_time = (time.time() - search_start) * 1000  # Convert to ms

        # Format the results
        formatted_results = []
        for i, result in enumerate(search_results):
            # Skip results that fail validation
            formatted_result = {
                "rank": i + 1,
                "chunk_id": result["id"],
                "similarity_score": result["score"],
                "text_content": result["payload"].get("text", "")[:200] + "..." if len(result["payload"].get("text", "")) > 200 else result["payload"].get("text", ""),
                "full_content": result["payload"].get("text", ""),
                "source_url": result["payload"].get("url", ""),
                "source_title": result["payload"].get("title", ""),
                "headings": result["payload"].get("headings", []),
                "metadata": {k: v for k, v in result["payload"].items() if k not in ["text", "url", "title", "headings"]}
            }

            # Validate the formatted result before adding
            if validate_retrieved_chunk(formatted_result):
                formatted_results.append(formatted_result)
            else:
                print(f"Warning: Skipping invalid chunk with ID: {result['id']}")

        # Calculate total execution time
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Update performance metrics
        self.performance_metrics.add_query_time(execution_time)
        self.performance_metrics.avg_embedding_time = embedding_time
        self.performance_metrics.avg_search_time = search_time

        # Prepare the output
        output = {
            "query": query,
            "query_embedding_model": self.cohere_client.model_name,
            "collection": collection_name,
            "top_k": top_k,
            "results": formatted_results,
            "execution_time_ms": execution_time,
            "embedding_time_ms": embedding_time,
            "search_time_ms": search_time,
            "performance_metrics": {
                "avg_response_time_ms": self.performance_metrics.get_avg_response_time(),
                "p95_response_time_ms": self.performance_metrics.get_p95_response_time(),
                "throughput_requests_per_minute": self.performance_metrics.get_throughput()
            },
            "timestamp": time.time()
        }

        # Validate the final output
        if not validate_retrieval_result(output):
            raise ValueError("Retrieved results failed validation")

        return output

    def validate_collection(self, collection_name: str) -> bool:
        """
        Validate that the specified collection exists and has vectors.

        Args:
            collection_name: Name of the collection to validate

        Returns:
            True if collection exists and has vectors, False otherwise
        """
        return self.qdrant_client.check_collection_exists(collection_name)

    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive performance report.

        Returns:
            Dictionary containing performance metrics
        """
        return {
            "total_requests": self.performance_metrics.total_requests,
            "avg_response_time_ms": self.performance_metrics.get_avg_response_time(),
            "p95_response_time_ms": self.performance_metrics.get_p95_response_time(),
            "throughput_requests_per_minute": self.performance_metrics.get_throughput(),
            "avg_embedding_time_ms": self.performance_metrics.avg_embedding_time,
            "avg_search_time_ms": self.performance_metrics.avg_search_time
        }