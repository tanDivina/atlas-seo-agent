import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from src.database.manager import SessionLocal, ScrapedPage, create_tables, save_scraped_content
from src.scrapers.web_scraper import scrape_url
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding_for_long_text
from src.agents.researcher import find_top_competitor_urls
from src.analyzers.strategist import generate_content_strategy
import struct

app = FastAPI()

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

class KeywordRequest(BaseModel):
    keyword: str

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/api/analyze")
def analyze_and_store_url(request: UrlRequest):
    # This endpoint is working perfectly and needs no changes.
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
    search_embedding_list = search_embedding.tolist()
    search_binary = struct.pack('384f', *search_embedding_list)
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT url, qae_score,
                   VEC_L2_DISTANCE(VECTOR_FROM_BINARY(content_embedding, 384), VECTOR_FROM_BINARY(:search_vec, 384)) AS distance
            FROM scraped_pages
            WHERE content_embedding IS NOT NULL
            ORDER BY distance ASC LIMIT 5;
        """)
        
        results = db.execute(query, {"search_vec": search_binary}).fetchall()
        similar_articles = [
            {"url": row.url, "qae_score": row.qae_score, "distance": f"{row.distance:.4f}"}
            for row in results
        ]
        return {"search_target": target_url, "similar_articles": similar_articles}
    finally:
        db.close()

@app.post("/api/generate-full-strategy")
def generate_full_strategy(request: KeywordRequest):
    print(f"--- Starting Full Strategy Generation for keyword: {request.keyword} ---")
    try:
        print("[1/4] Researching top competitors...")
        competitor_urls = find_top_competitor_urls(request.keyword)
        if not competitor_urls:
            return {"error": "Could not find any competitors for the keyword."}
        print(f"Found competitors: {competitor_urls}")
        
        print("\n[2/4] Analyzing and vectorizing competitors...")
        competitor_texts = []
        for url in competitor_urls:
            try:
                content = scrape_url(url)
                if content:
                    competitor_texts.append(content)
                    print(f"Successfully scraped and embedded: {url}")
                else:
                    print(f"No content scraped for: {url}")
            except Exception as scrape_error:
                print(f"Error scraping URL: {url} - {scrape_error}")
                continue  # Skip failed URLs
        
        if not competitor_texts:
            return {"error": "Could not scrape any competitor content. Try a different keyword."}
        print(f"Analyzed {len(competitor_texts)} competitors")
        
        print("\n[3/4] Performing semantic analysis in TiDB...")
        # Use the first scraped content for search embedding
        first_content = competitor_texts[0]
        search_embedding = generate_embedding_for_long_text(first_content)
        search_embedding_list = search_embedding.tolist()
        search_binary = struct.pack('384f', *search_embedding_list)
        print("Generated search embedding, binary length:", len(search_binary))
        
        db = SessionLocal()
        similar_texts = []
        results = []
        try:
            print("Executing TiDB vector similarity query...")
            query = text("""
                SELECT url, content FROM scraped_pages
                WHERE content_embedding IS NOT NULL
                ORDER BY VEC_L2_DISTANCE(VECTOR_FROM_BINARY(content_embedding, 384), VECTOR_FROM_BINARY(:search_vec, 384)) ASC
                LIMIT 5;
            """)
            
            results = db.execute(query, {"search_vec": search_binary}).fetchall()
            if results:
                similar_texts = [row.content for row in results if row.content]
                print(f"Retrieved {len(similar_texts)} competitor texts from TiDB vector search")
        except Exception as vector_error:
            print(f"TiDB vector query failed (expected if not enabled): {vector_error}")
            results = []  # Ensure results is defined for suggested_article
            # Fallback to text search on scraped content
            try:
                print("Falling back to text search...")
                for competitor_text in competitor_texts:
                    if request.keyword.lower() in competitor_text.lower():
                        similar_texts.append(competitor_text)
                similar_texts = similar_texts[:3]
                print(f"Fallback text search retrieved {len(similar_texts)} texts")
            except Exception as text_error:
                print(f"Text fallback also failed: {text_error}")
                similar_texts = []
        finally:
            db.close()
        
        if not similar_texts:
            print("No similar texts found, using scraped competitor texts")
            similar_texts = competitor_texts[:3]  # Use scraped ones as fallback
        
        print("\n[4/4] Generating final content blueprint with Kimi AI...")
        strategy_blueprint = generate_content_strategy(similar_texts)
        
        # Add suggested article from top similar result
        suggested_article = None
        if results and len(results) > 0:
            top_result = results[0]
            suggested_article = {"url": top_result.url, "content": top_result.content}
        
        print("\n--- ✅ Full Strategy Generation Complete! ---")
        return {
            "strategy_blueprint": strategy_blueprint,
            "suggested_article": suggested_article
        }

    except Exception as e:
        print(f"An unexpected error occurred in the full strategy workflow: {e}")
        return {"error": str(e)}