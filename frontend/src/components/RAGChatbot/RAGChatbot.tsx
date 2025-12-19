import React, { useState, useRef, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Define TypeScript interfaces
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

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

// Import the shared API service
import chatService from '../../api/chatService';

// Chatbot component for Docusaurus
const RAGChatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m your AI assistant for this book. Ask me anything about the content.',
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get bot response
      const response = await chatService.query({
        query: inputValue,
        top_k: 5,
        temperature: 0.7,
        include_citations: true
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error getting bot response:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
  };

  // Auto-resize textarea as user types
  useEffect(() => {
    const textarea = document.getElementById('userInput') as HTMLTextAreaElement;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    }
  }, [inputValue]);

  return (
    <div className="chatbot-container" style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      maxWidth: '600px',
      margin: '20px 0',
      backgroundColor: '#f9f9f9',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <div style={{ marginBottom: '16px', fontWeight: 'bold', fontSize: '1.1em', textAlign: 'center' }}>
        Book AI Assistant
      </div>
      <div className="chatbot-messages" style={{
        maxHeight: '400px',
        overflowY: 'auto',
        marginBottom: '16px',
        padding: '8px',
        backgroundColor: 'white',
        borderRadius: '4px'
      }}>
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              marginBottom: '12px',
              textAlign: message.sender === 'user' ? 'right' : 'left'
            }}
          >
            <div
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '18px',
                backgroundColor: message.sender === 'user' ? '#007cba' : '#e5e5e5',
                color: message.sender === 'user' ? 'white' : 'black',
                maxWidth: '80%'
              }}
            >
              {message.text}
            </div>
            <div
              style={{
                fontSize: '0.7em',
                color: '#999',
                marginTop: '4px'
              }}
            >
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={{ textAlign: 'left', marginBottom: '12px' }}>
            <div
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '18px',
                backgroundColor: '#e5e5e5',
                color: 'black',
                maxWidth: '80%'
              }}
            >
              Thinking...
            </div>
            <div
              style={{
                fontSize: '0.7em',
                color: '#999',
                marginTop: '4px'
              }}
            >
              {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
        <textarea
          id="userInput"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Ask a question about this book..."
          rows={1}
          style={{
            flex: 1,
            padding: '8px 12px',
            border: '1px solid #ccc',
            borderRadius: '18px',
            resize: 'none',
            overflow: 'hidden'
          }}
        />
        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007cba',
            color: 'white',
            border: 'none',
            borderRadius: '18px',
            cursor: isLoading ? 'not-allowed' : 'pointer'
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

// Wrapper to ensure component only renders in browser
const RAGChatbotWrapper: React.FC = () => {
  return (
    <BrowserOnly>
      {() => <RAGChatbot />}
    </BrowserOnly>
  );
};

export default RAGChatbotWrapper;