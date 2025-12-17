from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import time


class QueryRequest(BaseModel):
    """
    Model for incoming query requests to the RAG agent.
    """
    query: str = Field(..., description="The user's query about book content", min_length=1)
    top_k: int = Field(default=5, ge=1, le=20, description="Number of top results to retrieve from vector database")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature parameter for response generation")
    include_citations: bool = Field(default=True, description="Whether to include source citations in the response")


class SourceCitation(BaseModel):
    """
    Model representing a citation to a source document.
    """
    source_document: str = Field(..., description="Name or identifier of the source document")
    page_number: Optional[int] = Field(None, description="Page number in the source document")
    section_title: Optional[str] = Field(None, description="Title of the section where the information appears")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score between query and source content")


class QueryResponse(BaseModel):
    """
    Model for responses from the RAG agent.
    """
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for this query")
    original_query: str = Field(..., description="The original query text submitted by the user")
    response: str = Field(..., description="The agent's response to the query")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the response accuracy")
    citations: List[SourceCitation] = Field(default=[], description="List of citations for the information in the response")
    retrieved_chunks_count: int = Field(..., description="Number of content chunks retrieved to generate the response")
    processing_time_ms: float = Field(..., description="Time taken to process the query in milliseconds")
    timestamp: float = Field(default_factory=time.time, description="Timestamp of when the response was generated")


class HealthStatus(BaseModel):
    """
    Model for health check responses.
    """
    status: str = Field(..., description="Overall health status of the service", regex=r"^(healthy|unhealthy)$")
    timestamp: float = Field(default_factory=time.time, description="Timestamp of the health check")
    dependencies: dict = Field(..., description="Status of dependent services")


class PerformanceMetrics(BaseModel):
    """
    Model for performance metrics responses.
    """
    total_queries: int = Field(..., description="Total number of queries processed")
    failed_queries: int = Field(..., description="Number of queries that failed processing")
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Success rate of query processing")
    average_processing_time_ms: float = Field(..., description="Average processing time in milliseconds")
    timestamp: float = Field(default_factory=time.time, description="Timestamp of the metrics collection")