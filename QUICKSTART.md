# ET News Copilot - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Start the Backend Server
```bash
python -m uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Test the API
In a new terminal:
```bash
# Health check
curl http://localhost:8000/health

# Clean some text
curl -X POST http://localhost:8000/clean-text \
  -H "Content-Type: application/json" \
  -d '{"text": "The <p>RBI announced AI regulation</p> Check https://example.com for details"}'

# Chunk text
curl -X POST http://localhost:8000/chunk-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Your very long article text here with many words that needs to be split into chunks for better semantic processing...", "chunk_size": 10}'
```

### 4. Run Verification Tests
```bash
python scripts/verify_phase1.py
```

---

## 📁 Project Structure

```
et-news-copilot/
├── backend/
│   ├── main.py              ← FastAPI app
│   ├── config.py            ← Settings
│   ├── models.py            ← Data schemas
│   ├── services/
│   │   └── text_processing.py  ← Clean & chunk
│   ├── routers/
│   │   └── health.py        ← Health endpoint
│   └── data/
│       └── articles.json    ← 15 sample articles
├── scripts/
│   └── verify_phase1.py     ← Tests
├── .env                     ← Environment vars
├── requirements.txt         ← Python packages
└── README.md
```

---

## 🧪 Testing Text Processing Directly

```python
from backend.services.text_processing import clean_article, chunk_text

# Clean text
text = "<p>RBI announced AI regulation</p> Visit https://example.com"
cleaned = clean_article(text)
print(cleaned)
# Output: "RBI announced AI regulation"

# Chunk text
long_text = "word " * 100  # 100 words
chunks = chunk_text(long_text, chunk_size=20, overlap=5)
print(f"Created {len(chunks)} chunks")
```

---

## 🔧 Configuration

Edit `.env` to customize:
```
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
CHUNK_SIZE=512
CHUNK_OVERLAP=50
GROQ_API_KEY=your_key_here  # Add in Phase 3
```

---

## ✅ Phase 1 Checklist

- [x] FastAPI backend created
- [x] Text cleaning function works
- [x] Text chunking function works
- [x] Sample data loaded (15 articles)
- [x] Health check endpoint works
- [x] Configuration system ready
- [x] Verification tests pass

---

## 🚀 Next Phase (Phase 2)

After Phase 1 verification passes:

1. Set up ChromaDB
2. Add Sentence Transformers
3. Load articles into vector DB
4. Implement article search

See `PHASE_1_README.md` for detailed next steps.

---

## 🆘 Troubleshooting

### Port already in use?
```bash
python -m uvicorn backend.main:app --port 8001
```

### Module not found?
```bash
# Make sure you're in project root
cd /path/to/et-news-copilot
pip install -r backend/requirements.txt
```

### .env not loading?
```bash
# Verify .env exists in root (not in backend/)
ls -la .env
```

---

## 📖 Documentation

- `PHASE_1_README.md` - Detailed Phase 1 documentation
- `QUICKSTART.md` - This file
- `scripts/verify_phase1.py` - Automated tests

---

**Ready? Run:** `python -m uvicorn backend.main:app --reload`
