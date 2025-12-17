# RAG Agent Backend

## Overview
This project implements an AI agent that answers user queries using retrieved book content through a retrieval-augmented generation (RAG) approach. The system integrates with the OpenAI Agents SDK, connects to a Qdrant vector database containing embedded book content, and generates grounded responses that cite sources. It includes functionality for backend engineers and RAG evaluators to test and validate the retrieval pipeline's accuracy and performance.

## Features

- Processes user queries about book content using an AI agent
- Integrates with OpenAI Agents SDK for response generation
- Retrieves relevant content chunks from Qdrant vector database
- Generates grounded responses based on retrieved content with source citations
- Includes performance monitoring and validation tools
- Handles edge cases like connection failures and invalid queries gracefully

## Prerequisites

- Python 3.9+
- UV package manager or pip
- OpenAI API key
- Qdrant instance (cloud or self-hosted) with embedded book content

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Install dependencies:
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

   Or if using uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with your API keys and configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION=book_content
   OPENAI_MODEL=gpt-4-turbo
   DEFAULT_TOP_K=5
   CONFIDENCE_THRESHOLD=0.5
   REQUEST_TIMEOUT=30
   ```

## Usage

### Running the API Server
Start the RAG agent API server:
```bash
cd backend
uvicorn rag_agent.main:app --host 0.0.0.0 --port 8000
```

### Using the API
Once the server is running, you can make requests to the `/query` endpoint:

**Example request using curl:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main themes discussed in the book?",
    "top_k": 5,
    "temperature": 0.7,
    "include_citations": true
  }'
```

**Example request with Python:**
```python
import requests

response = requests.post("http://localhost:8000/query", json={
    "query": "What are the main themes discussed in the book?",
    "top_k": 5,
    "temperature": 0.7,
    "include_citations": True
})

print(response.json())
```

### Available Endpoints

- `POST /query` - Submit a query and get a grounded response
- `GET /health` - Check the health status of the service
- `GET /stats` - Get performance metrics
- `GET /docs` - Interactive API documentation (Swagger UI)

## Configuration Options

Adjust the following parameters in your `.env` file:

- `OPENAI_MODEL`: Model to use for response generation (default: 'gpt-4-turbo')
- `DEFAULT_TOP_K`: Number of results to retrieve (default: 5, min: 1, max: 20)
- `DEFAULT_TEMPERATURE`: Creativity parameter for response generation (default: 0.7)
- `CONFIDENCE_THRESHOLD`: Minimum confidence for valid responses (default: 0.5)
- `REQUEST_TIMEOUT`: Timeout for API requests in seconds (default: 30)

## Architecture

The system consists of the following key components:

1. **Main API**: FastAPI application that handles incoming requests
2. **RAG Agent**: Core logic for processing queries and coordinating response generation
3. **Retrieval Tool**: Interface for retrieving relevant content from Qdrant
4. **Validation Tool**: Ensures responses are grounded in retrieved content
5. **Configuration Module**: Manages settings and environment variables
6. **Data Models**: Pydantic models for request/response validation

## Design Decisions

- Used a tool-based agent architecture for clear separation of concerns
- Implemented validation to ensure response accuracy and proper citations
- Designed comprehensive error handling for various edge cases
- Included performance metrics tracking for monitoring and optimization

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Exit Codes

- `0`: Success - query processed successfully
- `1`: General error - unexpected error occurred
- `2`: Configuration error - missing API keys or invalid configuration
- `3`: Connection error - unable to connect to OpenAI or Qdrant
- `4`: Invalid input - invalid query or parameters

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.