/**
 * Text selection utility for capturing selected text from any page
 * Provides functionality to get selected text and set up event listeners
 */

class TextSelectionService {
  constructor() {
    this.selectedText = '';
    this.onTextSelectedCallback = null;
  }

  /**
   * Get the currently selected text on the page
   * @returns {string} The selected text, or empty string if no text is selected
   */
  getSelectedText = () => {
    const selection = window.getSelection();
    return selection ? selection.toString().trim() : '';
  };

  /**
   * Get detailed information about the current selection
   * @returns {Object} Object containing selected text, start/end positions, etc.
   */
  getSelectionInfo = () => {
    const selection = window.getSelection();
    if (!selection || selection.toString().trim() === '') {
      return null;
    }

    const range = selection.rangeCount > 0 ? selection.getRangeAt(0) : null;
    const selectedText = selection.toString().trim();

    return {
      text: selectedText,
      range: range,
      rect: range ? range.getBoundingClientRect() : null,
      anchorOffset: selection.anchorOffset,
      focusOffset: selection.focusOffset,
      anchorNode: selection.anchorNode,
      focusNode: selection.focusNode,
    };
  };

  /**
   * Set callback function to be called when text is selected
   * @param {Function} callback - Function to call when text is selected
   */
  setOnTextSelected = (callback) => {
    this.onTextSelectedCallback = callback;
  };

  /**
   * Handle the text selection event
   * @private
   */
  handleTextSelection = () => {
    const selectedText = this.getSelectedText();

    // Only trigger callback if there's actually selected text
    if (selectedText && selectedText.length > 0 && this.onTextSelectedCallback) {
      this.onTextSelectedCallback(selectedText);
    }
  };

  /**
   * Start listening for text selection events
   */
  startListening = () => {
    // Remove existing listeners to avoid duplicates
    this.stopListening();

    // Add event listeners for text selection
    document.addEventListener('mouseup', this.handleTextSelection);
    document.addEventListener('keyup', this.handleTextSelection);
  };

  /**
   * Stop listening for text selection events
   */
  stopListening = () => {
    document.removeEventListener('mouseup', this.handleTextSelection);
    document.removeEventListener('keyup', this.handleTextSelection);
  };

  /**
   * Clear the current selection
   */
  clearSelection = () => {
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    } else if (document.selection) {
      document.selection.empty();
    }
  };

  /**
   * Highlight text in a specific element (for demo purposes)
   * @param {HTMLElement} element - The element to highlight text in
   * @param {number} start - Start position of the text to highlight
   * @param {number} end - End position of the text to highlight
   */
  highlightText = (element, start, end) => {
    if (!element || start < 0 || end > element.textContent.length || start >= end) {
      return;
    }

    const range = document.createRange();
    const textNodes = this.getTextNodesIn(element);
    let currentPos = 0;
    let startNode = null;
    let endNode = null;
    let startOffset = 0;
    let endOffset = 0;

    for (const node of textNodes) {
      const nodeEndPos = currentPos + node.length;

      if (currentPos <= start && start < nodeEndPos) {
        startNode = node;
        startOffset = start - currentPos;
      }

      if (currentPos < end && end <= nodeEndPos) {
        endNode = node;
        endOffset = end - currentPos;
        break;
      }

      currentPos = nodeEndPos;
    }

    if (startNode && endNode) {
      range.setStart(startNode, startOffset);
      range.setEnd(endNode, endOffset);

      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }
  };

  /**
   * Helper function to get all text nodes within an element
   * @private
   */
  getTextNodesIn = (node) => {
    const textNodes = [];

    function getTextNodes(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        textNodes.push(node);
      } else {
        for (let childNode of node.childNodes) {
          getTextNodes(childNode);
        }
      }
    }

    getTextNodes(node);
    return textNodes;
  };
}

// Create a singleton instance
export const textSelectionService = new TextSelectionService();

// Export the class as default for flexibility
export default TextSelectionService;