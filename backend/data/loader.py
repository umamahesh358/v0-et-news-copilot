"""
Data loader for articles.
Loads sample articles from JSON file into vector database.
"""

import json
import os
from typing import List, Dict, Any

def load_articles_from_json(json_path: str) -> List[Dict[str, Any]]:
    """
    Load articles from JSON file.
    
    Args:
        json_path: Path to articles.json
        
    Returns:
        List of article dicts
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Articles file not found: {json_path}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both list and dict with 'articles' key
        articles = data if isinstance(data, list) else data.get('articles', [])
        
        print(f"[v0] Loaded {len(articles)} articles from {json_path}")
        return articles
    except json.JSONDecodeError as e:
        print(f"[v0] Error parsing JSON: {e}")
        raise
    except Exception as e:
        print(f"[v0] Error loading articles: {e}")
        raise

def initialize_database(retrieval_service, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Initialize database with articles.
    
    Args:
        retrieval_service: RetrievalService instance
        articles: List of articles to add
        
    Returns:
        Status dict
    """
    try:
        # Clear existing data
        retrieval_service.clear_database()
        
        # Add articles
        result = retrieval_service.add_articles(articles)
        return result
    except Exception as e:
        print(f"[v0] Error initializing database: {e}")
        return {"status": "error", "message": str(e)}
