import React from 'react';
import { SourceCitation } from './SourceCitation';
import './MessageDisplay.css';

export const MessageDisplay = ({ message }) => {
  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-content">
        {message.content}
      </div>

      {isAssistant && message.sources && message.sources.length > 0 && (
        <div className="message-sources">
          <h4>Sources:</h4>
          <div className="sources-list">
            {message.sources.map((source, index) => (
              <SourceCitation
                key={index}
                source={source}
                relevanceScore={source.relevance_score}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageDisplay;