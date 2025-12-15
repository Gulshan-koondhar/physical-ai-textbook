import React, { useState, useEffect } from 'react';
import { ChatInterface } from './ChatInterface';
import { SourceCitation } from './SourceCitation';
import { textSelectionService } from '../services/textSelection';
import './ChatWidget.css';

export const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showSelectedTextPrompt, setShowSelectedTextPrompt] = useState(false);

  // Initialize text selection service
  useEffect(() => {
    // Set up callback for when text is selected
    textSelectionService.setOnTextSelected((text) => {
      if (text && text.length > 0) {
        setSelectedText(text);
        setShowSelectedTextPrompt(true);
      }
    });

    // Start listening for text selection
    textSelectionService.startListening();

    // Clean up on unmount
    return () => {
      textSelectionService.stopListening();
    };
  }, []);

  const handleAskAboutSelection = () => {
    if (selectedText) {
      // Show the chat interface with the selected text context
      setIsOpen(true);
      setShowSelectedTextPrompt(false);

      // Optionally pre-fill the input with a prompt related to the selected text
      // This would be handled in the ChatInterface component
    }
  };

  const handleAskGeneral = () => {
    setSelectedText('');
    setIsOpen(true);
    setShowSelectedTextPrompt(false);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <div className="chat-widget">
      {showSelectedTextPrompt && (
        <div className="selected-text-prompt">
          <p>You've selected text:</p>
          <div className="selected-text-preview">
            "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
          </div>
          <div className="selected-text-actions">
            <button onClick={handleAskAboutSelection} className="ask-selected-btn">
              Ask about selection
            </button>
            <button onClick={handleAskGeneral} className="ask-general-btn">
              Ask general question
            </button>
          </div>
        </div>
      )}

      {isOpen ? (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Textbook Assistant</h3>
            <button onClick={closeChat} className="close-btn">✕</button>
          </div>
          <ChatInterface
            selectedText={selectedText}
            onBackToSelectionPrompt={() => setShowSelectedTextPrompt(true)}
          />
        </div>
      ) : (
        <button onClick={toggleChat} className="chat-toggle-btn">
          💬 Ask Textbook
        </button>
      )}
    </div>
  );
};

export default ChatWidget;