"""Pydantic models for request/response schemas"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class BriefingRequest(BaseModel):
    """Request to generate a briefing for an article"""
    article_text: str = Field(..., min_length=100, description="Full article content")
    article_url: Optional[str] = None
    persona: str = Field(default="investor", description="Target persona: investor, student, or founder")


class BriefingResponse(BaseModel):
    """Response containing AI-generated briefing"""
    what_happened: str
    why_it_matters: str
    who_involved: str
    what_next: str


class RelatedArticle(BaseModel):
    """A single related article"""
    id: str
    title: str
    snippet: Optional[str] = None
    similarity_score: float = Field(ge=0, le=1)
    source: Optional[str] = None
    date: Optional[str] = None


class SearchRelatedRequest(BaseModel):
    """Request to search for related articles"""
    article_text: str = Field(..., min_length=100)
    limit: int = Field(default=5, ge=1, le=20)


class SearchRelatedResponse(BaseModel):
    """Response with related articles"""
    related_articles: List[RelatedArticle]
    query_summary: Optional[str] = None


class QuestionRequest(BaseModel):
    """Request to ask a question about article"""
    question: str = Field(..., min_length=5)
    article_text: str = Field(..., min_length=100)
    use_related: bool = False
    persona: Optional[str] = "general"


class Citation(BaseModel):
    """A citation/source for an answer"""
    source: str
    title: Optional[str]
    excerpt: Optional[str]
    relevance_score: Optional[float] = None


class AnswerResponse(BaseModel):
    """Response containing Q&A answer with citations"""
    answer: str
    citations: List[Citation] = []
    confidence_score: Optional[float] = None


class TextCleanRequest(BaseModel):
    """Request to clean text"""
    text: str = Field(..., min_length=10)


class TextCleanResponse(BaseModel):
    """Response with cleaned text"""
    original_length: int
    cleaned_length: int
    cleaned_text: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime
    services: Dict[str, str] = {}
