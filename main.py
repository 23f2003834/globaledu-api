# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from lxml import html
from urllib.parse import quote
from typing import Optional

app = FastAPI(title="GlobalEdu Country Outline API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GlobalEdu Country Outline API is running!"}

@app.get("/api/outline")
async def get_country_outline(country: Optional[str] = None):
    # ── 1. Input validation
    if not country:
        raise HTTPException(status_code=400, detail="Missing 'country' query parameter")
    print(f"[DEBUG] Requested country: {country}")

    # ── 2. Build Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{quote(country)}"
    print(f"[DEBUG] Wikipedia URL: {wiki_url}")

    # ── 3. Fetch page
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print("[DEBUG] Sending HTTP request...")
            response = await client.get(wiki_url)
            print(f"[DEBUG] HTTP Status: {response.status_code}")
    except httpx.RequestError as e:
        print(f"[ERROR] Network error: {e}")
        raise HTTPException(status_code=502, detail="Failed to reach Wikipedia")

    if response.status_code != 200:
        print(f"[ERROR] Page not found: {response.status_code}")
        raise HTTPException(status_code=404, detail=f"Country page not found: {country}")

    # ── 4. Parse HTML
    try:
        tree = html.fromstring(response.content)
        print(f"[DEBUG] HTML parsed, length: {len(response.content)} bytes")
    except Exception as e:
        print(f"[ERROR] HTML parsing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse Wikipedia page")

    # ── 5. Extract headings
    headings = tree.xpath("//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
    print(f"[DEBUG] Found {len(headings)} headings")

    # ── 6. Build Markdown
    md_outline = "## Contents\n\n"
    for i, h in enumerate(headings):
        level = int(h.tag[1])
        text = h.text_content().strip()
        if text:
            md_outline += "#" * level + " " + text + "\n\n"
            if i < 5:  # Show first 5 in console
                print(f"[DEBUG] Heading: {'#' * level} {text}")

    print(f"[DEBUG] Markdown outline length: {len(md_outline)} chars")
    return {"outline": md_outline}

# ── 7. Run server (only when executed directly)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,        # Auto-reload on code change
        log_level="debug"   # Full logs
    )