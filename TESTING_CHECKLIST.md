# Testing & Verification Checklist

## Phase 1: Backend Setup
- [ ] FastAPI app starts without errors
- [ ] `/health` endpoint returns 200 with status
- [ ] CORS headers present in responses
- [ ] Text cleaning function works
- [ ] Text chunking function works

## Phase 2: Vector Database
- [ ] ChromaDB initializes on startup
- [ ] 15 articles loaded into database
- [ ] `/db-stats` shows correct article count
- [ ] Embeddings model loads (all-MiniLM-L6-v2)
- [ ] `/search-related` endpoint works

### Search Tests
```bash
curl -X POST http://localhost:8000/api/search-related \
  -H "Content-Type: application/json" \
  -d '{"article_text": "AI regulation in fintech", "limit": 5}'
```
- [ ] Returns 5 similar articles
- [ ] Similarity scores between 0-1
- [ ] Articles sorted by relevance
- [ ] Response time < 2 seconds

## Phase 3: LLM Integration
- [ ] Groq API key loaded from .env
- [ ] LLM service initializes
- [ ] `/briefing` endpoint works

### Briefing Tests
```bash
curl -X POST http://localhost:8000/api/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "article_text": "RBI announces AI regulation...",
    "persona": "investor"
  }'
```
- [ ] Returns 4-part briefing (what/why/who/next)
- [ ] Text is personalized for investor/student/founder
- [ ] Response includes related articles
- [ ] Response time < 10 seconds
- [ ] No hallucinations/made-up facts

### Persona Tests
- [ ] "investor" persona generates business-focused briefing
- [ ] "student" persona generates academic perspective
- [ ] "founder" persona generates entrepreneurial angle
- [ ] "journalist" persona generates narrative angle

## Phase 4: Q&A System
- [ ] `/ask-question` endpoint works

### Q&A Tests
```bash
curl -X POST http://localhost:8000/api/ask-question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How will this affect startups?",
    "article_text": "RBI announces AI regulation...",
    "use_related": true,
    "max_sources": 3
  }'
```
- [ ] Returns answer to question
- [ ] Includes 1-3 citations
- [ ] Citations have source titles
- [ ] Citations have excerpts from articles
- [ ] Relevance scores are reasonable (0-1)
- [ ] Answer references cited articles
- [ ] Response time < 10 seconds

### Q&A Edge Cases
- [ ] Empty question returns error
- [ ] Empty article returns error
- [ ] Questions unrelated to article return "not found" message
- [ ] Multiple related articles used if available

## Phase 5: Frontend (Streamlit)
- [ ] App launches without errors
- [ ] API connection shows ✓ or error
- [ ] Article input sidebar works
- [ ] Persona dropdown has 4 options
- [ ] "Generate Briefing" button works
- [ ] "Search Related" button works
- [ ] "Ask Question" input and button work

### Frontend UI Tests
- [ ] Briefing tab displays 4 sections with icons
- [ ] Related Articles tab shows matching articles
- [ ] Q&A tab shows question input and answer
- [ ] Stats tab displays article length and word count
- [ ] Loading spinners appear during API calls
- [ ] Error messages display properly
- [ ] Styling is clean and readable

## Phase 6: End-to-End Testing

### Test Case 1: Simple Article
1. [ ] Paste simple news article
2. [ ] Generate briefing
3. [ ] Verify 4 questions answered
4. [ ] Check related articles found
5. [ ] Ask question and verify answer
6. [ ] Check citations present

### Test Case 2: Technical Article
1. [ ] Paste technical news article
2. [ ] Change persona to "founder"
3. [ ] Generate briefing with founder perspective
4. [ ] Verify business implications emphasized
5. [ ] Search for startup-related articles
6. [ ] Ask question about implementation

### Test Case 3: Long Article
1. [ ] Paste 5000+ character article
2. [ ] Test still works without timeout
3. [ ] Briefing generated correctly
4. [ ] Search still returns relevant results

### Test Case 4: Multiple Personas
1. [ ] Run briefing with investor persona
2. [ ] Run briefing with student persona
3. [ ] Compare output - verify different perspectives
4. [ ] Verify personalization working

## Phase 7: Automated Testing

Run test suite:
```bash
python scripts/test_all_endpoints.py
```

Expected output:
```
[PHASE 1] Health & Database
✓ Health Check
✓ Database Stats

[PHASE 2] Vector Search
✓ Search Related Articles

[PHASE 3] Smart Briefing
✓ Briefing - investor
✓ Briefing - student
✓ Briefing - founder

[PHASE 4] Question Answering
✓ Q&A: How will this affect fintech startups?
✓ Q&A: When do companies need to comply?
✓ Q&A: What are the penalties?

SUMMARY
Total Tests: 11
Passed: 11
Failed: 0
Success Rate: 100%
```

- [ ] All 11 tests pass
- [ ] No errors in terminal
- [ ] Response times acceptable
- [ ] No timeouts

## Performance Tests

### Response Times
- [ ] `/health` < 100ms
- [ ] `/search-related` < 3 seconds
- [ ] `/briefing` < 10 seconds (includes LLM)
- [ ] `/ask-question` < 10 seconds (includes LLM)
- [ ] `/db-stats` < 100ms

### Database Tests
- [ ] 15 articles loaded
- [ ] Article count correct
- [ ] Search returns 5 results
- [ ] No duplicate results
- [ ] Relevance scores make sense

### Memory Tests
- [ ] App doesn't crash after 10 requests
- [ ] No memory leaks visible
- [ ] Embeddings model stays loaded
- [ ] ChromaDB connection stable

## Error Handling Tests

### Missing Parameters
- [ ] POST without article_text returns 400
- [ ] POST without question returns 400
- [ ] POST with empty string returns 400

### Invalid Input
- [ ] Invalid persona falls back to "investor"
- [ ] Very long text gets truncated gracefully
- [ ] HTML in article gets cleaned

### API Failures
- [ ] If Groq API fails, error message returned
- [ ] If ChromaDB fails, error message returned
- [ ] No unhandled exceptions

## Security Tests
- [ ] CORS headers present
- [ ] No sensitive data in logs
- [ ] API keys not exposed in responses
- [ ] Input sanitized (no injection possible)

## Demo Readiness Checklist
- [ ] Backend starts in < 10 seconds
- [ ] Frontend loads in < 5 seconds
- [ ] Sample article ready (copied to clipboard)
- [ ] All 3 personas tested
- [ ] Demo questions prepared
- [ ] Backup demo video recorded
- [ ] Slide deck prepared
- [ ] Architecture diagram ready

## Final Verification

```bash
# Terminal 1: Start backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Start frontend
streamlit run frontend/streamlit_app.py

# Terminal 3: Run tests
python scripts/test_all_endpoints.py
```

Expected: All tests pass, demo works smoothly

## Sign-Off

- [ ] Backend: Fully functional ✓
- [ ] Frontend: Fully functional ✓
- [ ] All endpoints tested ✓
- [ ] Error handling verified ✓
- [ ] Performance acceptable ✓
- [ ] Demo prepared and tested ✓
- [ ] Ready for deployment ✓

**PROJECT STATUS: READY FOR DEMO** 🎉
