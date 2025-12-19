// API service to connect to the RAG backend in Docusaurus

// Docusaurus-compatible way to handle environment variables
// Use window object to store the backend URL
const BACKEND_URL =
  typeof window !== 'undefined'
    ? (window as any).__BACKEND_URL__ || 'http://localhost:8000'
    : 'http://localhost:8000';

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

class DocusaurusChatService {
  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${BACKEND_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(request),
      // Add credentials include to handle cookies if needed
      credentials: 'include'
    });

    if (!response.ok) {
      // Try to get error message from response body
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorBody = await response.json();
        if (errorBody.detail) {
          errorMessage += ` - ${errorBody.detail}`;
        }
      } catch (e) {
        // If we can't parse the error body, use the default message
      }
      throw new Error(errorMessage);
    }

    return await response.json();
  }

  async healthCheck(): Promise<any> {
    const response = await fetch(`${BACKEND_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

export default new DocusaurusChatService();