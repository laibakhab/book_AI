# Data Model: Frontend-Backend Integration

## Entities

### UserQuery
Represents a query submitted by a user through the frontend interface

**Attributes:**
- `query_id` (string): Unique identifier for the query
- `query_text` (string): The actual text of the user's query
- `timestamp` (datetime): When the query was submitted
- `user_session_id` (string, optional): Identifier for the user's session (for tracking conversation history)
- `source_page_url` (string): URL of the page where the query was submitted

### ApiResponse
Represents the response from the RAG backend service

**Attributes:**
- `response_id` (string): Unique identifier for the response
- `query_id` (string): Reference to the original query
- `answer_text` (string): The AI-generated answer to the query
- `confidence_score` (float): Confidence score between 0 and 1
- `source_citations` (list of Citation objects): References to source content used in the response
- `processing_time_ms` (float): Time taken to process the query
- `timestamp` (datetime): When the response was generated
- `error_info` (string, optional): Error details if the response generation failed

### Citation
Represents a reference to specific content in the book that was used to generate the response

**Attributes:**
- `citation_id` (string): Unique identifier for the citation
- `source_url` (string): URL to the source content
- `source_title` (string): Title of the source page/chapter
- `section_title` (string): Section heading where the information appears
- `page_number` (number): Page number in the original book (if applicable)
- `similarity_score` (float): Relevance score between 0 and 1
- `text_snippet` (string): Excerpt of the content that supports the answer

### QuerySession
Represents a user session for tracking conversation history (future enhancement)

**Attributes:**
- `session_id` (string): Unique identifier for the session
- `start_time` (datetime): When the session began
- `last_activity_time` (datetime): When the last query was processed
- `query_history` (list of UserQuery objects): Sequence of queries in this session
- `response_history` (list of ApiResponse objects): Corresponding responses to the queries
- `conversation_context` (string): Summary of conversation context for multi-turn interactions

## Relationships

- One `QuerySession` → Many `UserQuery` objects (one-to-many, optional if single-turn conversations)
- One `UserQuery` → One `ApiResponse` (one-to-one relationship)
- One `ApiResponse` → Many `Citation` objects (one-to-many relationship)

## Validation Rules

**For UserQuery:**
- `query_text` must not be empty or only whitespace after trimming
- `query_text` must be less than 2000 characters to prevent overly long requests
- `source_page_url` must be a valid URL

**For ApiResponse:**
- `confidence_score` must be between 0 and 1
- `processing_time_ms` must be non-negative
- `source_citations` must be a list (even if empty)

**For Citation:**
- `similarity_score` must be between 0 and 1
- `source_url` must be a valid URL format
- `text_snippet` must not exceed 5000 characters

**For QuerySession:**
- `session_id` must be unique for active sessions
- Session should expire after 30 minutes of inactivity
- `query_history` and `response_history` must be of equal length