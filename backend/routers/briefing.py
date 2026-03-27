"""
Briefing router for generating smart article briefings.
"""

from fastapi import APIRouter, HTTPException
from backend.models import (
    BriefingRequest,
    BriefingResponse,
    Briefing
)
from backend.services.summarizer import get_summarizer_service
from backend.services.retrieval import get_retrieval_service

router = APIRouter(prefix="/api", tags=["briefing"])

@router.post("/briefing", response_model=BriefingResponse)
async def generate_briefing(request: BriefingRequest) -> BriefingResponse:
    """
    Generate a smart 4-question briefing from an article.
    
    This endpoint uses AI to analyze an article and provide:
    1. What happened
    2. Why it matters (for given persona)
    3. Who's involved
    4. What to watch for
    
    Args:
        request: BriefingRequest with article_text and persona
        
    Returns:
        BriefingResponse with generated briefing
    """
    try:
        if not request.article_text or len(request.article_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="article_text cannot be empty"
            )
        
        # Validate persona
        valid_personas = ["investor", "student", "founder", "journalist"]
        persona = request.persona.lower() if request.persona else "investor"
        if persona not in valid_personas:
            persona = "investor"
        
        # Generate briefing
        summarizer = get_summarizer_service()
        result = summarizer.generate_briefing(
            article_text=request.article_text,
            persona=persona
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Failed to generate briefing")
            )
        
        briefing_data = result.get("briefing", {})
        
        # Search for related articles
        retrieval_service = get_retrieval_service()
        search_result = retrieval_service.search_similar_articles(
            query_text=request.article_text,
            limit=5,
            min_similarity=0.3
        )
        
        related_articles = []
        if search_result.get("status") == "success":
            for article in search_result.get("articles", [])[:3]:
                related_articles.append({
                    "id": article["id"],
                    "title": article["title"],
                    "similarity_score": article["similarity_score"]
                })
        
        return BriefingResponse(
            status="success",
            briefing=Briefing(
                what_happened=briefing_data.get("what_happened", ""),
                why_it_matters=briefing_data.get("why_it_matters", ""),
                who_involved=briefing_data.get("who_involved", ""),
                what_next=briefing_data.get("what_next", "")
            ),
            persona=persona,
            related_articles=related_articles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[v0] Error in briefing endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Briefing generation error: {str(e)}"
        )
