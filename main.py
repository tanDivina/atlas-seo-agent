import sys
from src.scrapers.web_scraper import scrape_url
from src.database.manager import create_tables, save_scraped_content
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding  # <-- Import the new function

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a URL to scrape.")
        print("   Usage: python main.py <your_url_here>")
        return

    target_url = sys.argv[1]
    
    # 1. Ensure database tables are created
    create_tables()

    # 2. Scrape the content
    content = scrape_url(target_url)

    if content:
        # 3. Analyze for QAE score
        qae_score = analyze_qae_score(content)

        # 4. Generate the vector embedding
        embedding = generate_embedding(content)

        # 5. Save everything to the database
        save_scraped_content(target_url, content, qae_score, embedding)
    else:
        print("Scraping failed. Nothing to save to the database.")

if __name__ == "__main__":
    main()
