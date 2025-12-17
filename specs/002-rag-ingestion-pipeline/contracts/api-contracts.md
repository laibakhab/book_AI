# API Contracts: RAG Knowledge Ingestion Pipeline

This document defines the API contracts for the RAG Knowledge Ingestion Pipeline. Currently, this is primarily a data processing pipeline, but we define contracts for potential future API endpoints.

## Ingestion API

### Start Ingestion Job
- **Endpoint**: `POST /api/v1/ingest`
- **Description**: Initiates a new ingestion job for a Docusaurus site
- **Request**:
  ```json
  {
    "source_url": "https://example-docusaurus-site.com",
    "chunk_size": 1024,
    "model_name": "embed-multilingual-v2.0",
    "collection_name": "rag_embeddings"
  }
  ```
- **Response**:
  - 202: Job accepted
    ```json
    {
      "job_id": "job-12345",
      "status": "started",
      "estimated_completion": "2023-01-01T12:00:00Z"
    }
    ```
  - 400: Invalid request
  - 500: Server error

### Get Ingestion Job Status
- **Endpoint**: `GET /api/v1/ingest/{job_id}`
- **Description**: Returns the current status of an ingestion job
- **Response**:
  - 200: Job status
    ```json
    {
      "job_id": "job-12345",
      "status": "running",
      "pages_crawled": 150,
      "pages_failed": 5,
      "chunks_created": 420,
      "start_time": "2023-01-01T10:00:00Z",
      "end_time": null,
      "error_log": ["Error processing page X"]
    }
    ```
  - 404: Job not found

## Search API

### Semantic Search
- **Endpoint**: `POST /api/v1/search`
- **Description**: Performs semantic search on the ingested content
- **Request**:
  ```json
  {
    "query": "your search query",
    "collection_name": "rag_embeddings",
    "limit": 10,
    "filters": {
      "url": "optional URL filter"
    }
  }
  ```
- **Response**:
  - 200: Search results
    ```json
    {
      "query": "your search query",
      "results": [
        {
          "id": "chunk-123",
          "score": 0.95,
          "text": "relevant text content",
          "metadata": {
            "url": "https://source-page.com",
            "title": "Source Page Title",
            "headings": ["Heading 1", "Subheading"]
          }
        }
      ]
    }
    ```
  - 400: Invalid request

## Configuration API

### Get Configuration
- **Endpoint**: `GET /api/v1/config`
- **Description**: Returns current system configuration
- **Response**:
  - 200: Configuration
    ```json
    {
      "chunk_size": 1024,
      "model_name": "embed-multilingual-v2.0",
      "collection_name": "rag_embeddings",
      "rate_limit_delay": 1.0
    }
    ```

### Update Configuration
- **Endpoint**: `PUT /api/v1/config`
- **Description**: Updates system configuration
- **Request**:
  ```json
  {
    "chunk_size": 2048,
    "model_name": "embed-multilingual-v2.0",
    "rate_limit_delay": 2.0
  }
  ```
- **Response**:
  - 200: Configuration updated
  - 400: Invalid configuration values