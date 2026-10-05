let currentLocation = null;

// Handle Enter key in input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Send message to backend
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Translate response if multilingual is enabled
        let translatedResponse = data.response;
        if (window.multilingualManager && window.multilingualManager.getCurrentLanguage() !== 'en') {
            translatedResponse = await window.multilingualManager.translateWeatherResponse(data.response);
        }
        
        // Add bot response
        addMessage(translatedResponse, 'bot');
        
        // Speak response if voice assistant is enabled
        if (window.voiceAssistant && window.voiceAssistant.isEnabled()) {
            window.voiceAssistant.speak(translatedResponse);
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        console.error('Error:', error);
    }
}

// Add message to chat
function addMessage(text, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `<p>${text}</p>`;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    // Use translated typing indicator based on current language
    let typingText = '🤔 Thinking...';
    if (window.multilingualManager) {
        const lang = window.multilingualManager.getCurrentLanguage();
        const typingTranslations = {
            'ta': '🤔 நினைக்கிறது...',
            'hi': '🤔 सोच रहा हूं...',
            'te': '🤔 ఆలోచిస్తోంది...',
            'ml': '🤔 ചിന്തുന്നു...',
            'kn': '🤔 ಆಲೋಚಿಸುತ್ತಾದೆ...',
            'bn': '🤔 ভাবছা করছি...',
            'mr': '🤔 विचारत आहे...',
            'gu': '🤔 વિચારુ છું...'
        };
        typingText = typingTranslations[lang] || typingText;
    }
    
    typingDiv.innerHTML = `<p>${typingText}</p>`;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Get weather for specific location (can be called from map)
function askAboutLocation(lat, lng) {
    const input = document.getElementById('user-input');
    input.value = `What's the weather at ${lat.toFixed(4)}, ${lng.toFixed(4)}?`;
    sendMessage();
}