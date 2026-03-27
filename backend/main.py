"""ET News Copilot - FastAPI Backend Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routers import health, search, briefing, qa
from backend.models import TextCleanRequest, TextCleanResponse
from backend.services.text_processing import clean_article, chunk_text
from backend.services.retrieval import get_retrieval_service
from backend.data.loader import load_articles_from_json, initialize_database
import os

# Initialize FastAPI app
app = FastAPI(
    title="ET News Copilot API",
    description="AI-powered news analysis and Q&A system",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(search.router)
app.include_router(briefing.router)
app.include_router(qa.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "ET News Copilot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "clean_text": "/clean-text",
            "chunk_text": "/chunk-text"
        }
    }


@app.post("/clean-text", response_model=TextCleanResponse)
async def clean_text_endpoint(request: TextCleanRequest):
    """Clean and normalize article text"""
    try:
        cleaned = clean_article(request.text)
        return TextCleanResponse(
            original_length=len(request.text),
            cleaned_length=len(cleaned),
            cleaned_text=cleaned
        )
    except ValueError as e:
        return {"error": str(e)}, 400


@app.post("/chunk-text")
async def chunk_text_endpoint(request: dict):
    """
    Chunk text into semantic pieces
    
    Request body:
    {
        "text": "article text",
        "chunk_size": 512,
        "overlap": 50
    }
    """
    try:
        text = request.get("text")
        chunk_size = request.get("chunk_size", settings.chunk_size)
        overlap = request.get("overlap", settings.chunk_overlap)
        
        if not text:
            return {"error": "text field is required"}, 400
        
        chunks = chunk_text(text, chunk_size, overlap)
        
        return {
            "success": True,
            "total_chunks": len(chunks),
            "chunk_size": chunk_size,
            "overlap": overlap,
            "chunks": chunks
        }
    except ValueError as e:
        return {"error": str(e)}, 400


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("[Startup] ET News Copilot API starting...")
    print(f"[Startup] Debug mode: {settings.debug}")
    print(f"[Startup] GROQ API Key configured: {'✓' if settings.GROQ_API_KEY else '✗'}")
    
    # Initialize vector database
    try:
        print("[Startup] Initializing vector database...")
        retrieval_service = get_retrieval_service()
        
        # Load articles
        articles_path = os.path.join(os.path.dirname(__file__), "data", "articles.json")
        if os.path.exists(articles_path):
            articles = load_articles_from_json(articles_path)
            result = initialize_database(retrieval_service, articles)
            print(f"[Startup] Database initialized: {result}")
        else:
            print(f"[Startup] Articles file not found at {articles_path}")
    except Exception as e:
        print(f"[Startup] Error initializing database: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("[Shutdown] ET News Copilot API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
