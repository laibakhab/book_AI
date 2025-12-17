from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import logging

# Import our modules
from rag_agent.agents.rag_agent import RAGAgent
from rag_agent.config.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for the RAG (Retrieval-Augmented Generation) Agent that answers queries using book content",
    version="1.0.0"
)

# Initialize the RAG agent
rag_agent = RAGAgent()


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = Query(5, ge=1, le=20, description="Number of top results to retrieve")
    temperature: Optional[float] = Query(0.7, ge=0.0, le=1.0, description="Temperature for response generation")
    include_citations: Optional[bool] = True


class SourceCitation(BaseModel):
    source_document: str
    page_number: Optional[int]
    section_title: Optional[str]
    similarity_score: float


class QueryResponse(BaseModel):
    query_id: str
    original_query: str
    response: str
    confidence_score: float
    citations: List[SourceCitation]
    retrieved_chunks_count: int
    processing_time_ms: float
    timestamp: float


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Submit a query to the RAG agent and receive a grounded response based on book content.
    """
    start_time = time.time()
    
    try:
        # Validate query is not empty
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query with RAG agent
        result = rag_agent.process_query(
            query=request.query,
            top_k=request.top_k,
            temperature=request.temperature
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Format response
        response = QueryResponse(
            query_id=result.get("query_id", ""),
            original_query=request.query,
            response=result["response"],
            confidence_score=result["confidence_score"],
            citations=result["citations"],
            retrieved_chunks_count=len(result["citations"]),
            processing_time_ms=processing_time,
            timestamp=time.time()
        )
        
        logger.info(f"Processed query in {processing_time:.2f}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Check the health status of the RAG agent service and its dependencies.
    """
    # Check if we can connect to required services
    dependencies_status = {
        "openai_api": "connected" if rag_agent.check_openai_connection() else "disconnected",
        "qdrant_db": "connected" if rag_agent.check_qdrant_connection() else "disconnected",
        "agent_service": "ready"
    }
    
    overall_status = "healthy" if all(status == "connected" for status in dependencies_status.values()) else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": time.time(),
        "dependencies": dependencies_status
    }


@app.get("/stats")
async def get_stats():
    """
    Get statistics about the RAG agent's performance and usage.
    """
    stats = rag_agent.get_performance_stats()
    return stats


# Run the application with uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)