# ET News Copilot - Preview 404 Error Diagnosis & Resolution

## ROOT CAUSE ANALYSIS

### Primary Issue: Missing Backend Server
**Status:** CRITICAL  
**Impact:** Frontend shows 404 errors when trying to call API endpoints

The Next.js frontend (`app/page.tsx`) makes HTTP requests to `http://localhost:8000/api/*` endpoints, but:
- ✗ No backend server is running in the preview
- ✗ The FastAPI backend exists in `/backend/` but is not deployed/running
- ✗ The v0 preview only runs the Next.js frontend

### Secondary Issue: Hydration Warnings (Minor)
**Status:** COSMETIC  
**Impact:** Console warnings only, doesn't affect functionality

Browser extension interference causing HTML attribute mismatches between SSR and client rendering:
- `data-new-gr-c-s-check-loaded` and `data-gr-ext-installed` attributes added by Grammarly
- Not a code issue - just noise in console

---

## ISSUES IDENTIFIED

### Issue #1: API Calls to Non-Existent Backend
**Symptom:** 404 errors when clicking "Generate Briefing"  
**Root Cause:** FastAPI backend not running  
**Current Code:**
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

**Problem:**
- Hardcoded localhost:8000
- Backend must be running separately in a terminal
- v0 Preview environment doesn't support running Python backends

### Issue #2: No Environment Variable Configuration
**Symptom:** API_URL defaults to localhost in preview  
**Root Cause:** NEXT_PUBLIC_API_URL not set in .env.local  
**Impact:** Frontend tries to call non-existent backend

### Issue #3: Missing Error Handling for Backend Unavailability
**Symptom:** Cryptic error messages  
**Root Cause:** Generic error messages don't explain backend not running  
**Impact:** User confusion about what's wrong

---

## RECOMMENDED SOLUTIONS

### Solution 1: Add Mock Backend Data (Recommended for Demo)
**Effort:** Low | **Time:** 15 min | **Testing:** 5 min

Replace API calls with hardcoded sample data for demonstration purposes.

**Steps:**
1. Create mock data service with sample briefings
2. Add "Use Sample Data" toggle in UI
3. Return hardcoded responses matching API format
4. Users can still see full UI functionality without backend

**Benefits:**
- Works immediately in v0 preview
- Demonstrates UI/UX
- No configuration needed

### Solution 2: Configure Backend Deployment
**Effort:** Medium | **Time:** 30 min | **Testing:** 10 min

Deploy FastAPI backend to Vercel or Railway.

**Steps:**
1. Deploy backend to Railway.app (free tier)
2. Add deployed URL to .env.local
3. Update frontend to use deployed backend
4. Test all endpoints

**Benefits:**
- Full feature demo
- Real API responses
- Production-ready

### Solution 3: Add Graceful Degradation
**Effort:** Low | **Time:** 20 min | **Testing:** 10 min

Detect backend unavailability and show helpful UI.

**Steps:**
1. Add health check endpoint call on mount
2. Show "Backend Unavailable" state with instructions
3. Disable buttons with helpful tooltip
4. Provide sample data button

**Benefits:**
- Professional UX
- Clear error communication
- User guidance

### Solution 4: Create Standalone Frontend
**Effort:** Medium | **Time:** 40 min | **Testing:** 15 min

Build integrated backend + frontend as one Next.js app using API Routes.

**Steps:**
1. Create `/app/api/` route handlers
2. Move Python logic to Node.js/TypeScript
3. Use AI SDK for LLM calls directly
4. Remove external backend dependency

**Benefits:**
- Single deployment
- Works in v0 preview
- Simplified architecture

---

## STEP-BY-STEP TROUBLESHOOTING GUIDE

### Step 1: Verify Frontend is Loading
- Open Developer Console (F12)
- Check: Is page HTML loading? ✓
- Check: Are styles applying? ✓
- **Status:** Frontend loads correctly

### Step 2: Identify API Failures
- Open Network tab (F12 > Network)
- Click "Generate Briefing"
- Check: What's the response status?
- **Expected:** 404 Not Found (localhost:8000 not running)
- **Fix:** Start backend or use alternative solution

### Step 3: Check Environment Variables
```bash
# Check what API_URL is being used
echo $NEXT_PUBLIC_API_URL

# If empty, backend URL is defaulting to localhost:8000
```

### Step 4: Verify Backend Status
```bash
# In terminal, check if backend is running
curl http://localhost:8000/health

# Expected: JSON response with status
# If failed: Backend not running
```

### Step 5: Test with Mock Data
- If backend unavailable, use mock solution
- Modify page.tsx to use sample data
- Verify UI renders correctly

---

## QUICK FIX: Add Mock Backend (5 minutes)

This is the fastest way to get the preview working:

**File:** `/vercel/share/v0-project/app/page.tsx`

Replace the fetch calls with this mock service:

```typescript
// Mock data service
const mockBriefings: Record<string, any> = {
  investor: {
    briefing: {
      what_happened: "A major regulatory announcement was made affecting the technology sector.",
      why_it_matters: "This could impact valuations and investment returns across multiple companies.",
      who_involved: "Government agencies, tech companies, regulatory bodies",
      what_next: "Industry consultation phase expected in the coming weeks"
    },
    related_articles: [
      {
        title: "Tech Companies Response to New Regulations",
        snippet: "Major tech firms are preparing for compliance...",
        similarity_score: 0.94,
        date: "2025-03-25"
      }
    ]
  }
};

// Then in handleGenerateBriefing:
const handleGenerateBriefing = async () => {
  if (!articleText.trim()) {
    setError('Please enter article text');
    return;
  }
  
  setLoading(true);
  setError('');
  
  // Use mock data instead of API call
  setTimeout(() => {
    setBriefing(mockBriefings[persona].briefing);
    setRelatedArticles(mockBriefings[persona].related_articles);
    setLoading(false);
  }, 1000); // Simulate API delay
};
```

---

## HYDRATION MISMATCH WARNINGS (Cosmetic)

The warnings about hydration mismatch are caused by browser extensions (likely Grammarly).

**Why it happens:**
- Server renders HTML without extension attributes
- Client hydrates with extension attributes added
- Attributes don't match → warning

**Why it's safe:**
- React detects mismatch but continues
- `suppressHydrationWarning` is already in place
- No functionality is broken
- Only console noise

**Solution:** Already applied in `app/layout.tsx`:
```typescript
<body className="font-sans antialiased" suppressHydrationWarning>
```

---

## VERIFICATION CHECKLIST

After implementing a solution, verify:

- [ ] Frontend loads without JavaScript errors
- [ ] "Generate Briefing" button responds to click
- [ ] Results display in tabs (Briefing/Related/Q&A)
- [ ] Persona selection works
- [ ] Error messages are helpful and clear
- [ ] No 404 errors in Network tab
- [ ] Works on different screen sizes
- [ ] Works on mobile devices
- [ ] API or mock data returns expected format
- [ ] Citations display correctly in Q&A tab

---

## RECOMMENDED IMPLEMENTATION

**For immediate demo/testing:** Use Solution 1 (Mock Backend) - 15 minutes
**For production:** Use Solution 2 (Deploy Backend) - 30 minutes
**For long-term:** Use Solution 4 (Integrated Backend) - 40 minutes

---

## DEPLOYMENT OPTIONS

### Option A: Deploy to Railway (Recommended)
1. Sign up at railway.app
2. Connect GitHub or upload code
3. Railway auto-detects FastAPI
4. Gets public URL in 2 minutes
5. Update `.env.local` with URL

### Option B: Deploy to Vercel with Python Backend
1. Create separate backend directory
2. Use Vercel's Python runtime
3. Deploy as separate project
4. Get public API URL
5. Update frontend to use it

### Option C: Run Locally in Parallel
1. Terminal 1: `cd backend && python -m uvicorn backend.main:app`
2. Terminal 2: `npm run dev` (Next.js frontend)
3. Open http://localhost:3000
4. Both running locally on your machine

