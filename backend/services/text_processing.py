"""Text processing utilities for article cleaning and chunking"""

import re
from typing import List
from backend.config import settings


def clean_article(text: str) -> str:
    """
    Clean article text by removing HTML, URLs, and normalizing whitespace.
    
    Args:
        text: Raw article text
        
    Returns:
        Cleaned text ready for processing
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    
    # Remove HTML tags (basic)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters (but keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?;\'"():\-]', '', text)
    
    # Remove multiple punctuation
    text = re.sub(r'[.!?;]{2,}', '.', text)
    
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = None,
    overlap: int = None
) -> List[str]:
    """
    Split text into overlapping chunks for better semantic retrieval.
    
    Args:
        text: Text to chunk
        chunk_size: Words per chunk (default from config)
        overlap: Words to overlap between chunks (default from config)
        
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if overlap is None:
        overlap = settings.chunk_overlap
    
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")
    
    # Split by words
    words = text.split()
    
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        if chunk_words:  # Only add non-empty chunks
            chunks.append(' '.join(chunk_words))
    
    return chunks


def preprocess_article(text: str) -> tuple[str, List[str]]:
    """
    Complete preprocessing: clean and chunk text.
    
    Args:
        text: Raw article text
        
    Returns:
        Tuple of (cleaned_text, chunks)
    """
    cleaned = clean_article(text)
    chunks = chunk_text(cleaned)
    return cleaned, chunks


def extract_summary(text: str, word_limit: int = 100) -> str:
    """
    Extract first N words as a summary snippet.
    
    Args:
        text: Text to summarize
        word_limit: Maximum words in summary
        
    Returns:
        Summary text
    """
    words = text.split()
    summary = ' '.join(words[:word_limit])
    
    # Add ellipsis if truncated
    if len(words) > word_limit:
        summary += "..."
    
    return summary


# Test functions (can be removed later)
if __name__ == "__main__":
    test_text = """
    <p>The Reserve Bank of India announced new AI regulation guidelines today.</p>
    <p>Check out more at https://example.com for details.</p>
    This is the main content!!!  Multiple spaces   here.
    """
    
    print("Original:", test_text)
    cleaned = clean_article(test_text)
    print("Cleaned:", cleaned)
    
    chunks = chunk_text(cleaned, chunk_size=20, overlap=5)
    print(f"Chunks ({len(chunks)}):", chunks)
