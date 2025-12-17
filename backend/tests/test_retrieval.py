"""
Unit tests for the retrieval functionality.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.retrieval import RetrievalService


class TestRetrievalService(unittest.TestCase):
    """Unit tests for the RetrievalService class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # We'll mock the clients to avoid actual API calls
        with patch('models.retrieval.CohereClient') as mock_cohere, \
             patch('models.retrieval.QdrantClientWrapper') as mock_qdrant:
            
            self.mock_cohere = mock_cohere.return_value
            self.mock_qdrant = mock_qdrant.return_value
            
            # Mock settings
            with patch('models.retrieval.settings') as mock_settings:
                mock_settings.QDRANT_COLLECTION = "test_collection"
                mock_settings.DEFAULT_TOP_K = 5
                
                self.service = RetrievalService()
    
    def test_retrieve_calls_clients_correctly(self):
        """Test that retrieve method calls the clients with correct parameters."""
        # Arrange
        query = "test query"
        expected_embedding = [0.1, 0.2, 0.3]
        expected_results = [
            {
                "id": "chunk-1",
                "score": 0.9,
                "payload": {
                    "text": "This is a test chunk",
                    "url": "https://example.com",
                    "title": "Test Title",
                    "headings": ["Heading1", "Heading2"]
                }
            }
        ]
        
        self.mock_cohere.generate_embedding.return_value = expected_embedding
        self.mock_qdrant.search.return_value = expected_results
        
        # Act
        result = self.service.retrieve(query, collection_name="test_collection", top_k=1)
        
        # Assert
        self.mock_cohere.generate_embedding.assert_called_once_with(query)
        self.mock_qdrant.search.assert_called_once_with(
            collection_name="test_collection",
            query_vector=expected_embedding,
            top_k=1
        )
        self.assertEqual(result["query"], query)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["chunk_id"], "chunk-1")
        self.assertEqual(result["results"][0]["similarity_score"], 0.9)
    
    def test_validate_collection_calls_client(self):
        """Test that validate_collection calls the Qdrant client."""
        # Arrange
        collection_name = "test_collection"
        expected_result = True
        
        self.mock_qdrant.check_collection_exists.return_value = expected_result
        
        # Act
        result = self.service.validate_collection(collection_name)
        
        # Assert
        self.mock_qdrant.check_collection_exists.assert_called_once_with(collection_name)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()