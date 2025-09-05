import sys
import numpy as np
from src.database.manager import SessionLocal, ScrapedPage
from src.scrapers.web_scraper import scrape_url
from src.analyzers.content_analyzer import generate_embedding

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_similar_articles(url: str, limit: int = 5):
    """
    Finds and prints the most semantically similar articles
    from the database compared to the given URL.
    """
    if not url:
        print("❌ No URL provided.")
        return

    print(f"--- Finding articles similar to: {url} ---")
    
    # 1. Scrape and vectorize the input URL to get a search vector
    content = scrape_url(url)
    if not content:
        print("Could not scrape the target URL. Aborting search.")
        return
    
    search_embedding = generate_embedding(content)
    
    db = SessionLocal()
    try:
        print("\nSearching the database for similar content...")
        
        # 2. Fetch all articles from the database
        articles = db.query(ScrapedPage).filter(ScrapedPage.content_embedding.isnot(None)).all()
        
        if not articles:
            print("No articles with embeddings found in the database.")
            return
        
        # 3. Calculate similarity scores
        similarities = []
        for article in articles:
            if article.content_embedding:
                similarity = cosine_similarity(search_embedding, article.content_embedding)
                similarities.append((article, similarity))
        
        # 4. Sort by similarity (higher is better)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        print("\n--- Top Similar Articles Found ---")
        for i, (article, similarity) in enumerate(similarities[:limit]):
            print(f"{i+1}. URL: {article.url}")
            print(f"   QAE Score: {article.qae_score}")
            print(f"   Similarity Score: {similarity:.4f}\n")

    except Exception as e:
        print(f"❌ An error occurred during the search: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a URL to search against.")
        print("   Usage: python search.py <your_url_here>")
    else:
        target_url = sys.argv[1]
        find_similar_articles(target_url)
