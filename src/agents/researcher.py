import os
from typing import List
import requests
from dotenv import load_dotenv

load_dotenv()

BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

def find_top_competitor_urls(keyword: str) -> List[str]:
    """
    Find the top 5 competitor URLs for a given keyword using Bright Data Search Engine Scraper API.
    
    Args:
        keyword (str): The search keyword.
    
    Returns:
        List[str]: List of top 5 competitor URLs.
    
    Raises:
        ValueError: If BRIGHTDATA_API_TOKEN is not set.
        requests.RequestException: If the API request fails.
    """
    if not BRIGHTDATA_API_TOKEN:
        raise ValueError("BRIGHTDATA_API_TOKEN environment variable is not set.")
    
    url = "https://api.brightdata.com/serp/req"
    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "engine": "google",
        "query": keyword
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract the first 5 organic results' links
        organic_results = result.get("organic", [])
        competitor_urls = [result.get("link", "") for result in organic_results[:5] if result.get("link")]
        
        return competitor_urls
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")
    except Exception as e:
        raise Exception(f"Failed to parse API response: {e}")