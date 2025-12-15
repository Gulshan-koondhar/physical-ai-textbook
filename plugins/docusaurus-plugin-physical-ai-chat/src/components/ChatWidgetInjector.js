import React, { useEffect } from 'react';

// This component will be injected into all pages to load the chat widget
const ChatWidgetInjector = () => {
  useEffect(() => {
    // Create the chat widget container div if it doesn't exist
    let widgetContainer = document.getElementById('physical-ai-chat-widget');
    if (!widgetContainer) {
      widgetContainer = document.createElement('div');
      widgetContainer.id = 'physical-ai-chat-widget';
      widgetContainer.style.position = 'fixed';
      widgetContainer.style.bottom = '20px';
      widgetContainer.style.right = '20px';
      widgetContainer.style.zIndex = '10000';
      widgetContainer.style.fontFamily = 'Arial, sans-serif';
      document.body.appendChild(widgetContainer);
    }

    // Function to initialize the widget once dependencies are loaded
    const initializeWidget = () => {
      if (window.initPhysicalAIChatWidget) {
        console.log('Initializing chat widget via initPhysicalAIChatWidget');
        try {
          window.initPhysicalAIChatWidget();
        } catch (error) {
          console.error('Error initializing chat widget:', error);
        }
      } else {
        console.warn('initPhysicalAIChatWidget function not available');
      }
    };

    // Check if React and ReactDOM are available before loading the widget
    const checkDependenciesAndLoad = () => {
      if (window.React && window.ReactDOM) {
        console.log('React and ReactDOM are available, loading chat widget');
        loadChatWidget();
      } else {
        console.warn('React and/or ReactDOM not available yet, waiting...');
        // Wait a bit more and try again
        setTimeout(() => {
          if (window.React && window.ReactDOM) {
            loadChatWidget();
          } else {
            console.error('React and ReactDOM are still not available after waiting');
          }
        }, 1000);
      }
    };

    // Function to load the chat widget script
    const loadChatWidget = () => {
      // Check if the chat widget script has already been loaded
      const existingScript = document.querySelector('script[src="/chat-widget.js"]');
      if (!existingScript) {
        // Load the chat widget script
        const script = document.createElement('script');
        script.src = '/chat-widget.js';
        script.async = false; // Ensure it loads in order
        script.onload = () => {
          console.log('Chat widget script loaded');
          // Initialize the widget after script is loaded
          setTimeout(initializeWidget, 100);
        };
        script.onerror = () => {
          console.error('Failed to load chat widget script');
        };

        // Add script to head and let it execute
        document.head.appendChild(script);
      } else {
        // If script already exists, try to initialize the widget
        setTimeout(initializeWidget, 100);
      }
    };

    // Start the process
    checkDependenciesAndLoad();

    // Also add a fallback in case React/ReactDOM load after the initial check
    const checkInterval = setInterval(() => {
      if (window.React && window.ReactDOM && !document.querySelector('script[src="/chat-widget.js"]')) {
        console.log('React and ReactDOM became available, loading chat widget');
        clearInterval(checkInterval);
        loadChatWidget();
      }
    }, 500);

    // Cleanup function
    return () => {
      clearInterval(checkInterval);
      const widgetContainer = document.getElementById('physical-ai-chat-widget');
      if (widgetContainer && widgetContainer.parentNode) {
        widgetContainer.parentNode.removeChild(widgetContainer);
      }
    };
  }, []);

  return null;
};

export default ChatWidgetInjector;