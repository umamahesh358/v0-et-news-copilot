"""
Search router for semantic article search.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from backend.models import (
    SearchRequest,
    SearchResponse,
    Article
)
from backend.services.retrieval import get_retrieval_service

router = APIRouter(prefix="/api", tags=["search"])

@router.post("/search-related", response_model=SearchResponse)
async def search_related_articles(request: SearchRequest) -> SearchResponse:
    """
    Search for articles related to the given text.
    
    This endpoint performs semantic search using vector embeddings.
    It finds articles similar to the provided query text.
    
    Args:
        request: SearchRequest with article_text and optional limit
        
    Returns:
        SearchResponse with list of similar articles
    """
    try:
        if not request.article_text or len(request.article_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="article_text cannot be empty"
            )
        
        retrieval_service = get_retrieval_service()
        
        # Search for similar articles
        result = retrieval_service.search_similar_articles(
            query_text=request.article_text,
            limit=request.limit,
            min_similarity=0.3
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Search failed")
            )
        
        # Convert to Article models
        articles = [
            Article(
                id=a["id"],
                title=a["title"],
                source=a["source"],
                url=a["url"],
                date=a["date"],
                category=a["category"],
                snippet=a["snippet"],
                similarity_score=a["similarity_score"]
            )
            for a in result.get("articles", [])
        ]
        
        return SearchResponse(
            status="success",
            related_articles=articles,
            query=request.article_text,
            total_found=result.get("total_found", 0)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[v0] Error in search endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}"
        )


@router.get("/db-stats")
async def get_database_stats():
    """
    Get statistics about the vector database.
    
    Returns:
        Database stats including total articles count
    """
    try:
        retrieval_service = get_retrieval_service()
        stats = retrieval_service.get_database_stats()
        return stats
    except Exception as e:
        print(f"[v0] Error getting stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
