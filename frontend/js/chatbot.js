/**
 * DeepGuard - AI Chatbot Module
 * Educational chatbot for deepfake awareness and guidance
 */

// Chatbot Configuration
const CHATBOT_CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    MAX_MESSAGE_LENGTH: 500,
    TYPING_DELAY: 50,
    MESSAGE_DELAY: 300
};

// Chatbot State
let chatbotState = {
    isOpen: false,
    isTyping: false,
    messageHistory: [],
    initialized: false
};

// DOM Elements
let chatbotElements = {};

/**
 * Initialize chatbot when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeChatbot();
});

/**
 * Initialize chatbot elements and event listeners
 */
function initializeChatbot() {
    // Get DOM elements
    chatbotElements = {
        widget: document.getElementById('chatbotWidget'),
        toggle: document.getElementById('chatbotToggle'),
        window: document.getElementById('chatbotWindow'),
        close: document.getElementById('chatbotClose'),
        messages: document.getElementById('chatbotMessages'),
        suggestions: document.getElementById('chatbotSuggestions'),
        input: document.getElementById('chatbotInput'),
        send: document.getElementById('chatbotSend')
    };

    // Check if elements exist
    if (!chatbotElements.toggle) {
        console.warn('Chatbot elements not found');
        return;
    }

    // Add event listeners
    chatbotElements.toggle.addEventListener('click', toggleChatbot);
    chatbotElements.close.addEventListener('click', closeChatbot);
    chatbotElements.send.addEventListener('click', sendMessage);
    chatbotElements.input.addEventListener('keypress', handleInputKeypress);
    chatbotElements.input.addEventListener('input', handleInputChange);

    chatbotState.initialized = true;
    console.log('🤖 GuardBot initialized');
}

/**
 * Toggle chatbot window
 */
function toggleChatbot() {
    if (chatbotState.isOpen) {
        closeChatbot();
    } else {
        openChatbot();
    }
}

/**
 * Open chatbot window
 */
function openChatbot() {
    chatbotState.isOpen = true;
    chatbotElements.window.classList.remove('hidden');
    chatbotElements.toggle.classList.add('active');
    chatbotElements.input.focus();

    // Show welcome message if first time
    if (chatbotState.messageHistory.length === 0) {
        showWelcomeMessage();
    }
}

/**
 * Close chatbot window
 */
function closeChatbot() {
    chatbotState.isOpen = false;
    chatbotElements.window.classList.add('hidden');
    chatbotElements.toggle.classList.remove('active');
}

/**
 * Show welcome message
 */
async function showWelcomeMessage() {
    try {
        const response = await fetch(`${CHATBOT_CONFIG.API_BASE_URL}/api/chat/welcome`);
        const data = await response.json();

        if (data.success) {
            addBotMessage(data.message);
            showSuggestions(data.suggestions);
        } else {
            addBotMessage("👋 Hi! I'm **GuardBot**, your AI assistant for deepfake education. How can I help you today?");
            showDefaultSuggestions();
        }
    } catch (error) {
        console.error('Error fetching welcome message:', error);
        addBotMessage("👋 Hi! I'm **GuardBot**, your AI assistant for deepfake education. How can I help you today?");
        showDefaultSuggestions();
    }
}

/**
 * Show default suggestions
 */
function showDefaultSuggestions() {
    showSuggestions([
        "What is a deepfake?",
        "How to detect them?",
        "Protection tips"
    ]);
}

/**
 * Handle input keypress
 */
function handleInputKeypress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

/**
 * Handle input change
 */
function handleInputChange() {
    const hasText = chatbotElements.input.value.trim().length > 0;
    chatbotElements.send.disabled = !hasText;
}

/**
 * Send message to chatbot
 */
async function sendMessage() {
    const message = chatbotElements.input.value.trim();

    if (!message || chatbotState.isTyping) return;

    // Clear input
    chatbotElements.input.value = '';
    chatbotElements.send.disabled = true;

    // Add user message
    addUserMessage(message);

    // Hide suggestions
    clearSuggestions();

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch(`${CHATBOT_CONFIG.API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Remove typing indicator
        hideTypingIndicator();

        if (data.success) {
            // Simulate typing effect
            await typeMessage(data.response);

            // Show suggestions
            if (data.suggestions && data.suggestions.length > 0) {
                showSuggestions(data.suggestions);
            }
        } else {
            addBotMessage("I'm sorry, I couldn't process that. Please try again!");
            showDefaultSuggestions();
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTypingIndicator();
        addBotMessage("I'm having trouble connecting. Please make sure the server is running!");
        showDefaultSuggestions();
    }
}

/**
 * Add user message to chat
 */
function addUserMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-message user-message';
    messageEl.innerHTML = `
        <div class="message-content">${escapeHtml(message)}</div>
        <div class="message-time">${getCurrentTime()}</div>
    `;

    chatbotElements.messages.appendChild(messageEl);
    scrollToBottom();

    chatbotState.messageHistory.push({ role: 'user', content: message });
}

/**
 * Add bot message to chat
 */
function addBotMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-message bot-message';
    messageEl.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="message-content">${formatMarkdown(message)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    chatbotElements.messages.appendChild(messageEl);
    scrollToBottom();

    chatbotState.messageHistory.push({ role: 'bot', content: message });
}

/**
 * Type message with animation
 */
async function typeMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-message bot-message';
    messageEl.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="message-content"></div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    chatbotElements.messages.appendChild(messageEl);
    const contentEl = messageEl.querySelector('.message-content');

    // For long messages, just show them directly
    if (message.length > 500) {
        contentEl.innerHTML = formatMarkdown(message);
        scrollToBottom();
    } else {
        // Animate shorter messages
        const formattedMessage = formatMarkdown(message);
        contentEl.innerHTML = formattedMessage;
        scrollToBottom();
    }

    chatbotState.messageHistory.push({ role: 'bot', content: message });
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    chatbotState.isTyping = true;

    const typingEl = document.createElement('div');
    typingEl.className = 'chat-message bot-message typing-indicator';
    typingEl.id = 'typingIndicator';
    typingEl.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatbotElements.messages.appendChild(typingEl);
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    chatbotState.isTyping = false;
    const typingEl = document.getElementById('typingIndicator');
    if (typingEl) {
        typingEl.remove();
    }
}

/**
 * Show suggestions
 */
function showSuggestions(suggestions) {
    chatbotElements.suggestions.innerHTML = '';

    suggestions.forEach(suggestion => {
        const btn = document.createElement('button');
        btn.className = 'suggestion-btn';
        btn.textContent = suggestion;
        btn.addEventListener('click', () => {
            chatbotElements.input.value = suggestion;
            sendMessage();
        });
        chatbotElements.suggestions.appendChild(btn);
    });
}

/**
 * Clear suggestions
 */
function clearSuggestions() {
    chatbotElements.suggestions.innerHTML = '';
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatbotElements.messages.scrollTop = chatbotElements.messages.scrollHeight;
}

/**
 * Get current time formatted
 */
function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format markdown-like syntax to HTML
 */
function formatMarkdown(text) {
    return text
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Line breaks
        .replace(/\n/g, '<br>')
        // Bullet points
        .replace(/^[•\-]\s/gm, '<span class="bullet">•</span> ')
        // Numbered lists
        .replace(/^(\d+)\.\s/gm, '<span class="number">$1.</span> ')
        // Headers (simple)
        .replace(/^#{1,3}\s+(.+)$/gm, '<strong class="header">$1</strong>');
}

/**
 * Sleep utility
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Export for external use
window.ChatBot = {
    open: openChatbot,
    close: closeChatbot,
    toggle: toggleChatbot,
    sendMessage: (msg) => {
        chatbotElements.input.value = msg;
        sendMessage();
    }
};
