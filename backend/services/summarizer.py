"""
Summarizer service for generating smart briefings.
Creates 4-question briefings personalized by persona.
"""

import json
from typing import Dict, Any, Optional
from backend.services.llm import get_llm_service

PERSONA_CONTEXT = {
    "investor": "an investor or venture capitalist",
    "student": "a student or academic researcher",
    "founder": "a startup founder or entrepreneur",
    "journalist": "a journalist or content creator"
}

class SummarizerService:
    """Service for generating article summaries and briefings."""
    
    def __init__(self):
        """Initialize summarizer."""
        self.llm_service = get_llm_service()
    
    def generate_briefing(
        self,
        article_text: str,
        persona: str = "investor"
    ) -> Dict[str, Any]:
        """
        Generate a 4-question briefing from article.
        
        Args:
            article_text: Full article text
            persona: Target persona (investor, student, founder, journalist)
            
        Returns:
            Dict with what_happened, why_it_matters, who_involved, what_next
        """
        if not article_text or len(article_text.strip()) == 0:
            return {"status": "error", "message": "Article text cannot be empty"}
        
        # Validate persona
        if persona not in PERSONA_CONTEXT:
            persona = "investor"
        
        persona_desc = PERSONA_CONTEXT[persona]
        
        # Truncate article if too long
        max_chars = 3000
        if len(article_text) > max_chars:
            article_text = article_text[:max_chars] + "..."
        
        prompt = f"""
You are an expert analyst. Analyze the following article and provide a clear, concise briefing.

TARGET AUDIENCE: {persona_desc}

ARTICLE:
{article_text}

Answer these 4 questions. Keep each answer to 2-3 sentences max:

1. WHAT HAPPENED? (Describe the event/news in simple terms)
2. WHY DOES IT MATTER FOR A {persona.upper()}? (Explain specific impact and business/personal relevance)
3. WHO ARE THE KEY PLAYERS? (List 3-5 people, companies, or institutions mentioned)
4. WHAT SHOULD WE WATCH FOR? (What developments or impacts should we expect next?)

Format your response EXACTLY as this JSON (no markdown, no code blocks):
{{
    "what_happened": "...",
    "why_it_matters": "...",
    "who_involved": "...",
    "what_next": "..."
}}
"""
        
        try:
            response = self.llm_service.generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=800
            )
            
            briefing = self.llm_service.parse_json_response(response)
            
            # Ensure all keys are present
            required_keys = ["what_happened", "why_it_matters", "who_involved", "what_next"]
            for key in required_keys:
                if key not in briefing:
                    briefing[key] = ""
            
            return {
                "status": "success",
                "briefing": briefing,
                "persona": persona
            }
        except Exception as e:
            print(f"[v0] Error generating briefing: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def generate_title_summary(self, article_text: str, max_length: int = 150) -> str:
        """
        Generate a short summary/title for article.
        
        Args:
            article_text: Article text
            max_length: Maximum length of summary
            
        Returns:
            Short summary text
        """
        if len(article_text) > 2000:
            article_text = article_text[:2000]
        
        prompt = f"""
Generate a short, compelling {max_length}-character summary of this article. Be specific and impactful.

ARTICLE:
{article_text}

Summary (max {max_length} chars):
"""
        
        try:
            response = self.llm_service.generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=100
            )
            return response.strip()
        except Exception as e:
            print(f"[v0] Error generating summary: {e}")
            return "Article summary unavailable"


# Global instance
summarizer_service = None

def get_summarizer_service() -> SummarizerService:
    """Get or create summarizer service (singleton)."""
    global summarizer_service
    if summarizer_service is None:
        summarizer_service = SummarizerService()
    return summarizer_service
