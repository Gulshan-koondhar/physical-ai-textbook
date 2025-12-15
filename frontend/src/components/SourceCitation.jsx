import React from 'react';
import './SourceCitation.css';

export const SourceCitation = ({ source, relevanceScore }) => {
  // Extract the file name from the path for display
  const getFileName = (filePath) => {
    if (!filePath) return 'Unknown source';
    const parts = filePath.split('/');
    return parts[parts.length - 1] || filePath;
  };

  return (
    <div className="source-citation">
      <div className="source-info">
        <span className="source-path" title={source.file_path}>
          {getFileName(source.file_path)}
        </span>
        {relevanceScore !== undefined && (
          <span className="relevance-score" title={`Relevance: ${relevanceScore}`}>
            ({Math.round(relevanceScore * 100)}%)
          </span>
        )}
      </div>
      <div className="source-preview">
        "{source.content_snippet.substring(0, 100)}{source.content_snippet.length > 100 ? '...' : ''}"
      </div>
    </div>
  );
};

export default SourceCitation;