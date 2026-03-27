"""
LLM service using Groq API.
Handles communication with language models for text generation.
"""

import json
from typing import Dict, Any, Optional
from groq import Groq
from backend.config import settings

class LLMService:
    """Service for LLM operations via Groq API."""
    
    def __init__(self):
        """Initialize Groq client."""
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = "mixtral-8x7b-32768"  # Fast, free tier model
            print(f"[v0] LLM service initialized with model: {self.model}")
        except Exception as e:
            print(f"[v0] Error initializing LLM: {e}")
            raise
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: User prompt
            temperature: Creativity level (0-1)
            max_tokens: Maximum response length
            system_prompt: Optional system message
            
        Returns:
            Generated text
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"[v0] Error generating text: {e}")
            raise
    
    def parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        
        Args:
            text: LLM response text
            
        Returns:
            Parsed JSON dict
        """
        try:
            # Try to extract JSON from response
            # Handle case where LLM wraps JSON in markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            print(f"[v0] Error parsing JSON response: {e}")
            # Return as string in a dict if parsing fails
            return {"response": text}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the LLM."""
        return {
            "model": self.model,
            "provider": "Groq",
            "description": "Fast, cost-effective inference"
        }


# Global instance
llm_service = None

def get_llm_service() -> LLMService:
    """Get or create LLM service (singleton)."""
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service
