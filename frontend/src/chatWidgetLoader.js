import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatWidget from './components/ChatWidget.jsx';

// Create a global function to initialize the chat widget
window.initPhysicalAIChatWidget = () => {
  // Create the container element for the chat widget
  let container = document.getElementById('physical-ai-chat-widget');

  if (!container) {
    container = document.createElement('div');
    container.id = 'physical-ai-chat-widget';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.right = '20px';
    container.style.zIndex = '10000';
    container.style.fontFamily = 'Arial, sans-serif';
    document.body.appendChild(container);
  }

  // Render the chat widget
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <ChatWidget />
    </React.StrictMode>
  );
};

// Auto-initialize if the container element exists
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('physical-ai-chat-widget')) {
    window.initPhysicalAIChatWidget();
  }
});

// Also make the ChatWidget available globally for dynamic loading
window.PhysicalAIChatWidget = ChatWidget;