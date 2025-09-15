import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus
import json  # Import the json library
from bs4 import BeautifulSoup

load_dotenv()

def find_top_competitor_urls(keyword: str) -> list[str]:
    """
    Finds top 3 unique competitor URLs for a keyword using the Bright Data Request API for SERP scraping.
    """
    # --- THIS IS OUR FINAL DEBUGGING TRACER BULLET ---
    print("--- ✅ RUNNING FINAL researcher.py with JSON DUMP ---")
    # --- END OF TRACER BULLET ---

    api_token = os.getenv("BRIGHTDATA_API_TOKEN")
    if not api_token:
        raise ValueError("BRIGHTDATA_API_TOKEN environment variable not set.")

    url = "https://api.brightdata.com/request"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    
    encoded_keyword = quote_plus(keyword)
    search_url = f"https://www.google.com/search?q={encoded_keyword}"
    
    payload = {
        "zone": "serp_api1",
        "url": search_url,
        "format": "json"
    }
    
    try:
        print("Making Bright Data API request...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print("Received response from Bright Data API.")
        response.raise_for_status()
        
        result = response.json()
        
        # --- THIS IS THE CRITICAL DEBUGGING LINE ---
        # Print the entire JSON response to the log so we can see its structure
        print("--- 🚨 BRIGHT DATA SERVER RESPONSE (FULL JSON): ---")
        print(json.dumps(result, indent=2))
        print("--- END OF BRIGHT DATA RESPONSE ---")
        # --- END OF DEBUGGING LINE ---

        # Parse the body if present
        body = result.get('body', result)
        urls = []
        seen_urls = set()
        
        if isinstance(body, str):
            # Parse HTML to extract organic links
            soup = BeautifulSoup(body, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http') and 'google' not in href.lower():
                    # Deduplicate and filter for unique, relevant links
                    if href not in seen_urls and len(urls) < 3:
                        # Additional filter: avoid duplicates from same domain if possible
                        domain = href.split('/')[2] if '/' in href else ''
                        if len(urls) == 0 or urls[-1].split('/')[2] != domain:
                            urls.append(href)
                            seen_urls.add(href)
        else:
            # Parse JSON results
            organic_results = body.get('organic', []) or body.get('results', [])
            for r in organic_results:
                link = r.get('link', '')
                if link and link not in seen_urls and len(urls) < 3:
                    domain = link.split('/')[2] if '/' in link else ''
                    if len(urls) == 0 or urls[-1].split('/')[2] != domain:
                        urls.append(link)
                        seen_urls.add(link)
        
        print(f"Extracted {len(urls)} unique URLs: {urls}")
        
        return urls

    except requests.RequestException as e:
        print(f"Bright Data API request failed: {e}")
        if e.response is not None:
            print(f"Response body from Bright Data: {e.response.text}")
        return []