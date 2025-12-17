# Quickstart Guide: Retrieval Pipeline Testing

## Overview
This guide provides instructions to set up and use the retrieval testing CLI tool for validating vector retrieval from Qdrant using stored embeddings.

## Prerequisites
- Python 3.9+
- API keys for Cohere and Qdrant
- A populated Qdrant database with embeddings (from the RAG ingestion pipeline)

## Setup Instructions

1. **Install dependencies** (if not already installed for the main project):
   ```bash
   cd backend
   pip install cohere qdrant-client python-dotenv
   ```

2. **Set up environment variables**:
   Create or update the `.env` file in the backend directory with your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

## Basic Usage

Run a simple retrieval test:
```bash
python retrieval_test.py "What are the key features of RAG systems?"
```

## Advanced Usage

### Specify number of results
```bash
# Get top 10 results instead of default 5
python retrieval_test.py -k 10 "Your query here"
```

### Specify collection name
```bash
# Search in a specific Qdrant collection
python retrieval_test.py --collection "my_custom_collection" "Your query here"
```

### JSON output format
```bash
# Output results in JSON format
python retrieval_test.py --output json "Your query here"
```

### Log results to file
```bash
# Log results for later analysis
python retrieval_test.py --log-results "Your query here"
```

## Example Output

The tool will return results similar to:

```
Query: What are the key features of RAG systems?
Query embedding generated using model: embed-multilingual-v2.0

Retrieved 5 results:

1. RAG (Retrieval-Augmented Generation) systems combine... (Score: 0.842)
   Source: https://example.com/rag-intro
   Title: Introduction to RAG Systems
   Headings: ['What is RAG?', 'Key Components']

2. The core components of a RAG system include... (Score: 0.821)
   Source: https://example.com/rag-architecture
   Title: RAG Architecture Overview
   Headings: ['Components', 'Workflow']

[Additional results...]

Retrieval completed in 245.67 ms
```

## Troubleshooting

- If you see "Connection error", verify your Qdrant URL and API key in the `.env` file
- If you see "Authentication error", verify your API keys are correct
- If results seem irrelevant, the vector database may need more content or the query might need refinement