# API Contract: RAG Agent Service

## Base URL
`http://localhost:8000` (or as configured in deployment)

## Endpoints

### POST /query
Submit a query to the RAG agent and receive a grounded response based on book content.

**Request Body**:
```json
{
  "query": "What are the main themes discussed in the book?",
  "top_k": 5,
  "temperature": 0.7,
  "include_citations": true
}
```

**Parameters**:
- `query` (string, required): The user's question or query about the book content
- `top_k` (integer, optional): Number of top results to retrieve from the vector database (default: 5, min: 1, max: 20)
- `temperature` (float, optional): Temperature parameter for the LLM response generation (default: 0.7, min: 0.0, max: 1.0)
- `include_citations` (boolean, optional): Whether to include source citations in the response (default: true)

**Successful Response (200 OK)**:
```json
{
  "query_id": "uuid-string",
  "original_query": "What are the main themes discussed in the book?",
  "response": "The main themes discussed in the book include...",
  "confidence_score": 0.85,
  "citations": [
    {
      "source_document": "book_title.pdf",
      "page_number": 25,
      "section_title": "Chapter 3: Themes Overview",
      "similarity_score": 0.92
    }
  ],
  "retrieved_chunks_count": 5,
  "processing_time_ms": 1250,
  "timestamp": "2025-12-16T10:30:00Z"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid request parameters
```json
{
  "detail": "Query cannot be empty"
}
```

- `408 Request Timeout`: Query took too long to process
```json
{
  "detail": "Query processing timed out"
}
```

- `500 Internal Server Error`: System error during processing
```json
{
  "detail": "An internal error occurred while processing the query"
}
```

### GET /health
Check the health status of the RAG agent service and its dependencies.

**Successful Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T10:30:00Z",
  "dependencies": {
    "openai_api": "connected",
    "qdrant_db": "connected",
    "agent_service": "ready"
  }
}
```

**Error Response (503 Service Unavailable)**:
```json
{
  "status": "unhealthy",
  "timestamp": "2025-12-16T10:30:00Z",
  "dependencies": {
    "openai_api": "disconnected",
    "qdrant_db": "connected",
    "agent_service": "degraded"
  },
  "detail": "OpenAI API connection failed"
}
```

### GET /stats
Get statistics about the RAG agent's performance and usage.

**Successful Response (200 OK)**:
```json
{
  "total_queries": 1250,
  "avg_response_time_ms": 1100,
  "queries_last_hour": 45,
  "top_k_used": 5,
  "confidence_threshold": 0.5,
  "timestamp": "2025-12-16T10:30:00Z"
}
```

## Error Handling

The API follows standard HTTP error codes:
- `200`: Successful request
- `400`: Client error (bad request, validation failure)
- `408`: Request timeout
- `422`: Request validation error
- `500`: Internal server error
- `503`: Service unavailable

## Authentication
This API does not require authentication for testing purposes. In production deployments, authentication may be added using API keys.

## Rate Limiting
The API may implement rate limiting to prevent abuse. Clients should implement appropriate retry logic with exponential backoff for 429 responses.