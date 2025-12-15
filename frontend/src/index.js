import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatWidget from './components/ChatWidget';

// Check if the chat widget container exists before rendering
const container = document.getElementById('physical-ai-chat-widget');
if (container) {
  const root = ReactDOM.createRoot(container);
  root.render(
    <React.StrictMode>
      <ChatWidget />
    </React.StrictMode>
  );
}

// Also make the ChatWidget available globally for dynamic loading
window.PhysicalAIChatWidget = ChatWidget;