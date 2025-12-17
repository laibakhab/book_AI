# Quickstart Guide: RAG Agent Backend

## Overview
This guide provides instructions to set up and run the RAG (Retrieval-Augmented Generation) Agent Backend. This system implements an AI agent that answers user queries using retrieved book content, with responses grounded in the vector database content.

## Prerequisites
- Python 3.11+
- OpenAI API key
- Qdrant vector database instance with embedded book content
- Git (for cloning the repository)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install fastapi openai qdrant-client python-dotenv pydantic uvicorn
   ```

5. **Set up environment variables**
   Create a `.env` file in the backend directory with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=your_qdrant_instance_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION=your_collection_name_containing_book_embeddings
   ```

6. **Run the application**
   ```bash
   uvicorn rag_agent.main:app --reload --port 8000
   ```

## Basic Usage

Once the server is running, you can interact with the agent using the following endpoints:

1. **Query the agent** (POST request to `/query`):
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Your question about the book content here",
       "top_k": 5,
       "temperature": 0.7
     }'
   ```

2. **Check the API documentation** at `http://localhost:8000/docs` for the interactive Swagger UI.

## Configuration Options

- `OPENAI_MODEL`: Change the model used for the agent (default: gpt-4-turbo)
- `TOP_K_RESULTS`: Number of documents to retrieve from the vector database (default: 5)
- `TEMPERATURE`: Controls randomness of the agent's responses (default: 0.7)
- `CONFIDENCE_THRESHOLD`: Minimum confidence score for a response to be returned (default: 0.5)

## Running Tests

To run the unit tests:
```bash
python -m pytest tests/test_rag_agent.py -v
```

## Troubleshooting

- If you get 401 errors, verify your OpenAI and Qdrant API keys are correct
- If queries return no results, check that your Qdrant collection has embedded book content
- For performance issues, consider adjusting the TOP_K_RESULTS and temperature settings