from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding_for_long_text

app = FastAPI()

# --- THE CRITICAL CORS FIX ---
origins = [
    "https://atlas-ai-source-auth-0iyo.bolt.host", # Your frontend
    "https://atlas-seo-agent-nsa8.onrender.com", # Your backend itself
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
# --- END OF FIX ---

class UrlRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/analyze")
def analyze_and_store_url(request: UrlRequest):
    # For now, just analyze the URL content
    target_url = request.url
    # Simple analysis - count characters as a placeholder
    content = f"Content from {target_url}"  # Placeholder
    qae_score = analyze_qae_score(content)
    embedding = generate_embedding_for_long_text(content)
    return {"url": target_url, "qae_score": qae_score, "status": "Analyzed Successfully"}

@app.post("/api/search")
def search_similar_articles(request: UrlRequest):
    # Placeholder implementation
    target_url = request.url
    content = f"Content from {target_url}"  # Placeholder
    search_embedding = generate_embedding_for_long_text(content)
    # Return placeholder results
    similar_articles = [
        {"url": "https://example.com/article1", "qae_score": 5, "distance": "0.1234"},
        {"url": "https://example.com/article2", "qae_score": 3, "distance": "0.2345"}
    ]
    return {"search_target": target_url, "similar_articles": similar_articles}