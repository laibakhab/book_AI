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
  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${BACKEND_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async healthCheck(): Promise<any> {
    const response = await fetch(`${BACKEND_URL}/health`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async getStats(): Promise<any> {
    const response = await fetch(`${BACKEND_URL}/stats`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

export default new ChatService();
