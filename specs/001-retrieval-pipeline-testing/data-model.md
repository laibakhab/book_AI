# Data Model: Retrieval Pipeline Testing

## Entities

### QueryText
Represents the original text input from a user

**Attributes:**
- `text` (string): The raw query text input by the user
- `timestamp` (datetime): When the query was submitted
- `user_id` (string, optional): Identifier of the user who submitted the query (for logging purposes)

### QueryEmbedding
Vector representation of the query text

**Attributes:**
- `vector` (list of floats): The embedding vector values (dimension depends on model used)
- `model_name` (string): Name of the model used to generate the embedding
- `model_version` (string): Version of the model used
- `query_text_id` (string): Reference to the original QueryText

### RetrievedChunk
Content segment retrieved from Qdrant

**Attributes:**
- `chunk_id` (string): Unique identifier for the retrieved chunk
- `text_content` (string): The actual text content of the chunk
- `similarity_score` (float): Cosine similarity score compared to the query
- `source_url` (string): The URL where the original content was sourced from
- `source_title` (string): The title of the source page
- `headings` (list of strings): List of headings associated with this chunk
- `retrieval_result_id` (string): Reference to the parent RetrievalResult

### RetrievalResult
Aggregated set of retrieved chunks

**Attributes:**
- `result_id` (string): Unique identifier for this retrieval result
- `query_text` (string): The original query text
- `query_embedding_id` (string): Reference to the query embedding used
- `top_k` (integer): The number of top results requested
- `total_chunks_retrieved` (integer): Total number of chunks in this result
- `execution_time_ms` (float): Time taken to execute the retrieval
- `timestamp` (datetime): When the retrieval was performed

## Relationships

- One `QueryText` → One `QueryEmbedding`
- One `QueryEmbedding` → Many `RetrievedChunk` (via `RetrievalResult`)
- One `RetrievalResult` → Many `RetrievedChunk`

## Validation Rules

- `QueryText.text` must not be empty
- `QueryEmbedding.vector` length must match the dimensions expected by the model
- `RetrievedChunk.similarity_score` must be between 0 and 1
- `RetrievalResult.top_k` must be a positive integer
- `RetrievedChunk.source_url` must be a valid URL format