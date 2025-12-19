import React from 'react';
import Layout from '@theme/Layout';
import RAGChatbot from '../components/RAGChatbot/RAGChatbot';

export default function ChatbotDemo(): React.ReactNode {
  return (
    <Layout title="AI Book Assistant Demo" description="Demo of the RAG-powered chatbot">
      <div style={{ padding: '20px' }}>
        <h1>AI Book Assistant Demo</h1>
        <p>Try out our RAG-powered chatbot below:</p>
        
        <RAGChatbot />
      </div>
    </Layout>
  );
}