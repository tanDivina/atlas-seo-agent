# Atlas SEO Agent

AI-powered SEO strategy generator that scrapes competitors, analyzes content with vector search in TiDB, and generates actionable content blueprints using Groq's Moonshot Kimi model ("moonshotai/kimi-k2-instruct-0905").

## Features

- **SERP Scraping**: Uses Bright Data API to fetch top competitor URLs for a keyword.
- **Content Extraction**: Scrapes and cleans content from competitor pages.
- **Vector Embeddings**: Generates 384-dim embeddings with paraphrase-MiniLM-L3-v2 and stores in TiDB.
- **Semantic Search**: Uses TiDB vector similarity (L2 distance) to find relevant competitor content.
- **AI Strategy Generation**: Generates comprehensive SEO strategies with Groq Kimi AI.
- **API Endpoints**:
  - POST /api/analyze: Analyze and store a URL's content and embedding.
  - POST /api/search: Search similar articles by vector similarity.
  - POST /api/generate-full-strategy: Full workflow – scrape competitors, search semantically, generate strategy with suggested article.

## Setup

1. Clone the repo: `git clone https://github.com/tanDivina/atlas-seo-agent.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   - DATABASE_URL: TiDB connection string.
   - GROQ_API_KEY: Your Groq API key (get from groq.com).
   - BRIGHTDATA_API_TOKEN: Your Bright Data token.
4. Run locally: `uvicorn api:app --reload`
5. Deploy: Use Render or similar; set env vars in dashboard.

## Usage

Test the full strategy endpoint:

```bash
curl -X POST "http://localhost:8000/api/generate-full-strategy" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "seo tips"}'
```

Returns: {"strategy_blueprint": "AI strategy...", "suggested_article": {"url": "...", "content": "..."}}

## Architecture

- **Backend**: FastAPI (Python 3.11).
- **Database**: TiDB with SQLAlchemy for vector storage.
- **AI**: Groq (Moonshot Kimi model for strategy generation).
- **Scraping**: requests + BeautifulSoup.
- **Embeddings**: sentence-transformers (paraphrase-MiniLM-L3-v2).

## Roadmap

- Add more AI models (Gemini, Moonshot direct).
- Frontend dashboard for strategy visualization.
- Advanced analytics (keyword clustering).

## License

MIT License.
