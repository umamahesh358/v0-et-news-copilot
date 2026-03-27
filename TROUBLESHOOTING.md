# ET News Copilot - Troubleshooting & Diagnostic Guide

## Current Issue Analysis

### Problem Identified: Hydration Mismatch Warnings

**Severity:** LOW (Non-blocking, visual warnings only)

**Root Cause:** Browser extensions (Grammarly) are injecting data attributes into the DOM after React hydration, causing mismatch warnings.

**Impact:** 
- No functional impact on the application
- Warnings appear in browser console
- Application works normally despite warnings

---

## Issue Details

### Error Message
```
A tree hydrated but some attributes of the server rendered HTML didn't match the client properties.
```

### Why It Happens
1. Server renders HTML without extension data attributes
2. Browser loads extension (e.g., Grammarly checker)
3. Extension injects data attributes (data-gr-ext-installed, data-new-gr-c-s-check-loaded)
4. React hydration notices mismatch
5. Console warning appears

### Affected Elements
- `<body>` tag attributes
- Data attributes from Grammarly, LastPass, and similar browser extensions

---

## Solutions

### Solution 1: Suppress Extension Data Attributes (Recommended)

**File:** `app/layout.tsx`

**Approach:** Suppress known extension attributes in hydration process using `suppressHydrationWarning`.

```typescript
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased" suppressHydrationWarning>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Why It Works:**
- Tells React to not warn about hydration mismatches on this specific element
- Only suppresses warnings for `<body>` (where extensions inject attributes)
- Does not suppress other hydration errors
- Safe and recommended by React documentation

**Implementation Impact:**
- Zero breaking changes
- Warnings will disappear
- Application functionality unaffected

---

### Solution 2: Disable Browser Extensions in Development

**Steps:**
1. Open Chrome DevTools (F12)
2. Click "Sources" tab
3. In left sidebar: click "Overrides"
4. Select "Enable local overrides"
5. Add extension disable rule

**When to Use:** Development/testing only

---

### Solution 3: Use Incognito Mode

**Approach:** Test in incognito/private browsing mode where extensions don't run.

**Steps:**
1. Open browser incognito window
2. Navigate to `http://localhost:3000`
3. Extensions won't load
4. Warnings disappear

**Verification:** Check that app works perfectly in incognito mode

---

## Verification Checklist

### Functional Tests (All should PASS)

- [ ] **Page Loads** - Does `http://localhost:3000` load without errors?
- [ ] **Content Displays** - Can you see the page content?
- [ ] **Interactive** - Can you click buttons/interact with UI?
- [ ] **No 5xx Errors** - Are there any server errors (500, 502, etc.)?
- [ ] **Console Clear** - Are there JavaScript errors (not warnings)?
- [ ] **Responsive** - Does it work on mobile/tablet/desktop?

### Backend Tests (All should PASS)

```bash
# Test API connectivity
curl http://localhost:8000/health

# Expected response:
# {"status": "ok", "version": "1.0.0"}
```

### Database Tests (All should PASS)

```bash
# Verify database is loaded
curl http://localhost:8000/api/db-stats

# Should return article count and vector DB stats
```

---

## Common Issues & Fixes

### Issue 1: "Cannot GET /"
**Cause:** No page.tsx file created
**Fix:** Create `app/page.tsx` with basic content

### Issue 2: Backend Not Connected
**Cause:** CORS issue or wrong API endpoint
**Fix:** Check `NEXT_PUBLIC_API_URL` environment variable

### Issue 3: Slow Loading
**Cause:** Database initialization taking time
**Fix:** Normal on first load; subsequent requests are fast

### Issue 4: Vector Search Not Working
**Cause:** ChromaDB not initialized
**Fix:** Run backend startup script first

### Issue 5: Hydration Warnings Persist
**Cause:** Extension data attributes still present
**Fix:** Apply Solution 1 (suppressHydrationWarning)

---

## Performance Diagnosis

### Check Server Performance
```bash
# Terminal 1: Start backend with timing
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Watch for initialization time and endpoint response times
```

### Check Frontend Performance
```bash
# Terminal 2: Check Next.js build time
npm run build

# Check page load time
# Open DevTools > Network tab
# Reload page, observe timing
```

### Expected Metrics
- Server startup: < 5 seconds
- API response (search): 200-500ms
- API response (briefing): 2-5 seconds (LLM dependent)
- Page load: < 2 seconds

---

## Environment Variables Verification

### Backend (.env file)
```
GROQ_API_KEY=<should-be-set>
DEBUG=true
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Verification Steps
1. Check `.env` exists in project root
2. Check GROQ_API_KEY is set (not empty)
3. Run: `echo $GROQ_API_KEY` (should print key)
4. Check `.env` is in `.gitignore`

---

## Deployment Verification

### Before Deploying to Production

- [ ] All tests passing locally
- [ ] No hydration warnings after applying suppressHydrationWarning
- [ ] Environment variables configured in Vercel dashboard
- [ ] Backend deployed (if using separate service)
- [ ] Database initialized on production instance
- [ ] CORS properly configured for production domain

### Testing Production Build Locally

```bash
# Build for production
npm run build

# Start production server
npm start

# Test at http://localhost:3000
```

---

## Browser Compatibility

### Tested & Verified
- Chrome 120+ ✓
- Firefox 121+ ✓
- Safari 17+ ✓
- Edge 120+ ✓

### Known Issues by Browser
- **Chrome with Grammarly:** Hydration warnings (non-blocking)
- **Safari:** No known issues
- **Firefox:** No known issues

---

## Getting Help

### Debug Information to Collect

1. **Console errors:** Copy full error message
2. **Network tab:** Screenshot showing failed requests
3. **Environment:** Which OS, browser, Node version?
4. **Logs:** Output from backend startup

### Support Resources

1. Check `README.md` for main documentation
2. Check `START.md` for setup instructions
3. Run `scripts/final_check.py` for environment verification
4. Check `PROJECT_STATUS.md` for feature status

---

## Next Steps

1. **Implement Solution 1:** Add `suppressHydrationWarning` to `<body>` tag
2. **Verify Functionality:** Use verification checklist above
3. **Run Full Test Suite:** Execute `scripts/test_all_endpoints.py`
4. **Monitor Performance:** Watch backend logs for slow queries
5. **Ready to Deploy:** Follow deployment verification steps
