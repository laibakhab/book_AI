# Quickstart Guide: Frontend-Backend Integration

## Overview
This guide provides instructions to set up and run the RAG (Retrieval-Augmented Generation) frontend-backend integration. This system connects the Docusaurus-based book frontend with the RAG backend service to enable interactive Q&A functionality.

## Prerequisites
- Python 3.9+
- Node.js 16+ (if modifying the frontend)
- Docusaurus installation (for the book website)
- API keys for Cohere and Qdrant
- Git for version control

## Setup Instructions

### Backend Setup
1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Or if requirements.txt doesn't exist, install the required packages:
   pip install fastapi uvicorn cohere qdrant-client python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory with the following content:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION=rag_embeddings
   COHERE_MODEL=embed-multilingual-v2.0
   DEFAULT_TOP_K=5
   MIN_TOP_K=1
   MAX_TOP_K=20
   LOG_LEVEL=INFO
   ```

5. **Start the backend service**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup
1. **Navigate to the Docusaurus directory**
   ```bash
   cd physical-ai-hackathon
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure the API endpoint**
   In your Docusaurus configuration, ensure the API endpoint is set to connect to the backend:
   - Update `docusaurus.config.ts` or relevant config to include the API endpoint information for the Q&A component

4. **Start the frontend**
   ```bash
   npm run start
   ```

## Making API Requests

Once both services are running, you can test the integration with direct API calls:

### Submit a Query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key features of RAG systems?",
    "top_k": 3,
    "include_citations": true
  }'
```

### Check Health Status
```bash
curl -X GET "http://localhost:8000/health"
```

## Frontend Integration Points

### Adding Q&A Component
To integrate the Q&A functionality into your Docusaurus pages:

1. Create a React component that sends requests to the backend API
2. Use the `/query` endpoint to submit user questions
3. Display the response with proper citation formatting

Example integration in a Docusaurus page (using React):
```javascript
import React, { useState } from 'react';

const QAInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 3 })
      });
      
      const data = await result.json();
      setResponse(data);
    } catch (error) {
      console.error('Error submitting query:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the book content..." 
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit'}
        </button>
      </form>
      
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response.answer}</p>
          
          <h4>Citations:</h4>
          <ul>
            {response.citations.map((citation, index) => (
              <li key={index}>
                <a href={citation.source_url}>{citation.source_title}</a>: {citation.text_snippet}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
```

## Testing the Integration

1. **Verify the backend is responding**:
   - Test the `/health` endpoint to ensure all dependencies are available
   - Test the `/query` endpoint with a sample query via curl or Postman

2. **Verify frontend can reach backend**:
   - Check browser developer tools for CORS errors
   - Ensure your backend CORS settings allow requests from your frontend origin

3. **Test end-to-end functionality**:
   - Submit a query through the frontend
   - Verify the response appears correctly formatted
   - Check that citations are properly displayed

## Configuration Options

- `DEFAULT_TOP_K`: Number of results to return by default (default: 5)
- `MIN_TOP_K`, `MAX_TOP_K`: Bounds for the number of results (min: 1, max: 20)
- `LOG_LEVEL`: Level of logging detail (default: INFO)
- `COHERE_MODEL`: Model for embedding generation (default: embed-multilingual-v2.0)

## Troubleshooting

- If you get CORS errors, ensure your backend FastAPI app has CORS middleware configured appropriately
- If API keys are rejected, double-check the `.env` file and restart the backend service
- If responses are slow, verify your Cohere and Qdrant API connectivity and quotas
- If queries return no results, confirm that your Qdrant collection has content and is properly configured