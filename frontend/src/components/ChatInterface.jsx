import React, { useState, useEffect, useRef } from 'react';
import { MessageDisplay } from './MessageDisplay';
import { SourceCitation } from './SourceCitation';
import { apiService } from '../services/apiClient';
import './ChatInterface.css';

export const ChatInterface = ({ selectedText, onBackToSelectionPrompt }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize session
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const response = await apiService.createSession();
        setSessionId(response.data.session_id);
      } catch (error) {
        console.error('Error creating session:', error);
      }
    };

    initializeSession();
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || !sessionId || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Determine query type based on whether we have selected text context
      const queryType = selectedText ? 'selected_text' : 'general';

      const response = await apiService.sendMessage({
        session_id: sessionId,
        message: inputValue,
        query_type: queryType,
        selected_text: selectedText || undefined,
      });

      // Add assistant response to the chat
      const assistantMessage = {
        id: `resp_${Date.now()}`,
        role: 'assistant',
        content: response.data.message,
        sources: response.data.sources || [],
        timestamp: response.data.timestamp,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        sources: [],
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToSelection = () => {
    if (onBackToSelectionPrompt) {
      onBackToSelectionPrompt();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {selectedText && (
          <div className="context-indicator">
            <span className="context-label">Context:</span>
            <div className="context-preview">
              "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
            </div>
            {onBackToSelectionPrompt && (
              <button onClick={handleBackToSelection} className="change-context-btn">
                Change context
              </button>
            )}
          </div>
        )}

        {messages.map((message) => (
          <MessageDisplay key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="loading-message">
            <div className="typing-indicator">
              <div></div>
              <div></div>
              <div></div>
            </div>
            <span className="loading-text">Thinking...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText ? "Ask about the selected text..." : "Ask about the textbook..."}
          className="chat-input"
          disabled={isLoading}
        />
        <button type="submit" disabled={!inputValue.trim() || isLoading} className="send-btn">
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;