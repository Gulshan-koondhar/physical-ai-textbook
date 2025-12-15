import google.generativeai as genai
import os
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """
    Service for interacting with Google Gemini API for responses
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response using Google Gemini
        """
        # Combine context and prompt if context is provided
        if context:
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        else:
            full_prompt = prompt

        try:
            response = await self.model.generate_content_async(full_prompt)
            return response.text if response.text else "I couldn't generate a response for your query."
        except Exception as e:
            print(f"Error generating response from Gemini: {e}")
            return "I'm having trouble generating a response right now. Please try again later."

    async def generate_response_with_sources(self, prompt: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a response with source citations
        """
        # Create context from sources
        context_parts = []
        source_info = []

        for source in sources:
            context_parts.append(f"Source: {source['file_path']}\nContent: {source['content_snippet']}")
            source_info.append({
                'file_path': source['file_path'],
                'content_snippet': source['content_snippet'],
                'relevance_score': source.get('relevance_score', 0.0)
            })

        context = "\n\n".join(context_parts)

        response_text = await self.generate_response(prompt, context)

        return {
            'content': response_text,
            'sources': source_info
        }

# Global instance
gemini_service = GeminiService()