"""Technical SEO analyzer for website performance and structure."""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Analyzes technical SEO aspects."""
    
    async def analyze(self, page_data) -> Dict[str, Any]:
        """Analyze technical SEO factors."""
        return {
            "page_speed_score": self._analyze_page_speed(page_data),
            "mobile_friendly_score": self._analyze_mobile_friendly(page_data),
            "structured_data_score": self._analyze_structured_data(page_data),
            "url_structure_score": self._analyze_url_structure(page_data),
            "internal_linking_score": self._analyze_internal_linking(page_data)
        }
    
    def _analyze_page_speed(self, page_data) -> float:
        """Analyze page speed factors."""
        content_size = len(page_data.html)
        
        if content_size < 50000:
            return 90.0
        elif content_size < 100000:
            return 80.0
        elif content_size < 500000:
            return 70.0
        else:
            return 50.0
    
    def _analyze_mobile_friendly(self, page_data) -> float:
        """Analyze mobile-friendliness."""
        viewport = page_data.soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            return 85.0
        return 40.0
    
    def _analyze_structured_data(self, page_data) -> float:
        """Analyze structured data implementation."""
        if page_data.structured_data:
            return 90.0
        return 20.0
    
    def _analyze_url_structure(self, page_data) -> float:
        """Analyze URL structure."""
        url = page_data.url
        score = 70.0
        
        if url.startswith('https://'):
            score += 15.0
        
        if len(url) < 100:
            score += 10.0
        
        return min(score, 100.0)
    
    def _analyze_internal_linking(self, page_data) -> float:
        """Analyze internal linking structure."""
        internal_links = len(page_data.links.get('internal', []))
        
        if internal_links >= 10:
            return 90.0
        elif internal_links >= 5:
            return 70.0
        elif internal_links >= 3:
            return 50.0
        else:
            return 30.0
