#!/usr/bin/env python3
"""Phase 1 Verification Script - Test text processing functionality"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.text_processing import clean_article, chunk_text
from backend.config import settings


def test_text_cleaning():
    """Test the clean_article function"""
    print("\n" + "="*60)
    print("TEST 1: Text Cleaning")
    print("="*60)
    
    test_cases = [
        {
            "name": "HTML and URLs",
            "input": "<p>Check https://example.com for details</p>",
            "expected_contains": ["Check", "details"]
        },
        {
            "name": "Extra whitespace",
            "input": "Multiple    spaces    and\n\nnewlines",
            "expected_contains": ["Multiple", "spaces", "and", "newlines"]
        },
        {
            "name": "Real article snippet",
            "input": "<p>The RBI announced new AI regulation!!! Multiple punctuation...</p>",
            "expected_contains": ["RBI", "announced", "AI", "regulation"]
        }
    ]
    
    for test in test_cases:
        try:
            result = clean_article(test["input"])
            passed = all(word in result for word in test["expected_contains"])
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"\n{status} - {test['name']}")
            print(f"  Input: {test['input'][:50]}...")
            print(f"  Output: {result[:70]}...")
        except Exception as e:
            print(f"\n✗ FAIL - {test['name']}: {str(e)}")


def test_text_chunking():
    """Test the chunk_text function"""
    print("\n" + "="*60)
    print("TEST 2: Text Chunking")
    print("="*60)
    
    long_text = " ".join([f"word{i}" for i in range(100)])
    
    test_cases = [
        {
            "name": "Basic chunking",
            "text": long_text,
            "chunk_size": 20,
            "overlap": 5,
            "min_chunks": 4
        },
        {
            "name": "Small text (no chunking needed)",
            "text": "Short text with few words",
            "chunk_size": 50,
            "overlap": 5,
            "min_chunks": 1
        },
        {
            "name": "Large chunk size",
            "text": long_text,
            "chunk_size": 200,
            "overlap": 0,
            "min_chunks": 1
        }
    ]
    
    for test in test_cases:
        try:
            chunks = chunk_text(test["text"], test["chunk_size"], test["overlap"])
            passed = len(chunks) >= test["min_chunks"]
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"\n{status} - {test['name']}")
            print(f"  Chunks generated: {len(chunks)} (expected >= {test['min_chunks']})")
            print(f"  Chunk 1 length: {len(chunks[0].split())} words")
        except Exception as e:
            print(f"\n✗ FAIL - {test['name']}: {str(e)}")


def test_sample_data():
    """Test that sample articles are valid JSON"""
    print("\n" + "="*60)
    print("TEST 3: Sample Data Validation")
    print("="*60)
    
    articles_path = Path(__file__).parent.parent / "backend" / "data" / "articles.json"
    
    try:
        with open(articles_path, 'r') as f:
            articles = json.load(f)
        
        required_fields = ["id", "title", "content", "source", "date"]
        
        total_articles = len(articles)
        valid_articles = 0
        
        for article in articles:
            has_required = all(field in article for field in required_fields)
            if has_required and len(article["content"]) > 50:
                valid_articles += 1
        
        passed = valid_articles == total_articles
        status = "✓ PASS" if passed else "✗ FAIL"
        
        print(f"\n{status} - Articles JSON")
        print(f"  Total articles: {total_articles}")
        print(f"  Valid articles: {valid_articles}")
        print(f"  Sample article: {articles[0]['title'][:50]}...")
        
    except FileNotFoundError:
        print("\n✗ FAIL - Articles JSON not found")
    except json.JSONDecodeError:
        print("\n✗ FAIL - Articles JSON is invalid")
    except Exception as e:
        print(f"\n✗ FAIL - {str(e)}")


def test_config_loading():
    """Test that configuration loads properly"""
    print("\n" + "="*60)
    print("TEST 4: Configuration Loading")
    print("="*60)
    
    try:
        print(f"\n✓ PASS - Configuration loaded")
        print(f"  API Host: {settings.api_host}")
        print(f"  API Port: {settings.api_port}")
        print(f"  Debug Mode: {settings.debug}")
        print(f"  Chunk Size: {settings.chunk_size}")
        print(f"  Chunk Overlap: {settings.chunk_overlap}")
        print(f"  GROQ API Key configured: {'Yes' if settings.groq_api_key else 'No (expected for Phase 1)'}")
    except Exception as e:
        print(f"\n✗ FAIL - Configuration error: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("  ET NEWS COPILOT - PHASE 1 VERIFICATION")
    print("█"*60)
    
    test_config_loading()
    test_text_cleaning()
    test_text_chunking()
    test_sample_data()
    
    print("\n" + "="*60)
    print("PHASE 1 VERIFICATION COMPLETE")
    print("="*60)
    print("\nNext Steps:")
    print("1. Start FastAPI server: python -m uvicorn backend.main:app --reload")
    print("2. Visit health endpoint: http://localhost:8000/health")
    print("3. Proceed to Phase 2: Vector DB and embeddings")
    print("\n")


if __name__ == "__main__":
    main()
