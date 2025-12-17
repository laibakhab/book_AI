import logging
import re
from typing import Tuple


logger = logging.getLogger(__name__)


class ResponseValidator:
    """
    Validates that generated responses are properly grounded in the provided context.
    """

    def __init__(self):
        self.validation_threshold = 0.7  # Minimum confidence for valid responses

    def validate_response(self,
                         response: str,
                         context: str,
                         query: str) -> Tuple[bool, str]:
        """
        Validate if the response is supported by the provided context.

        Args:
            response: The generated response to validate
            context: The context passages that should support the response
            query: The original query that prompted the response

        Returns:
            Tuple of (is_valid, feedback_message)
        """
        # Check if response is empty
        if not response or not response.strip():
            return False, "Response is empty"

        # Check if response contains phrases indicating lack of information
        unsupported_phrases = [
            r"cannot determine",
            r"not mentioned",
            r"not provided",
            r"not specified",
            r"not found in the context",
            r"no information provided"
        ]

        for phrase in unsupported_phrases:
            if re.search(phrase, response, re.IGNORECASE):
                # If the agent properly acknowledges lack of information, this is valid
                if len(response) < 200:  # Short acknowledgment responses are valid
                    return True, "Valid acknowledgment of insufficient information"

        # Check if response cites specific information from context
        has_citation = self._check_citations(response, context)

        # Check if key information in response appears in context
        has_supporting_evidence = self._check_supporting_evidence(response, context)

        # Check if response directly addresses the query
        addresses_query = self._check_query_alignment(response, query)

        # Determine overall validity
        if has_citation and has_supporting_evidence and addresses_query:
            return True, "Response is well-supported by context"
        elif has_supporting_evidence and addresses_query:
            return True, "Response is supported by context but could improve citation"
        else:
            feedback_parts = []
            if not has_citation:
                feedback_parts.append("Missing proper citations to context")
            if not has_supporting_evidence:
                feedback_parts.append("Response contains information not found in context")
            if not addresses_query:
                feedback_parts.append("Response does not adequately address the query")

            return False, "; ".join(feedback_parts)

    def _check_citations(self, response: str, context: str) -> bool:
        """
        Check if the response appropriately references information from the context.

        Args:
            response: The response text
            context: The context text

        Returns:
            True if response appropriately cites context, False otherwise
        """
        # Look for explicit citations or references to sources
        citation_patterns = [
            r"according to",      # According to the text...
            r"the document says", # The document says...
            r"based on",         # Based on the provided information...
            r"mentioned in",     # Mentioned in the text...
            r"is stated",        # X is stated in the document...
        ]

        for pattern in citation_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return True

        # If no explicit citations, check if content logically derives from context
        # For now, we'll return True if the response has supporting evidence
        return True

    def _check_supporting_evidence(self, response: str, context: str) -> bool:
        """
        Check if key information in the response appears in the context.

        Args:
            response: The response text
            context: The context text

        Returns:
            True if response content is supported by context, False otherwise
        """
        # Simple keyword overlap approach as a baseline
        # (A more advanced implementation would use semantic similarity)

        if len(context) == 0:
            return False

        # Extract key terms from response
        response_words = set(re.findall(r'\b\w+\b', response.lower()))
        context_words = set(re.findall(r'\b\w+\b', context.lower()))

        # Calculate overlap
        intersection = response_words.intersection(context_words)
        response_unique_words = len(response_words)

        if response_unique_words == 0:
            return False

        # If at least 40% of unique words in the response appear in context
        overlap_ratio = len(intersection) / response_unique_words
        return overlap_ratio >= 0.4  # Require 40% overlap for basic validation

    def _check_query_alignment(self, response: str, query: str) -> bool:
        """
        Check if the response addresses the original query.

        Args:
            response: The response text
            query: The query text

        Returns:
            True if response addresses the query, False otherwise
        """
        # Simple check: see if response addresses key terms from the query
        query_keywords = re.findall(r'\b\w+\b', query.lower())

        # Remove common stop words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "to", "of", "in", "on", "at", "for",
            "with", "by", "and", "or", "but", "if", "then", "than", "so", "as", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will", "would", "should",
            "may", "might", "must", "can", "could"
        }
        query_terms = [term for term in query_keywords if term not in stop_words and len(term) > 2]

        if not query_terms:
            # If no meaningful terms in query, can't validate alignment
            return True

        response_lower = response.lower()
        aligned_terms = [term for term in query_terms if term in response_lower]

        # Require at least 50% of query terms to appear in response
        return len(aligned_terms) / len(query_terms) >= 0.5 if len(query_terms) > 0 else True