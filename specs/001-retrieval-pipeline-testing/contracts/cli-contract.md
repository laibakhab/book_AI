# CLI Interface Contract: Retrieval Pipeline Testing

## Command-Line Interface

### Main Command
`python retrieval_test.py [options]`

**Description**: The main command for testing the RAG retrieval pipeline against a Qdrant vector database.

## Arguments and Options

### Positional Arguments
- `query` (required): The text query to test against the vector database
  - Type: string
  - Example: `"What are the key features of the RAG system?"`

### Optional Arguments
- `-k`, `--top-k` (optional): Number of top results to retrieve (default: 5)
  - Type: integer
  - Range: 1-100
  - Example: `-k 10` or `--top-k 10`

- `-c`, `--collection` (optional): Name of the Qdrant collection to search (default: "rag_embeddings")
  - Type: string
  - Example: `-c "my_collection"`

- `-o`, `--output` (optional): Output format (text or json, default: text)
  - Type: string
  - Values: "text", "json"
  - Example: `-o json`

- `-l`, `--log-results` (optional): Whether to log results to a file
  - Type: boolean flag
  - Example: `-l` or `--log-results`

## Exit Codes

- `0`: Success - retrieval completed successfully
- `1`: General error - unexpected error occurred
- `2`: Configuration error - missing API keys or invalid configuration
- `3`: Connection error - unable to connect to Qdrant or Cohere
- `4`: Invalid input - invalid query or parameters

## Input Validation

- Query text must not be empty or only whitespace
- Top-k value must be between 1 and 100
- Collection name must follow Qdrant naming conventions

## Expected Output (Text Format)

```
Query: [original query text]
Query embedding generated using model: [model name]

Retrieved 5 results:

1. [Chunk text content excerpt...] (Score: 0.XXX)
   Source: [URL]
   Title: [Document title]
   Headings: [list of headings]

2. [Chunk text content excerpt...] (Score: 0.XXX)
   Source: [URL]
   Title: [Document title]
   Headings: [list of headings]

[Additional results...]

Retrieval completed in [X.XX] ms
```

## Expected Output (JSON Format)

```json
{
  "query": "original query text",
  "query_embedding_model": "model name",
  "collection": "collection name",
  "top_k": 5,
  "results": [
    {
      "chunk_id": "unique chunk identifier",
      "text_content": "full text content of the chunk",
      "similarity_score": 0.XXX,
      "source_url": "source URL",
      "source_title": "document title",
      "headings": ["list", "of", "headings"],
      "chunk_index": 0
    }
  ],
  "execution_time_ms": 123.45,
  "timestamp": "2023-01-01T12:00:00Z"
}
```

## Error Output

When output format is JSON, errors will be returned as:

```json
{
  "error": "error message",
  "error_code": 1,
  "timestamp": "2023-01-01T12:00:00Z"
}
```

When output format is text, errors will be returned as:
```
Error: [error message]
Code: [error code]
```