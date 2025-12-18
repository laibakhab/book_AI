import React from 'react';
import './App.css';
import Chatbot from './components/Chatbot/Chatbot';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Book AI Assistant</h1>
      </header>
      <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
        <Chatbot />
      </main>
    </div>
  );
}

export default App;
