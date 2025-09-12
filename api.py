import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from src.database.manager import SessionLocal, ScrapedPage, create_tables, save_scraped_content
from src.scrapers.web_scraper import scrape_url
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding_for_long_text

app = FastAPI()

# --- THE CORRECT CORS FIX ---
origins = [
    "https://atlas-ai-source-auth-0iyo.bolt.host",
    "https://atlas-seo-agent-nsa8.onrender.com",
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/api/analyze")
def analyze_and_store_url(request: UrlRequest):
    target_url = request.url
    content = scrape_url(target_url)
    if not content: return {"error": "Failed to scrape the URL."}
    qae_score = analyze_qae_score(content)
    embedding = generate_embedding_for_long_text(content)
    save_scraped_content(target_url, content, qae_score, embedding)
    return {"url": target_url, "qae_score": qae_score, "status": "Analyzed and Saved Successfully"}

@app.post("/api/search")
def search_similar_articles(request: UrlRequest):
    target_url = request.url
    content = scrape_url(target_url)
    if not content: return {"error": "Failed to scrape the target URL for search."}
    search_embedding = generate_embedding_for_long_text(content)
    search_embedding_str = json.dumps(search_embedding.tolist())  # JSON array string for VEC_FROM_TEXT
    db = SessionLocal()
    try:
        query = text(f"""
            SELECT url, qae_score, VEC_L2_DISTANCE(VEC_FROM_TEXT(CAST(content_embedding AS CHAR)), VEC_FROM_TEXT('{search_embedding_str}')) AS distance
            FROM scraped_pages ORDER BY distance ASC LIMIT 5;
        """)
        results = db.execute(query).fetchall()
        similar_articles = [
            {"url": row.url, "qae_score": row.qae_score, "distance": f"{row.distance:.4f}"}
            for row in results
        ]
        return {"search_target": target_url, "similar_articles": similar_articles}
    finally:
        db.close()