"""
Retrieval service using ChromaDB vector database.
Manages article storage, indexing, and semantic search.
"""

import json
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from backend.services.embeddings import get_embeddings_service

class RetrievalService:
    """Service for managing vector database and semantic search."""
    
    def __init__(self, persist_directory: str = "./chroma_data"):
        """
        Initialize ChromaDB.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        
        try:
            # Create persistent client
            os.makedirs(persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=persist_directory)
            self.collection = self.client.get_or_create_collection(
                name="articles",
                metadata={"hnsw:space": "cosine"}
            )
            print(f"[v0] ChromaDB initialized with collection 'articles'")
        except Exception as e:
            print(f"[v0] Error initializing ChromaDB: {e}")
            raise
    
    def add_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add articles to the vector database.
        
        Args:
            articles: List of article dicts with id, content, title, etc.
            
        Returns:
            Status dict with count of added articles
        """
        if not articles:
            return {"status": "error", "message": "No articles provided"}
        
        try:
            ids = []
            documents = []
            metadatas = []
            
            for article in articles:
                article_id = article.get("id", f"article-{len(ids)}")
                content = article.get("content", "")
                
                if not content:
                    print(f"[v0] Skipping article {article_id}: no content")
                    continue
                
                ids.append(article_id)
                documents.append(content)
                
                # Store metadata (ChromaDB auto-embeds documents)
                metadata = {
                    "title": article.get("title", ""),
                    "source": article.get("source", ""),
                    "url": article.get("url", ""),
                    "date": article.get("date", ""),
                    "category": article.get("category", ""),
                }
                metadatas.append(metadata)
            
            # ChromaDB auto-generates embeddings
            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            print(f"[v0] Added {len(ids)} articles to ChromaDB")
            return {
                "status": "success",
                "articles_added": len(ids),
                "total_in_db": self.collection.count()
            }
        except Exception as e:
            print(f"[v0] Error adding articles: {e}")
            return {"status": "error", "message": str(e)}
    
    def search_similar_articles(
        self, 
        query_text: str, 
        limit: int = 5,
        min_similarity: float = 0.3
    ) -> Dict[str, Any]:
        """
        Search for articles similar to query text.
        
        Args:
            query_text: Text to search for similar articles
            limit: Number of results to return
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of similar articles with scores
        """
        if not query_text:
            return {
                "status": "error",
                "message": "Query text cannot be empty"
            }
        
        try:
            # ChromaDB returns distances (0-2 range for cosine), convert to similarity
            results = self.collection.query(
                query_texts=[query_text],
                n_results=limit + 5,  # Get extra to filter by similarity
                include=["documents", "metadatas", "distances"]
            )
            
            if not results or not results["ids"] or len(results["ids"]) == 0:
                return {
                    "status": "success",
                    "articles": [],
                    "query": query_text
                }
            
            # Process results
            articles = []
            for idx, (doc_id, distance, metadata, document) in enumerate(
                zip(
                    results["ids"][0],
                    results["distances"][0],
                    results["metadatas"][0],
                    results["documents"][0]
                )
            ):
                # Convert distance to similarity (cosine: 0-2 range)
                # 0 = identical, 2 = opposite
                similarity = 1 - (distance / 2)
                similarity = max(0.0, min(1.0, similarity))  # Clamp to 0-1
                
                if similarity < min_similarity:
                    continue
                
                articles.append({
                    "id": doc_id,
                    "title": metadata.get("title", ""),
                    "source": metadata.get("source", ""),
                    "url": metadata.get("url", ""),
                    "date": metadata.get("date", ""),
                    "category": metadata.get("category", ""),
                    "snippet": document[:200] + "..." if len(document) > 200 else document,
                    "similarity_score": round(similarity, 3)
                })
            
            return {
                "status": "success",
                "articles": articles[:limit],
                "query": query_text,
                "total_found": len(articles)
            }
        except Exception as e:
            print(f"[v0] Error searching articles: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_article_by_id(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        Get article by ID.
        
        Args:
            article_id: ID of article to retrieve
            
        Returns:
            Article dict or None
        """
        try:
            results = self.collection.get(
                ids=[article_id],
                include=["documents", "metadatas"]
            )
            
            if not results or not results["ids"]:
                return None
            
            return {
                "id": results["ids"][0],
                "content": results["documents"][0],
                "metadata": results["metadatas"][0]
            }
        except Exception as e:
            print(f"[v0] Error getting article: {e}")
            return None
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get stats about the vector database."""
        try:
            count = self.collection.count()
            return {
                "total_articles": count,
                "collection_name": "articles",
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            print(f"[v0] Error getting stats: {e}")
            return {"status": "error", "message": str(e)}
    
    def clear_database(self) -> Dict[str, Any]:
        """Clear all articles from database."""
        try:
            self.client.delete_collection(name="articles")
            self.collection = self.client.get_or_create_collection(name="articles")
            return {"status": "success", "message": "Database cleared"}
        except Exception as e:
            print(f"[v0] Error clearing database: {e}")
            return {"status": "error", "message": str(e)}


# Global instance
retrieval_service = None

def get_retrieval_service() -> RetrievalService:
    """Get or create retrieval service (singleton)."""
    global retrieval_service
    if retrieval_service is None:
        retrieval_service = RetrievalService()
    return retrieval_service
