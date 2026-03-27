"""
Q&A router for question answering with citations.
"""

from fastapi import APIRouter, HTTPException
from backend.models import (
    QARequest,
    QAResponse,
    Citation
)
from backend.services.qa import get_qa_service

router = APIRouter(prefix="/api", tags=["qa"])

@router.post("/ask-question", response_model=QAResponse)
async def ask_question(request: QARequest) -> QAResponse:
    """
    Answer a question about an article with citations.
    
    This endpoint uses retrieval-augmented generation to answer questions
    with citations from the article and related articles.
    
    Args:
        request: QARequest with question and article_text
        
    Returns:
        QAResponse with answer and citations
    """
    try:
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="question cannot be empty"
            )
        
        if not request.article_text or len(request.article_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="article_text cannot be empty"
            )
        
        qa_service = get_qa_service()
        
        result = qa_service.answer_question(
            question=request.question,
            article_text=request.article_text,
            use_related=request.use_related,
            max_sources=request.max_sources
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Failed to answer question")
            )
        
        # Convert citations to Citation models
        citations = [
            Citation(
                source_id=c["source_id"],
                title=c["title"],
                excerpt=c["excerpt"],
                relevance_score=c.get("relevance_score", 0)
            )
            for c in result.get("citations", [])
        ]
        
        return QAResponse(
            status="success",
            answer=result.get("answer", ""),
            citations=citations,
            question=request.question
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[v0] Error in QA endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Q&A error: {str(e)}"
        )
