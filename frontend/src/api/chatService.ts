// API service to connect to the RAG backend  
  
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';  
  
interface QueryRequest {  
  query: string;  
  top_k?: number;  
  temperature?: number;  
  include_citations?: boolean;  
}  
  
interface QueryResponse {  
  query_id: string;  
  original_query: string;  
  response: string;  
  confidence_score: number;  
  citations: SourceCitation[];  
  retrieved_chunks_count: number;  
  processing_time_ms: number;  
  timestamp: number;  
}  
  
interface SourceCitation {  
  source_document: string;  
  page_number?: number;  
  section_title?: string;  
  similarity_score: number;  
}  
  
class ChatService {  
