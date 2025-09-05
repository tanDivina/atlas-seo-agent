from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- IMPORT THIS
from pydantic import BaseModel
from sqlalchemy import text
from src.database.manager import SessionLocal, ScrapedPage, create_tables, save_scraped_content
from src.scrapers.web_scraper import scrape_url
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding

# Initialize the FastAPI app
app = FastAPI()

# --- THIS IS THE FIX ---
# Define the list of allowed origins (your frontend's URL)
origins = [
    "https://atlas-ai-source-auth-0iyo.bolt.host",
    "http://localhost:3000", # Often used for local frontend development
    "http://localhost:5173", # Another common port for local development
]

# Add the CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)
# --- END OF FIX ---


# Define the data model for our incoming requests
class UrlRequest(BaseModel):
    url: str

# Ensure tables are created when the API starts up
@app.on_event("startup")
def on_startup():
    create_tables()

# (The rest of your API code is unchanged)
@app.post("/api/analyze")
def analyze_and_store_url(request: UrlRequest):
    target_url = request.url
    content = scrape_url(target_url)
    if not content:
        return {"error": "Failed to scrape the URL."}

    qae_score = analyze_qae_score(content)
    embedding = generate_embedding(content)
    
    save_scraped_content(target_url, content, qae_score, embedding)
    
    return {
        "url": target_url,
        "qae_score": qae_score,
        "status": "Analyzed and Saved Successfully"
    }

@app.post("/api/search")
def search_similar_articles(request: UrlRequest):
    target_url = request.url
    content = scrape_url(target_url)
    if not content:
        return {"error": "Failed to scrape the target URL for search."}
        
    search_embedding = generate_embedding(content)
    search_embedding_str = str(search_embedding.tolist())

    db = SessionLocal()
    try:
        query = text(f"""
            SELECT url, qae_score, VEC_L2_DISTANCE(content_embedding, '{search_embedding_str}') AS distance
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