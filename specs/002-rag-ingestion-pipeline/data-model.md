# Data Model: RAG Knowledge Ingestion Pipeline

## Entities

### CrawledPage
Represents a single page from the Docusaurus book website

**Attributes:**
- `url` (string): The original URL of the page
- `raw_html` (string): The raw HTML content of the page (optional, for debugging)
- `clean_text` (string): The extracted, cleaned text content
- `title` (string): The page title extracted from HTML
- ` headings` (list of strings): List of headings found in the page
- `crawl_timestamp` (datetime): When the page was crawled
- `word_count` (integer): Number of words in the clean text
- `processing_status` (enum): ['pending', 'success', 'error']
- `error_message` (string, optional): Error details if processing failed

### ContentChunk
Represents a segment of text extracted from a page

**Attributes:**
- `chunk_id` (string): Unique identifier for this chunk
- `text_content` (string): The actual text content of this chunk
- `source_url` (string): The URL from which this chunk originated
- `source_title` (string): The title of the source page
- `headings_hierarchy` (list of strings): Hierarchical headings leading to this chunk
- `chunk_position` (integer): Position of this chunk within the source page
- `word_count` (integer): Number of words in the chunk
- `embedding_vector` (list of floats): The embedding vector for semantic search
- `metadata` (dict): Additional metadata about the chunk
  - `original_url` (string): Original source URL
  - `section` (string): Section or chapter name if available
  - `tags` (list of strings): Tags associated with the content

### Embedding
Vector representation of content chunk

**Attributes:**
- `chunk_id` (string): Reference to the source content chunk
- `vector` (list of floats): The embedding vector values (dimension depends on model used)
- `model_name` (string): Name of the model used to generate the embedding
- `model_version` (string): Version of the model used
- `embedding_timestamp` (datetime): When the embedding was generated

### IngestionJob
Represents a single execution of the pipeline

**Attributes:**
- `job_id` (string): Unique identifier for the ingestion job
- `start_time` (datetime): When the job started
- `end_time` (datetime): When the job completed (null if running)
- `status` (enum): ['running', 'completed', 'failed', 'cancelled']
- `source_url` (string): The root URL of the site being ingested
- `pages_crawled_count` (integer): Total number of pages successfully crawled
- `pages_failed_count` (integer): Number of pages that failed to process
- `chunks_created_count` (integer): Total number of content chunks created
- `error_log` (list of strings): List of errors encountered during the job
- `crawl_rate_limit` (float): Delay between requests in seconds
- `chunk_size` (integer): Size of text chunks in tokens
- `model_name` (string): Model used for embeddings
- `collection_name` (string): Name of Qdrant collection used

## Relationships

- One `IngestionJob` → Many `CrawledPage` instances
- One `CrawledPage` → Many `ContentChunk` instances
- One `ContentChunk` → One `Embedding` (optional, until embedded)
- One `Embedding` → One `ContentChunk`

## Validation Rules

- `CrawledPage.url` must be a valid URL format
- `CrawledPage.clean_text` must not be empty when processing status is 'success'
- `ContentChunk.chunk_id` must be unique across all chunks
- `ContentChunk.text_content` length must be within configured chunk size limits
- `Embedding.vector` length must match the dimensions expected by the model
- `IngestionJob.source_url` must be a valid URL format
- `IngestionJob.chunk_size` must be between 512 and 4096 tokens