"""
Embeddings service using Sentence Transformers.
Generates and manages text embeddings for semantic search.
"""

from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

# Using lightweight model: 22M params, 384D vectors, very fast
MODEL_NAME = "all-MiniLM-L6-v2"

class EmbeddingsService:
    """Service for generating and managing text embeddings."""
    
    def __init__(self):
        """Initialize Sentence Transformers model."""
        try:
            self.model = SentenceTransformer(MODEL_NAME)
            self.embedding_dim = 384
            print(f"[v0] Embeddings model loaded: {MODEL_NAME}")
        except Exception as e:
            print(f"[v0] Error loading embeddings model: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            # Convert numpy array to list
            return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        except Exception as e:
            print(f"[v0] Error embedding text: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            # Convert to list of lists
            return [emb.tolist() if hasattr(emb, 'tolist') else list(emb) for emb in embeddings]
        except Exception as e:
            print(f"[v0] Error embedding texts: {e}")
            raise
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Cosine similarity
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            # Ensure value is between 0 and 1
            return float(max(0.0, min(1.0, (similarity + 1) / 2)))
        except Exception as e:
            print(f"[v0] Error computing similarity: {e}")
            return 0.0
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embeddings model."""
        return {
            "model_name": MODEL_NAME,
            "embedding_dimension": self.embedding_dim,
            "architecture": "Sentence Transformers",
            "description": "Lightweight, fast model for semantic similarity"
        }


# Global instance
embeddings_service = None

def get_embeddings_service() -> EmbeddingsService:
    """Get or create embeddings service (singleton)."""
    global embeddings_service
    if embeddings_service is None:
        embeddings_service = EmbeddingsService()
    return embeddings_service
