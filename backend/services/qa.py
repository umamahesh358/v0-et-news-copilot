"""
Q&A service using retrieval-augmented generation.
Answers questions with citations from articles.
"""

from typing import Dict, Any, List
from backend.services.llm import get_llm_service
from backend.services.retrieval import get_retrieval_service
from backend.utils.citations import (
    format_citation,
    merge_duplicate_citations,
    extract_quotes_from_text
)

class QAService:
    """Service for answering questions with citations."""
    
    def __init__(self):
        """Initialize QA service."""
        self.llm_service = get_llm_service()
        self.retrieval_service = get_retrieval_service()
    
    def answer_question(
        self,
        question: str,
        article_text: str,
        use_related: bool = True,
        max_sources: int = 3
    ) -> Dict[str, Any]:
        """
        Answer a question with citations from articles.
        
        Args:
            question: User's question
            article_text: Main article text to reference
            use_related: Whether to search for related articles
            max_sources: Maximum number of sources to cite
            
        Returns:
            Dict with answer and citations
        """
        if not question or len(question.strip()) == 0:
            return {"status": "error", "message": "Question cannot be empty"}
        
        try:
            # Retrieve relevant articles
            search_results = self.retrieval_service.search_similar_articles(
                query_text=question,
                limit=3 if use_related else 1,
                min_similarity=0.2
            )
            
            related_articles = search_results.get("articles", [])
            
            # Prepare context from articles
            context_parts = [f"MAIN ARTICLE:\n{article_text}"]
            
            article_lookup = {}
            for i, article in enumerate(related_articles[:max_sources]):
                context_parts.append(f"\nRELATED ARTICLE {i+1} (similarity: {article.get('similarity_score', 0)}):\n{article.get('snippet', '')}")
                article_lookup[article["id"]] = article
            
            context = "\n".join(context_parts)
            
            # Generate answer
            prompt = f"""
You are a research assistant. Answer the user's question based ONLY on the provided articles.

QUESTION: {question}

ARTICLES:
{context}

Rules:
1. Answer the question clearly and concisely (2-3 sentences)
2. Use information ONLY from the provided articles
3. If the answer isn't found in articles, say "Not covered in the provided articles"
4. Be specific and cite relevant facts

ANSWER:
"""
            
            answer = self.llm_service.generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract citations from retrieved articles
            citations = []
            for article in related_articles[:max_sources]:
                quotes = extract_quotes_from_text(article.get("snippet", ""), num_quotes=1)
                if quotes:
                    citation = format_citation(
                        source_id=article["id"],
                        title=article["title"],
                        excerpt=quotes[0],
                        relevance=article.get("similarity_score", 0)
                    )
                    citations.append(citation)
            
            # Merge duplicate citations
            citations = merge_duplicate_citations(citations)
            
            return {
                "status": "success",
                "answer": answer.strip(),
                "citations": citations[:max_sources],
                "question": question
            }
        except Exception as e:
            print(f"[v0] Error answering question: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_related_articles(
        self,
        question: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get articles related to a question.
        
        Args:
            question: Search query
            limit: Max results
            
        Returns:
            Search results with articles
        """
        try:
            results = self.retrieval_service.search_similar_articles(
                query_text=question,
                limit=limit,
                min_similarity=0.2
            )
            return results
        except Exception as e:
            print(f"[v0] Error getting related articles: {e}")
            return {"status": "error", "message": str(e)}


# Global instance
qa_service = None

def get_qa_service() -> QAService:
    """Get or create QA service (singleton)."""
    global qa_service
    if qa_service is None:
        qa_service = QAService()
    return qa_service
