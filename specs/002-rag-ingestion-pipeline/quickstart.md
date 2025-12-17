# Quickstart Guide: RAG Knowledge Ingestion Pipeline

## Overview
This guide provides step-by-step instructions to set up and run the RAG Knowledge Ingestion Pipeline that converts Docusaurus-based book websites into searchable vector knowledge bases.

## Prerequisites
- Python 3.9+
- UV package manager
- API keys for Cohere and Qdrant
- Access to the target Docusaurus website (https://physical-ai-hackathon-red.vercel.app/)

## Setup Instructions

1. **Clone the repository and navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies with UV**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install cohere qdrant-client python-dotenv requests beautifulsoup4
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory with your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

4. **Run the pipeline**
   ```bash
   python main.py
   ```

## Configuration Options

Adjust the following parameters in your `.env` file:

- `CHUNK_SIZE`: Size of text chunks (default: 1024, min: 512, max: 4096)
- `COHERE_MODEL`: Model to use for embeddings (default: 'embed-multilingual-v2.0')
- `QDRANT_COLLECTION`: Collection name in Qdrant (default: 'rag_embeddings')
- `RATE_LIMIT_DELAY`: Delay between requests in seconds (default: 1)

## Running Tests

Execute the test suite:
```bash
python -m pytest tests/
```

## Monitoring and Logging

- Check `logs/pipeline.log` for execution logs and errors
- Monitor progress through the console output
- For failed documents, review the error logs for troubleshooting

## Troubleshooting

- If you encounter rate limiting errors, increase `RATE_LIMIT_DELAY` in your configuration
- If you see memory errors with large documents, reduce the `CHUNK_SIZE`
- For connection issues with Qdrant, verify your URL and API key are correct