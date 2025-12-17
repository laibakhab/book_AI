# Data Model: RAG Agent Backend

## Entities

### QueryText
Represents the user's original query text to the RAG system

**Attributes**:
- `text` (string): The original query text from the user
- `timestamp` (datetime): When the query was submitted
- `user_id` (string, optional): Identifier of the user who submitted the query (for tracking purposes)
- `session_id` (string, optional): Identifier for the conversation session (for multi-turn conversations)

### RetrievedPassage
Content segment retrieved from the vector database based on query similarity

**Attributes**:
- `passage_id` (string): Unique identifier for the retrieved passage
- `text_content` (string): The actual text content of the passage
- `similarity_score` (float): Similarity score between 0 and 1 indicating relevance to query
- `source_document` (string): Name or identifier of the source document/book
- `source_location` (string): Specific location in the document (page, section, etc.)
- `metadata` (dict): Additional metadata from the vector database entry

### GroundedResponse
Agent-generated response that is grounded in retrieved content

**Attributes**:
- `response_id` (string): Unique identifier for this response
- `generated_text` (string): The text of the agent's response
- `confidence_score` (float): Confidence score between 0 and 1 for the response accuracy
- `source_citations` (list of strings): List of source identifiers cited in the response
- `query_id` (string): Reference to the original query that generated this response
- `timestamp` (datetime): When the response was generated
- `validation_status` (enum): ['valid', 'needs_review', 'invalid'] - status of fact-checking validation

### QuerySession
Tracks conversation history for multi-turn interactions

**Attributes**:
- `session_id` (string): Unique identifier for the conversation session
- `start_time` (datetime): When the session started
- `last_activity_time` (datetime): When the last query was processed
- `query_history` (list of QueryText ids): References to queries in this session
- `response_history` (list of GroundedResponse ids): References to responses in this session
- `status` (enum): ['active', 'closed', 'expired'] - current state of the session

## Relationships

- One `QuerySession` → Many `QueryText` objects (one-to-many relationship)
- One `QueryText` → One `GroundedResponse` (one-to-one relationship for each query-response pair)
- One `GroundedResponse` → Many `RetrievedPassage` references (one-to-many relationship for grounding)
- One `RetrievedPassage` → Many `GroundedResponse` references (one-to-many relationship as passages can be cited in multiple responses)

## Validation Rules

**For QueryText**:
- `text` must not be empty or only whitespace (after trimming)
- `user_id` must follow standard identifier format if present
- `session_id` must be a valid session if present

**For RetrievedPassage**:
- `similarity_score` must be between 0 and 1
- `text_content` must not exceed maximum token length for the model
- `source_document` must be a valid document in the vector database
- `source_location` should follow standard document referencing format

**For GroundedResponse**:
- `confidence_score` must be between 0 and 1
- `source_citations` must reference actual retrieved passages
- `generated_text` should be substantiated by cited sources
- `validation_status` reflects the outcome of fact-checking

**For QuerySession**:
- `session_id` must be unique across active sessions
- Sessions should expire after a configurable timeout period
- Query and response histories should be ordered chronologically