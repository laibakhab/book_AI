# API Contract: RAG Frontend-Backend Integration

## Base URL
`http://localhost:8000` (or as configured in deployment)

## Endpoints

### POST /query
Submit a user query to the RAG backend and receive a grounded response based on book content.

**Request Body:**
```json
{
  "query": "What are the key features of RAG systems?",
  "top_k": 5,
  "include_citations": true,
  "session_id": "session-uuid-if-applicable"
}
```

**Parameters:**
- `query` (string, required): The user's question or query about the book content
- `top_k` (integer, optional): Number of top results to retrieve from the vector database (default: 5, min: 1, max: 20)
- `include_citations` (boolean, optional): Whether to include source citations in the response (default: true)
- `session_id` (string, optional): Session identifier for maintaining conversation context (for future multi-turn support)

**Successful Response (200 OK):**
```json
{
  "response_id": "response-uuid",
  "query_id": "query-uuid",
  "query": "What are the key features of RAG systems?",
  "answer": "RAG (Retrieval-Augmented Generation) systems combine...",
  "confidence_score": 0.87,
  "citations": [
    {
      "source_url": "https://book-url/chapter-3",
      "source_title": "Chapter 3: RAG Implementation",
      "section_title": "Key Features",
      "page_number": 45,
      "similarity_score": 0.92,
      "text_snippet": "RAG systems have several key features including..."
    }
  ],
  "processing_time_ms": 650,
  "timestamp": "2025-12-16T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request parameters
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Query cannot be empty or exceed 2000 characters"
  }
}
```

- `408 Request Timeout`: Query processing took too long
```json
{
  "error": {
    "code": "QUERY_TIMEOUT",
    "message": "Query processing exceeded the allowed timeout of 10 seconds"
  }
}
```

- `500 Internal Server Error`: System error during processing
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal error occurred during query processing"
  }
}
```

- `503 Service Unavailable`: RAG backend services are temporarily unavailable
```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "RAG services are temporarily unavailable, please try again later"
  }
}
```

### GET /health
Check the health status of the RAG backend service and its dependencies.

**Successful Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T10:30:00Z",
  "dependencies": {
    "cohere_api": "connected",
    "qdrant_db": "connected",
    "rag_backend": "ready",
    "frontend_connection": "ready"
  }
}
```

**Error Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-12-16T10:30:00Z",
  "dependencies": {
    "cohere_api": "disconnected",
    "qdrant_db": "connected",
    "rag_backend": "degraded",
    "frontend_connection": "ready"
  },
  "detail": "Cohere API connection failed"
}
```

### GET /stats
Get statistics about the RAG system's performance and usage.

**Successful Response (200 OK):**
```json
{
  "queries_last_hour": 45,
  "avg_response_time_ms": 725,
  "success_rate": 0.96,
  "total_queries_served": 1240,
  "timestamp": "2025-12-16T10:30:00Z"
}
```

## Error Handling

The API follows standard HTTP error codes:
- `200`: Successful request with valid response
- `400`: Client error (malformed request, invalid parameters)
- `408`: Request timeout during processing
- `422`: Request validation error (unprocessable entity)
- `500`: Internal server error during processing
- `503`: Service unavailable (dependency down)

## Authentication
The API uses API key authentication in the header:
```
Authorization: Bearer <api_key>
```

## Rate Limiting
The API enforces rate limiting per IP address:
- 100 requests per minute per IP
- 429 response code when limit is exceeded
- Retry-After header specifies when to retry

## Security
- All requests must use HTTPS in production
- Input sanitization is applied to prevent injection attacks
- Response payloads are encoded to prevent XSS
- API keys must be rotated periodically