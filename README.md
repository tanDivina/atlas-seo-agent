# Atlas SEO Agent

**Elevator Pitch:** AI-Powered SEO Strategy Generator - Scrapes competitors, analyzes content with vector search, and delivers actionable optimization blueprints to outrank your rivals.

A comprehensive SEO analysis and optimization tool built with Python.

## Features

- **Web Scraping**: Extract content from any URL for SEO analysis
- **Content Analysis**: Analyze page titles, meta descriptions, and content quality
- **Technical SEO**: Check page speed, mobile-friendliness, and URL structure
- **Keyword Research**: Identify primary and semantic keywords
- **Backlink Analysis**: Analyze link profiles and opportunities
- **Database Integration**: Store and retrieve SEO data with TiDB
- **API Ready**: Built for easy API integration

## Quick Start

### 1. Setup Environment

```bash
# Navigate to project directory
cd /Users/dorienvandenabbeele/atlas-seo-agent

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-minimal.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `DATABASE_URL`: Your TiDB connection string
- `OPENAI_API_KEY`: For AI-powered analysis (optional)
- Other API keys as needed

### 3. Test the Setup

```bash
# Test web scraper and database connection
python src/scrapers/web_scraper.py

# Run basic SEO analysis
python main.py https://example.com
```

## Usage

### Basic SEO Analysis
```python
from src.agents.seo_agent import SEOAgent
import asyncio

async def analyze_site():
    agent = SEOAgent()
    analysis = await agent.analyze_url("https://example.com")
    print(f"Overall Score: {analysis.overall_score}")
    print(f"Recommendations: {len(analysis.recommendations)}")

asyncio.run(analyze_site())
```

### Web Scraping
```python
from src.scrapers.web_scraper import scrape_url

content = scrape_url("https://example.com")
print(f"Scraped {len(content)} characters")
```

### Database Connection
```python
from src.scrapers.web_scraper import test_db_connection

test_db_connection()
```

## Project Structure

```
atlas-seo-agent/
├── src/
│   ├── agents/
│   │   └── seo_agent.py          # Main SEO analysis agent
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── content_analyzer.py   # Content SEO analysis
│   │   ├── technical_analyzer.py # Technical SEO analysis
│   │   ├── backlink_analyzer.py  # Backlink analysis
│   │   └── keyword_analyzer.py   # Keyword research
│   ├── scrapers/
│   │   └── web_scraper.py        # Web scraping utilities
│   ├── config/
│   │   └── settings.py           # Configuration management
│   └── utils/                    # Utility functions
├── data/                         # Data storage
├── logs/                         # Log files
├── tests/                        # Test files
├── docs/                         # Documentation
├── main.py                       # Entry point
├── requirements.txt              # Full dependencies
├── requirements-minimal.txt      # Minimal dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## Development

### Adding New Features
1. Create new modules in appropriate directories
2. Update requirements if adding new dependencies
3. Add tests in the `tests/` directory
4. Update documentation

### Testing
```bash
# Run tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_seo_agent.py
```

## API Integration

The project is designed to be easily extended with API endpoints. Future versions will include:
- FastAPI integration
- RESTful endpoints for SEO analysis
- Real-time scraping capabilities
- Database query endpoints

## Inspiration

The Atlas SEO Agent was inspired by the need for automated, intelligent competitor analysis in the SEO space. Traditional SEO tools often require manual input and don't leverage modern AI capabilities for semantic understanding of content. We wanted to create a tool that could automatically discover competitors, analyze their content using vector similarity, and generate actionable strategies using advanced language models.

## What it does

Atlas SEO Agent automates the entire SEO strategy generation process:
1. **Competitor Discovery**: Uses SERP scraping to find top-ranking URLs for any keyword.
2. **Content Extraction**: Robustly scrapes and cleans content from competitor pages.
3. **Semantic Analysis**: Stores embeddings in TiDB and performs vector similarity searches to find the most relevant competitor content.
4. **AI Strategy Generation**: Uses Kimi AI (Moonshot) to analyze competitors and produce a comprehensive content blueprint with themes, keywords, structure, and optimization tips.
5. **Suggested Resources**: Provides a top suggested article from the database for reference.

The result is a ready-to-use SEO strategy that helps users outrank their competitors.

## How we built it

We built Atlas SEO Agent using a modern Python stack:
- **Backend**: FastAPI for the API server, providing high-performance endpoints.
- **Database**: TiDB for scalable storage with native vector search capabilities, allowing efficient similarity queries.
- **Scraping**: BeautifulSoup and requests for robust web scraping with error handling.
- **Embeddings**: SentenceTransformers for generating content embeddings, with chunking to handle long texts.
- **AI Integration**: OpenAI client for Kimi AI to generate strategies based on competitor analysis.
- **Deployment**: Render for hosting, with optimizations for memory usage.

The workflow integrates these components seamlessly through a modular structure in src/.

## Challenges we ran into

- **Memory Management**: Handling large scraped content and embedding generation caused out-of-memory errors on free-tier hosting. We solved this with content truncation, chunked embedding processing, and worker optimization.
- **Vector Search Integration**: TiDB's vector functions required binary BLOB storage and precise SQL queries, with fallbacks for text search when vector support was unavailable.
- **Scraping Robustness**: Dealing with varying website structures and anti-bot measures required deduplication, domain filtering, and timeout handling.
- **Deployment Issues**: ModuleNotFoundError for OpenAI was fixed by updating requirements.txt. Git push conflicts were resolved with merges and force pushes.

## Accomplishments that we're proud of

- Successfully integrated TiDB vector search for semantic competitor analysis, enabling intelligent content recommendations.
- Implemented robust fallback mechanisms (vector to text search) for reliability across different environments.
- Optimized the app for low-memory deployment while maintaining functionality, including chunked processing for embeddings.
- Created a complete end-to-end workflow from keyword input to AI-generated strategy, with suggested articles for practical use.
- Deployed on Render with API endpoints ready for frontend integration.

## What we learned

- The importance of memory-efficient processing in AI applications, especially with embeddings and large texts.
- How to leverage database-native vector search (TiDB) for scalable similarity matching without external services.
- Best practices for web scraping: handling errors gracefully, deduplicating results, and respecting rate limits.
- AI prompting techniques for generating actionable SEO strategies from competitor data.
- Deployment challenges on platforms like Render, including environment variables, requirements management, and instance upgrades.

## What's next for AI Content Strategy Generator

- **Multi-Language Support**: Extend scraping and analysis to non-English content.
- **Real-Time Monitoring**: Add cron jobs for periodic competitor tracking and alerts.
- **Advanced Analytics**: Integrate Google Analytics and Search Console APIs for performance metrics.
- **Visual Dashboard**: Build a React frontend for interactive strategy visualization.
- **More AI Features**: Incorporate image analysis for visual SEO and predictive ranking models.
- **Collaboration Tools**: Allow team sharing of strategies and collaborative editing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting guide in docs/
2. Review the .env.example for configuration
3. Open an issue on GitHub
