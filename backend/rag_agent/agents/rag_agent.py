import os
import time
import logging
import uuid
from typing import Dict, List, Any, Optional

import openai
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

from rag_agent.tools.retrieval_tool import RetrievalTool
from rag_agent.tools.validation_tool import ResponseValidator
from rag_agent.config.settings import settings


logger = logging.getLogger(__name__)


class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) Agent that answers queries using
    retrieved book content with citations and validation.
    """

    def __init__(self):
        # Initialize OpenAI client
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        if not qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )

        # Initialize tools
        self.retrieval_tool = RetrievalTool(self.qdrant_client)
        self.validator = ResponseValidator()

        # Track performance metrics
        self.total_queries = 0
        self.total_processing_time = 0.0
        self.failed_queries = 0

    def process_query(self,
                     query: str,
                     top_k: int = 5,
                     temperature: float = 0.7) -> Dict[str, Any]:
        """
        Process a query and return a grounded response based on retrieved content.

        Args:
            query: The user's query about book content
            top_k: Number of top results to retrieve from vector database
            temperature: Temperature parameter for response generation

        Returns:
            Dictionary containing response, citations, and metadata
        """
        start_time = time.time()
        self.total_queries += 1

        try:
            # Step 1: Retrieve relevant passages from vector database
            retrieved_passages = self.retrieval_tool.retrieve(
                query=query,
                top_k=top_k
            )

            if not retrieved_passages:
                logger.warning("No relevant content found for query")
                return {
                    "query_id": str(uuid.uuid4()),
                    "response": "I couldn't find any relevant information in the book content to answer your query.",
                    "confidence_score": 0.0,
                    "citations": [],
                    "processing_time": time.time() - start_time
                }

            # Step 2: Format context from retrieved passages
            context = self._format_context(retrieved_passages)

            # Step 3: Generate response using OpenAI
            response = self._generate_response(query, context, temperature)

            # Step 4: Validate the response
            is_valid, validation_feedback = self.validator.validate_response(
                response=response,
                context=context,
                query=query
            )

            # Step 5: Format citations
            citations = self._format_citations(retrieved_passages)

            # Calculate confidence based on validation and similarity scores
            confidence_score = self._calculate_confidence(retrieved_passages, is_valid)

            # Update performance metrics
            self.total_processing_time += (time.time() - start_time)

            logger.info(f"Query processed successfully in {(time.time() - start_time)*1000:.2f}ms")

            return {
                "query_id": str(uuid.uuid4()),
                "response": response,
                "confidence_score": confidence_score,
                "citations": citations,
                "validation_status": "valid" if is_valid else "needs_review",
                "validation_feedback": validation_feedback,
                "processing_time": time.time() - start_time
            }

        except Exception as e:
            self.failed_queries += 1
            logger.error(f"Error processing query: {str(e)}")
            raise

    def _format_context(self, retrieved_passages: List[Dict[str, Any]]) -> str:
        """
        Format the retrieved passages into a context string for the LLM.

        Args:
            retrieved_passages: List of retrieved passages with metadata

        Returns:
            Formatted context string
        """
        context_parts = []
        for i, passage in enumerate(retrieved_passages):
            text = passage.get("text", "")
            source = passage.get("source", "")
            doc_id = passage.get("doc_id", "")

            context_part = (
                f"Passage {i+1}: {text}\n"
                f"Source: {source} (ID: {doc_id})\n"
                f"Similarity Score: {passage.get('score', 0):.3f}\n\n"
            )
            context_parts.append(context_part)

        return "".join(context_parts)

    def _generate_response(self, query: str, context: str, temperature: float) -> str:
        """
        Generate a response using OpenAI based on the query and context.

        Args:
            query: User's query
            context: Retrieved context to ground the response
            temperature: Temperature parameter for generation

        Returns:
            Generated response text
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that answers questions based on provided book content. "
                    "Only use information from the provided passages to answer the question. "
                    "If the passages don't contain enough information to answer the question, say so. "
                    "Be concise but comprehensive in your response."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
            }
        ]

        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=settings.MAX_RESPONSE_TOKENS,
            n=1,
            stop=None
        )

        return response.choices[0].message['content'].strip()

    def _format_citations(self, retrieved_passages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format the retrieved passages into citation objects.

        Args:
            retrieved_passages: List of retrieved passages with metadata

        Returns:
            List of formatted citation objects
        """
        citations = []
        for passage in retrieved_passages:
            citation = {
                "source_document": passage.get("source", "Unknown"),
                "page_number": passage.get("page_number"),
                "section_title": passage.get("section_title"),
                "similarity_score": passage.get("score", 0.0),
                "passage_excerpt": passage.get("text", "")[:200] + "..." if len(passage.get("text", "")) > 200 else passage.get("text", "")
            }
            citations.append(citation)

        return citations

    def _calculate_confidence(self, retrieved_passages: List[Dict[str, Any]], is_valid: bool) -> float:
        """
        Calculate an overall confidence score based on similarity scores and validation result.

        Args:
            retrieved_passages: List of retrieved passages
            is_valid: Whether the response passed validation

        Returns:
            Confidence score between 0 and 1
        """
        if not retrieved_passages:
            return 0.0

        # Average similarity score of retrieved passages
        avg_similarity = sum(p.get("score", 0.0) for p in retrieved_passages) / len(retrieved_passages)

        # Adjust based on validation result
        validation_factor = 1.0 if is_valid else 0.5

        # Combine scores (could be more sophisticated)
        confidence = avg_similarity * validation_factor

        # Ensure it's within bounds
        return min(1.0, max(0.0, confidence))

    def check_openai_connection(self) -> bool:
        """
        Check if we can connect to the OpenAI API.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            openai.Model.list()
            return True
        except Exception:
            return False

    def check_qdrant_connection(self) -> bool:
        """
        Check if we can connect to the Qdrant database.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Attempt to list collections to check connection
            self.qdrant_client.get_collections()
            return True
        except Exception:
            return False

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the agent.

        Returns:
            Dictionary containing performance metrics
        """
        avg_processing_time = (
            self.total_processing_time / self.total_queries
            if self.total_queries > 0
            else 0.0
        )

        success_rate = (
            (self.total_queries - self.failed_queries) / self.total_queries
            if self.total_queries > 0
            else 0.0
        )

        return {
            "total_queries_processed": self.total_queries,
            "failed_queries": self.failed_queries,
            "success_rate": success_rate,
            "average_processing_time_ms": avg_processing_time * 1000,
            "timestamp": time.time()
        }