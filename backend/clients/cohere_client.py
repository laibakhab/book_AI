"""
Cohere client wrapper for the RAG retrieval pipeline testing tool.
"""

import os
import numpy as np
from typing import List
from cohere import Client


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score between 0 and 1
    """
    # Convert to numpy arrays
    a = np.array(vec1)
    b = np.array(vec2)

    # Calculate cosine similarity
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


class CohereClient:
    """Wrapper for Cohere client to generate embeddings."""

    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize the Cohere client.

        Args:
            api_key: Cohere API key. If not provided, will try to read from environment variable.
            model_name: Name of the embedding model to use. If not provided, will try to read from environment variable.
        """
        if api_key is None:
            api_key = os.getenv("COHERE_API_KEY", "")

        if model_name is None:
            model_name = os.getenv("COHERE_MODEL", "embed-english-v2.0")  # Default model

        if not api_key:
            raise ValueError("Cohere API key is required. Please provide it or set COHERE_API_KEY environment variable.")

        self.client = Client(api_key)
        self.model_name = model_name

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the provided texts.

        Args:
            texts: List of text strings to generate embeddings for

        Returns:
            List of embedding vectors (each vector is a list of floats)

        Raises:
            Exception: If the embedding generation fails
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model_name
            )
            return response.embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to generate embedding for

        Returns:
            Embedding vector (list of floats)

        Raises:
            Exception: If the embedding generation fails
        """
        return self.generate_embeddings([text])[0]

    def check_consistency(self, text: str, num_runs: int = 3, threshold: float = 0.99) -> bool:
        """
        Check consistency of embeddings for the same text across multiple runs.

        Args:
            text: Text to generate embeddings for
            num_runs: Number of runs to perform
            threshold: Minimum similarity threshold for consistency

        Returns:
            True if embeddings are consistent, False otherwise
        """
        embeddings = []
        for _ in range(num_runs):
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)

        # Compare each embedding with the first one
        first_embedding = embeddings[0]
        for i in range(1, len(embeddings)):
            similarity = cosine_similarity(first_embedding, embeddings[i])
            if similarity < threshold:
                return False

        return True

    def compare_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Compare semantic similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score between the embeddings
        """
        emb1 = self.generate_embedding(text1)
        emb2 = self.generate_embedding(text2)
        return cosine_similarity(emb1, emb2)