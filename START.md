# Getting Started with ET News Copilot

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
pip install -r frontend/requirements.txt
```

### 2. Set Up Environment

```bash
# Add your Groq API key to .env
# Get free key at https://console.groq.com

echo "GROQ_API_KEY=your_key_here" >> .env
```

### 3. Start Backend

```bash
# Terminal 1: Backend API
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✓ Embeddings model loaded: all-MiniLM-L6-v2
✓ ChromaDB initialized with collection 'articles'
✓ Added 15 articles to ChromaDB
```

### 4. Start Frontend

```bash
# Terminal 2: Streamlit Frontend
streamlit run frontend/streamlit_app.py
```

You should see:
```
✓ API connected
✓ Streamlit running on http://localhost:8501
```

### 5. Open in Browser

Visit: http://localhost:8501

## What to Try

1. **Paste an Article**
   - Copy any news article
   - Paste in sidebar
   - Select persona (investor/student/founder)

2. **Generate Briefing**
   - Click "Generate Briefing"
   - Get 4-question analysis in 5 seconds
   - See personalized insights

3. **Find Related Articles**
   - Click "Related Articles" tab
   - See 5 similar articles ranked by relevance
   - Understand semantic search in action

4. **Ask Questions**
   - Click "Q&A" tab
   - Ask any question about the article
   - Get answer with citations and sources

5. **Check Statistics**
   - Total articles in database
   - API health status
   - System info

## Test the API Directly

```bash
# In another terminal, run tests
python scripts/test_all_endpoints.py
```

This runs:
- ✓ Health checks
- ✓ Database stats
- ✓ Vector search
- ✓ Briefing generation
- ✓ Q&A system

Expected output: 11/11 tests passed

## Troubleshooting

### "API server is not running"
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, restart it
python -m uvicorn backend.main:app --reload
```

### "GROQ_API_KEY not found"
```bash
# Check .env file
cat .env

# Should see: GROQ_API_KEY=xxx

# If not, add it
echo "GROQ_API_KEY=your_key_here" > .env
```

### "ChromaDB error"
```bash
# Clear old database
rm -rf chroma_data/

# Restart backend (it will reinitialize)
python -m uvicorn backend.main:app --reload
```

### "Embeddings model too slow"
- Model downloads on first run (~100MB)
- Subsequent runs are instant
- Be patient on first startup

### "LLM response slow"
- Using Groq free tier (500 req/min shared)
- If hitting limit, wait a few seconds
- Get paid key for production

## Project Structure

```
et-news-copilot/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Settings
│   ├── models.py                  # Data schemas
│   ├── services/
│   │   ├── embeddings.py          # Sentence Transformers
│   │   ├── retrieval.py           # ChromaDB
│   │   ├── llm.py                 # Groq API
│   │   ├── summarizer.py          # Briefing generation
│   │   └── qa.py                  # Q&A system
│   ├── routers/
│   │   ├── health.py              # Health checks
│   │   ├── search.py              # /search-related
│   │   ├── briefing.py            # /briefing
│   │   └── qa.py                  # /ask-question
│   ├── data/
│   │   ├── articles.json          # Sample articles
│   │   └── loader.py              # Data loading
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py           # UI
│   └── requirements.txt
├── scripts/
│   ├── test_all_endpoints.py      # Tests
│   └── verify_phase1.py           # Phase 1 tests
├── .env                           # Secrets
└── docs/                          # Documentation
```

## API Endpoints

### Health
- `GET /health` - Server status

### Search
- `POST /api/search-related` - Find similar articles
- `GET /api/db-stats` - Database statistics

### Briefing
- `POST /api/briefing` - Generate smart briefing

### Q&A
- `POST /api/ask-question` - Answer with citations

See `PHASE_1_SUMMARY.md` for detailed endpoint docs.

## Next Steps

1. **Add More Articles**
   - Update `backend/data/articles.json`
   - Restart backend
   - Articles auto-loaded

2. **Deploy to Production**
   - Push to GitHub
   - Deploy backend to Railway/Vercel
   - Deploy frontend to Streamlit Cloud

3. **Add Premium Features**
   - User authentication
   - Save favorite articles
   - Custom briefing templates
   - API access for partners

4. **Scale to Real Data**
   - Connect to NewsAPI
   - Ingest real-time articles
   - Add RSS feed support

## Documentation Files

- `QUICKSTART.md` - 5-minute setup
- `PHASE_1_README.md` - Phase 1 details
- `PHASE_1_SUMMARY.md` - Implementation guide
- `DEMO_SCRIPT.md` - 5-minute demo outline
- `TESTING_CHECKLIST.md` - Verification steps

## Support

- Get Groq API key: https://console.groq.com
- FastAPI docs: http://localhost:8000/docs
- Streamlit docs: https://docs.streamlit.io
- ChromaDB docs: https://docs.trychroma.com

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│   FastAPI Backend   │
├─────────────────────┤
│ Text Processing     │
│ Embeddings (ST)     │
│ LLM (Groq)          │
│ Vector DB (ChromaDB)│
└─────────────────────┘
```

## Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] `.env` file with `GROQ_API_KEY`
- [ ] Backend running (`http://localhost:8000`)
- [ ] Frontend running (`http://localhost:8501`)
- [ ] Test article pasted
- [ ] Briefing generated
- [ ] Related articles found
- [ ] Q&A working
- [ ] All tests passing

**Everything is working! Ready to ship.** 🚀
