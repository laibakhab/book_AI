import pytest
import os
from unittest.mock import Mock, patch
from backend.main import RagIngestionPipeline


def test_pipeline_initialization():
    """Test that the pipeline initializes with required clients"""
    # Set environment variables for testing
    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['QDRANT_URL'] = 'https://test-qdrant.com'
    os.environ['QDRANT_API_KEY'] = 'test-qdrant-key'
    
    # Create pipeline instance
    pipeline = RagIngestionPipeline()
    
    # Check that clients are initialized
    assert pipeline.cohere_client is not None
    assert pipeline.qdrant_client is not None


@patch('requests.get')
def test_extract_text_from_url(mock_get):
    """Test text extraction from a URL"""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'<html><head><title>Test Page</title></head><body><p>This is test content.</p></body></html>'
    mock_get.return_value = mock_response
    
    # Set environment variables
    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['QDRANT_URL'] = 'https://test-qdrant.com'
    os.environ['QDRANT_API_KEY'] = 'test-qdrant-key'
    
    # Create pipeline and test
    pipeline = RagIngestionPipeline()
    result = pipeline.extract_text_from_url('https://example.com')
    
    assert result['title'] == 'Test Page'
    assert 'This is test content.' in result['text']
    assert result['status'] == 'success'


def test_chunk_text():
    """Test text chunking functionality"""
    os.environ['COHERE_API_KEY'] = 'test-key'
    os.environ['QDRANT_URL'] = 'https://test-qdrant.com'
    os.environ['QDRANT_API_KEY'] = 'test-qdrant-key'
    
    pipeline = RagIngestionPipeline()
    
    # Test with a text that should be split into multiple chunks
    long_text = 'This is sentence one. This is sentence two. ' * 100  # Make it long enough to chunk
    
    chunks = pipeline.chunk_text(long_text, max_chunk_size=100)
    
    # Should have more than one chunk
    assert len(chunks) > 1
    
    # Each chunk should be less than or equal to max_chunk_size
    for chunk in chunks:
        assert len(chunk) <= 100


if __name__ == '__main__':
    pytest.main()