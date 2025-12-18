// Chatbot functionality
document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Auto-resize textarea as user types
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message when clicking the send button
    sendButton.addEventListener('click', sendMessage);

    // Send message when pressing Enter (without Shift)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Function to handle sending messages
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessageToChat(message, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show typing indicator
        const botTyping = addBotTypingIndicator();
        
        try {
            // Call the backend API to get response
            const response = await getBotResponse(message);
            
            // Remove typing indicator
            chatMessages.removeChild(botTyping);
            
            // Add bot response to chat
            addMessageToChat(response, 'bot');
        } catch (error) {
            // Remove typing indicator
            chatMessages.removeChild(botTyping);
            
            // Show error message
            addMessageToChat('Sorry, I encountered an error processing your request. Please try again.', 'bot');
            console.error('Error getting bot response:', error);
        }
    }

    // Function to add a message to the chat interface
    function addMessageToChat(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'message--user' : 'message--bot');
        
        const messageText = document.createElement('div');
        messageText.classList.add('message-text');
        messageText.textContent = text;
        
        const timestamp = document.createElement('div');
        timestamp.classList.add('message-timestamp');
        timestamp.textContent = getCurrentTime();
        
        messageDiv.appendChild(messageText);
        messageDiv.appendChild(timestamp);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to add a typing indicator for the bot
    function addBotTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'message--bot');
        typingDiv.id = 'typing-indicator';
        
        const typingText = document.createElement('div');
        typingText.classList.add('message-text');
        typingText.textContent = 'Thinking...';
        
        const timestamp = document.createElement('div');
        timestamp.classList.add('message-timestamp');
        timestamp.textContent = getCurrentTime();
        
        typingDiv.appendChild(typingText);
        typingDiv.appendChild(timestamp);
        
        chatMessages.appendChild(typingDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return typingDiv;
    }

    // Function to get the current time in HH:MM format
    function getCurrentTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    }

    // Function to get response from the backend API
    async function getBotResponse(userMessage) {
        const response = await fetch('http://localhost:8000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: userMessage,
                top_k: 5,
                temperature: 0.7,
                include_citations: true
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    }
});