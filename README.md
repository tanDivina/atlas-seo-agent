# Atlas SEO Agent

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
