import requests
from bs4 import BeautifulSoup

def scrape_url(url: str):
    """Fetches and parses the content of a URL, pretending to be a browser."""
    print(f"Scraping URL: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = ' '.join(soup.stripped_strings)
        
        print(f"Successfully scraped {len(text_content)} characters.")
        return text_content
    except requests.RequestException as e:
        print(f"Error scraping URL: {e}")
        return None
