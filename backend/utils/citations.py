"""
Citation utilities for Q&A responses.
Formats and manages source citations.
"""

from typing import List, Dict, Any
import re

def format_citation(source_id: str, title: str, excerpt: str, relevance: float = 1.0) -> Dict[str, Any]:
    """
    Format a single citation.
    
    Args:
        source_id: Article ID
        title: Article title
        excerpt: Quote from article
        relevance: Relevance score (0-1)
        
    Returns:
        Formatted citation dict
    """
    # Clean excerpt
    excerpt = excerpt.strip()
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."
    
    return {
        "source_id": source_id,
        "title": title,
        "excerpt": excerpt,
        "relevance_score": round(relevance, 2)
    }

def extract_quotes_from_text(text: str, num_quotes: int = 3) -> List[str]:
    """
    Extract relevant quotes from text.
    
    Args:
        text: Source text
        num_quotes: Number of quotes to extract
        
    Returns:
        List of quote strings
    """
    # Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter short sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Return first num_quotes
    return sentences[:num_quotes]

def format_answer_with_citations(
    answer: str,
    citations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Format QA response with citations.
    
    Args:
        answer: Generated answer text
        citations: List of citation dicts
        
    Returns:
        Formatted response with citations
    """
    return {
        "answer": answer.strip(),
        "citations": citations,
        "citation_count": len(citations)
    }

def add_inline_citations(text: str, citations: List[Dict[str, Any]]) -> str:
    """
    Add inline citations to answer text.
    
    Args:
        text: Answer text
        citations: List of citations
        
    Returns:
        Text with citation markers like [1], [2]
    """
    if not citations:
        return text
    
    # For now, just return original text
    # Could be extended to add [1], [2] markers
    return text

def merge_duplicate_citations(citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate citations from the same source.
    
    Args:
        citations: List of citations
        
    Returns:
        Deduplicated list
    """
    seen = {}
    for citation in citations:
        source_id = citation["source_id"]
        if source_id not in seen or citation.get("relevance_score", 0) > seen[source_id].get("relevance_score", 0):
            seen[source_id] = citation
    
    return list(seen.values())
