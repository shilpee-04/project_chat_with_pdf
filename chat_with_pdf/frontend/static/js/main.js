
let chatHistory = [];
let currentStoreIds = [];
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('pdf-upload');
    const processBtn = document.getElementById('process-btn');
    
    // File upload handling
    dropZone.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            dropZone.innerHTML = `<p>${e.target.files.length} PDF file(s) selected</p>`;
        }
    });
    
    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropZone.classList.add('highlight');
    }
    
    function unhighlight() {
        dropZone.classList.remove('highlight');
    }
    
    dropZone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        
        if (files.length > 0) {
            dropZone.innerHTML = `<p>${files.length} PDF file(s) selected</p>`;
        }
    }
    
    // Process button handler
processBtn.addEventListener('click', async () => {
    const files = fileInput.files;
    if (files.length === 0) {
        alert('Please select at least one PDF file');
        return;
    }
    
    // Show loading state
    processBtn.textContent = 'Processing...';
    processBtn.disabled = true;
    
    try {
        // Create FormData and append files
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        
        // Send to backend
        const response = await fetch('/api/v1/pdf/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Processing result:', result);
        
        // Store the vector store IDs for future chats
        sessionStorage.setItem('store_ids', JSON.stringify(result.store_ids));
        
        // Show chat interface
        document.getElementById('upload-section').style.display = 'none';
        document.getElementById('chat-section').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process files');
    } finally {
        processBtn.textContent = 'Process Documents';
        processBtn.disabled = false;
    }
});

    
    // Chat functionality
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Get conversation mode
    const mode = document.querySelector('input[name="mode"]:checked').value;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input and show loading
    userInput.value = '';
    showTypingIndicator();
    
    // Get store IDs from session storage
    const storeIds = JSON.parse(sessionStorage.getItem('store_ids') || '[]');
    
    // Send to backend
    fetch('/api/v1/chat/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: message,
            store_ids: storeIds,
            chat_history: chatHistory,
            mode: mode
        })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        
        if (data.response) {
            addMessageToChat(data.response, 'assistant');
            
            // Update chat history
            chatHistory.push({role: 'user', content: message});
            chatHistory.push({role: 'assistant', content: data.response});
            
            // Keep only last 10 messages for context
            if (chatHistory.length > 10) {
                chatHistory = chatHistory.slice(-10);
            }
        } else {
            addMessageToChat('Sorry, I encountered an error.', 'assistant');
        }
    })
    .catch(error => {
        hideTypingIndicator();
        console.error('Chat error:', error);
        addMessageToChat('Sorry, I encountered an error.', 'assistant');
    });
}

function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `
        <div class="message-content">
            <strong>${sender === 'user' ? 'You' : 'Assistant'}:</strong>
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message assistant-message';
    typingDiv.innerHTML = '<div class="message-content"><p>Assistant is typing...</p></div>';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
});
