# ET News Copilot - Complete Verification & Troubleshooting Guide

## QUICK STATUS CHECK (2 minutes)

### What Should You See Now?

**When You Open the Preview:**
```
✓ Header: "ET News Copilot - Transform articles into intelligent briefings"
✓ Status Banner: "Using sample data for demonstration"
✓ Input Section: Text area for article content
✓ Buttons: Generate Briefing, Ask Question
✓ Demo Mode indicator: Top right corner
```

**When You Click "Generate Briefing":**
```
✓ Loading spinner appears for ~1.5 seconds
✓ 4 briefing cards appear: What Happened, Why It Matters, Who's Involved, What Next
✓ Related Articles tab shows 3 sample articles with similarity scores
✓ No error messages
✓ No 404 errors in console
```

**When You Ask a Question:**
```
✓ Answer appears with formatted text
✓ Citations show sources and quotes
✓ Relevance scores displayed
✓ Everything rendered correctly
```

---

## VERIFICATION CHECKLIST

### Browser Testing

- [ ] **Desktop Chrome/Firefox/Safari**
  - Page loads without JavaScript errors
  - All buttons are clickable
  - Status banner visible at top
  - Mock data responds to interactions

- [ ] **Mobile Device (iPhone/Android)**
  - Layout responsive and readable
  - Text size appropriate
  - Buttons easy to tap
  - Scrolling smooth
  - No layout shifts

- [ ] **Different Screen Sizes**
  - 1920x1080 (Desktop)
  - 1366x768 (Laptop)
  - 768x1024 (Tablet)
  - 375x667 (Mobile)

### Functionality Testing

- [ ] **Article Input**
  - Can paste text into textarea
  - URL field accepts input
  - Persona buttons toggle selection
  - Character count doesn't break UI

- [ ] **Briefing Generation**
  - Click "Generate Briefing"
  - Spinner appears
  - Results display in Briefing tab
  - All 4 fields have content
  - No HTML rendering in text
  - Formatting looks professional

- [ ] **Related Articles Tab**
  - Shows 3 articles by default
  - Similarity scores display correctly (90-97%)
  - Dates show in correct format
  - Snippets are readable
  - Hover effects work on desktop

- [ ] **Q&A Tab**
  - Question input accepts text
  - "Ask" button responds to click
  - Answer displays in blue card
  - Citations show below answer
  - Source names are visible
  - Quotes are in quotes
  - Relevance scores display

- [ ] **Error Handling**
  - Submitting empty article shows error
  - Submitting empty question shows error
  - Error messages clear when user fixes input
  - No JavaScript errors in console

- [ ] **Persona Selection**
  - All 4 personas work: investor, student, founder, journalist
  - Different briefings for different personas
  - Selection persists across requests
  - Styling highlights selected persona

---

## DETAILED VERIFICATION STEPS

### Step 1: Check Page Load (1 min)

```
Action: Open the v0 preview URL
Expected:
  - Page loads in <3 seconds
  - No JavaScript errors in console
  - Status banner shows "Demo Mode" or "Backend Connected"
  - All UI elements visible
  
Verify:
1. Open DevTools (F12 or Cmd+Shift+I)
2. Check Console tab - no red errors
3. Check Network tab - all requests successful (or CSS/JS loads)
4. All colors load correctly
5. Font renders properly
```

### Step 2: Test Input Fields (1 min)

```
Action: Interact with input elements
Expected:
  - Article URL field accepts input
  - Article text area accepts multiline text
  - Persona buttons are clickable
  - No console warnings

Test Cases:
1. Click URL field → type → text appears
2. Click textarea → type long text → scrolling works
3. Click each persona button → button highlights
4. Paste large article (~2000 words) → works smoothly
```

### Step 3: Generate Briefing with Each Persona (5 min)

```
Action: Generate briefing for different personas
Expected:
  - Each persona gets different briefing
  - Loading spinner shows for ~1.5 seconds
  - Results appear in Briefing tab
  - No errors in console

Test Cases:

1. Investor Persona:
   - Briefing mentions financial impact
   - Why It Matters emphasizes investment/valuation
   - Related articles focus on market/competitive impact
   
2. Student Persona:
   - Briefing mentions learning/career
   - Why It Matters emphasizes educational value
   - Related articles focus on skills/knowledge
   
3. Founder Persona:
   - Briefing mentions business operations
   - Why It Matters emphasizes competitive advantage
   - Related articles focus on startup/product impact
   
4. Journalist Persona:
   - Briefing mentions newsworthy elements
   - Why It Matters emphasizes public interest
   - Related articles focus on trends/story angles
```

### Step 4: Test Related Articles (2 min)

```
Action: Click "Related" tab
Expected:
  - Shows 3 articles minimum
  - Each has title, snippet, score, date
  - Similarity scores between 88-97%
  - Dates are formatted correctly (YYYY-MM-DD)

Verify:
1. All articles display in scrollable list
2. Hover effects work (shadow appears)
3. Text doesn't overflow containers
4. Scores show as percentages (e.g., "94%")
5. Dates are readable and reasonable
```

### Step 5: Test Q&A System (3 min)

```
Action: Ask questions in Q&A tab
Expected:
  - Question input accepts text
  - Answer appears in blue card
  - Citations display below
  - No errors occur

Test Questions:
1. "How will this affect my business?"
2. "What are the key risks?"
3. "Who should be concerned?"
4. "What actions should be taken?"

Expected Results:
- Thoughtful, contextual answers
- Answers mention specific topics from article
- Citations show real source names
- Confidence scores reasonable (85-98%)
```

### Step 6: Test Error States (2 min)

```
Action: Submit empty form
Expected:
  - Click "Generate Briefing" with no text
  - Error message appears at top
  - Error is clear and helpful
  - Buttons remain functional after error

Test Cases:
1. No article text → Error message appears
2. No question text → Error message appears
3. Fix issue (add text) → Error clears
4. Submit again → Works correctly
```

### Step 7: Test Responsive Design (3 min)

```
Action: Open DevTools, test different screen sizes
Expected:
  - Layout adapts to all screen sizes
  - Text remains readable
  - Buttons remain clickable
  - No horizontal scrolling on mobile

Screen Sizes to Test:
- 375x667 (iPhone)
- 768x1024 (iPad)
- 1366x768 (Laptop)
- 1920x1080 (Desktop)

For Each Screen Size:
1. Layout stacks appropriately
2. Font sizes readable
3. Buttons tap-able (min 44px on mobile)
4. Cards don't overflow
5. Images scale properly
```

### Step 8: Test in Different Browsers (2 min)

```
Action: Test in multiple browsers
Required Browsers:
  - Chrome/Chromium
  - Firefox
  - Safari (if on Mac)
  - Mobile Safari (if on iPhone)

For Each Browser:
- Page loads without errors
- Styling renders correctly
- All interactive elements work
- Performance is good (<3s load)
```

---

## WHAT YOU'LL SEE DIFFERENT BETWEEN MODES

### Demo Mode (Mock Data - Current)

**Status Banner:**
```
Using sample data for demonstration. 
Backend not connected - using realistic mock responses.
```

**Top Right Indicator:**
```
Demo Mode
Sample data
```

**Behavior:**
- ~1.5s artificial delay when loading
- Responses always same for same persona
- Doesn't require backend running
- Perfect for UI/UX demo
- No network requests to `/api/*`

### Production Mode (Real Backend)

**Status Banner:**
```
(No warning banner)
```

**Top Right Indicator:**
```
✓ Backend Connected
15 articles in DB
```

**Behavior:**
- Instant or fast responses
- Real article analysis
- Different responses each time
- Requires backend running
- Network requests to `/api/*` endpoints

---

## TROUBLESHOOTING COMMON ISSUES

### Issue: "Backend not connected" Warning Always Shows

**Cause:** Backend server not running (expected in v0 preview)

**Solution:**
1. This is normal behavior in preview mode
2. Click "Generate Briefing" anyway - mock data will work
3. To use real backend:
   - Run: `python -m uvicorn backend.main:app --reload`
   - Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`

### Issue: 404 Errors in Network Tab

**Cause:** Backend not running, trying to call real API

**Solution:**
1. Page should fall back to mock data automatically
2. Check Console for error messages
3. If stuck on error screen:
   - Hard refresh (Ctrl+Shift+R)
   - Check if backend startup failed
   - Restart Next.js dev server

### Issue: Spinner Spins Forever

**Cause:** API request hanging or timeout

**Solution:**
1. Check Network tab for stalled requests
2. Kill backend with Ctrl+C, restart
3. Hard refresh browser
4. If persists, clear browser cache

### Issue: Text Looks Broken/Misaligned

**Cause:** CSS not loading or font issue

**Solution:**
1. Hard refresh with Ctrl+Shift+R
2. Check Network tab for CSS errors
3. Restart Next.js dev server: `npm run dev`
4. Check browser console for warnings

### Issue: Persona Selection Not Working

**Cause:** State not updating correctly

**Solution:**
1. Verify button highlights when clicked
2. Ensure briefing generated AFTER selecting persona
3. Hard refresh if state seems stuck
4. Check console for JavaScript errors

### Issue: Mobile Layout Broken

**Cause:** Responsive classes not applying

**Solution:**
1. Check DevTools device toggle is on
2. Verify viewport meta tag in HTML
3. Hard refresh on mobile device
4. Test in different mobile browsers

---

## PERFORMANCE BENCHMARKS

### Expected Load Times

| Metric | Expected | Status |
|--------|----------|--------|
| Page Load | <2s | Should be instant in preview |
| Briefing Generation | 1.5s | Mock data simulates delay |
| Related Articles | <300ms | Should appear immediately |
| Q&A Response | 1.5s | Mock data simulates delay |
| Mobile (4G) | <4s total | Should still be fast |

### Visual Metrics

| Metric | Target | How to Check |
|--------|--------|-------------|
| Largest Contentful Paint | <2s | DevTools Lighthouse |
| First Input Delay | <100ms | DevTools Performance |
| Cumulative Layout Shift | <0.1 | DevTools Lighthouse |

---

## SIGN OF SUCCESS

✓ Page loads instantly
✓ Click "Generate Briefing" with any persona
✓ Results appear smoothly in tabs
✓ No console errors
✓ Status shows "Demo Mode"
✓ All 4 personas work differently
✓ Q&A shows citations
✓ Works on mobile
✓ No 404 errors
✓ Professional appearance

If you see all these, the app is working correctly!

---

## NEXT STEPS AFTER VERIFICATION

### To Use Real Backend (Optional)

1. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Set GROQ API key:**
   ```bash
   echo "GROQ_API_KEY=your_key_here" > .env
   ```

3. **Start backend in Terminal 1:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

4. **Update frontend .env.local:**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

5. **Restart Next.js in Terminal 2:**
   ```bash
   npm run dev
   ```

6. **Backend should now be connected!**

### To Deploy Backend

See `PREVIEW_ISSUE_DIAGNOSIS.md` for Railway/Vercel deployment options.

