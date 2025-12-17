# Research: Retrieval Pipeline Testing

## Decision: Technology Stack Selection
**Rationale**: For the retrieval pipeline testing tool, we chose Python as the primary language due to its rich ecosystem for vector databases and NLP. We specifically selected the Cohere embedding model for its consistency with the ingestion pipeline and Qdrant as the vector database for its performance and ease of use.

**Alternatives considered**:
- OpenAI embeddings vs. Cohere: Cohere was selected for consistency with the ingestion pipeline 
- Pinecone vs. Qdrant vs. Weaviate: Qdrant was chosen as it's the same database used in the ingestion pipeline
- Hugging Face transformers vs. Cohere API: The Cohere API was selected for consistency with the ingestion pipeline

## Decision: Command-Line Interface (CLI) Design
**Rationale**: A CLI tool was chosen for the retrieval testing system as it enables backend engineers and RAG evaluators to quickly test queries against the vector database. This approach allows for easy scripting and integration into validation workflows.

**Alternatives considered**:
- Web-based UI vs. CLI: CLI was chosen as it's simpler to implement and suitable for the target users (backend engineers)
- API-based interface vs. CLI: CLI was chosen for direct testing without the need for a running server

## Decision: Query Processing Workflow
**Rationale**: The workflow will follow these steps:
1. Accept user query from command line
2. Generate embedding for the query using Cohere (same model as ingestion)
3. Search Qdrant for top-K similar vectors
4. Print retrieved chunks with metadata
5. Log results for relevance validation

**Alternatives considered**:
- Different order of operations: The chosen order ensures we generate the query embedding before searching
- Different output format: Plain text with metadata was chosen for easy interpretation

## Decision: Configuration Management
**Rationale**: Using python-dotenv for configuration management allows easy management of API keys and settings without hardcoding values. This follows security best practices.

**Alternatives considered**:
- Environment variables only vs. config files: A hybrid approach was selected using .env files
- Command-line arguments vs. config files: Config files were preferred for API keys to avoid exposing them in command history

## Decision: Top-K Retrieval Value
**Rationale**: Defaulting to K=5 for top-K retrieval balances between providing sufficient context for evaluation while not overwhelming the user with too many results.

**Alternatives considered**:
- K=3 vs. K=5 vs. K=10: K=5 was chosen as a balanced default that can be configured as needed
- Fixed vs. configurable value: A configurable value was selected to allow flexibility