"""Main SEO Agent for comprehensive SEO analysis and optimization."""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from ..config.settings import settings
from ..scrapers.web_scraper import WebScraper, ScrapedPage
from ..analyzers.content_analyzer import ContentAnalyzer
from ..analyzers.technical_analyzer import TechnicalAnalyzer
from ..analyzers.backlink_analyzer import BacklinkAnalyzer
from ..analyzers.keyword_analyzer import KeywordAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class SEOAnalysis:
    """Comprehensive SEO analysis results."""
    url: str
    timestamp: datetime
    content_score: float
    technical_score: float
    backlink_score: float
    keyword_score: float
    overall_score: float
    recommendations: List[Dict[str, Any]]
    issues: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]


class SEOAgent:
    """Main SEO analysis agent."""
    
    def __init__(self):
        """Initialize the SEO agent with all necessary components."""
        self.scraper = WebScraper()
        self.content_analyzer = ContentAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.backlink_analyzer = BacklinkAnalyzer()
        self.keyword_analyzer = KeywordAnalyzer()
        
    async def analyze_url(self, url: str, depth: int = 1) -> SEOAnalysis:
        """
        Perform comprehensive SEO analysis for a given URL.
        
        Args:
            url: The URL to analyze
            depth: Analysis depth (1=basic, 2=detailed, 3=comprehensive)
            
        Returns:
            SEOAnalysis: Complete SEO analysis results
        """
        logger.info(f"Starting SEO analysis for {url} with depth {depth}")
        
        try:
            # Scrape the webpage
            page_data = await self.scraper.scrape_page(url)
            
            # Run parallel analysis
            tasks = [
                self.content_analyzer.analyze(page_data),
                self.technical_analyzer.analyze(page_data),
                self.backlink_analyzer.analyze(url),
                self.keyword_analyzer.analyze(page_data)
            ]
            
            # Execute all analysis tasks
            results = await asyncio.gather(*tasks)
            
            # Process results
            content_result, technical_result, backlink_result, keyword_result = results
            
            # Calculate scores
            content_score = content_result.get("content_score", 0)
            technical_score = technical_result.get("page_speed_score", 0)
            backlink_score = backlink_result.get("backlink_score", 0)
            keyword_score = keyword_result.get("keyword_score", 0)
            
            # Calculate overall score
            overall_score = (content_score + technical_score + backlink_score + keyword_score) / 4
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                content_result, technical_result, backlink_result, keyword_result
            )
            
            analysis = SEOAnalysis(
                url=url,
                timestamp=datetime.now(),
                content_score=content_score,
                technical_score=technical_score,
                backlink_score=backlink_score,
                keyword_score=keyword_score,
                overall_score=overall_score,
                recommendations=recommendations,
                issues=self._identify_issues(content_result, technical_result),
                opportunities=self._identify_opportunities(keyword_result)
            )
            
            logger.info(f"Completed SEO analysis for {url}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {url}: {str(e)}")
            raise
    
    def _generate_recommendations(self, content: Dict, technical: Dict, 
                                backlink: Dict, keyword: Dict) -> List[Dict[str, Any]]:
        """Generate actionable SEO recommendations."""
        recommendations = []
        
        # Content recommendations
        if content.get("title_score", 0) < 70:
            recommendations.append({
                "title": "Improve page title",
                "description": "Optimize title for better SEO performance",
                "priority": "high",
                "impact": "high"
            })
        
        if content.get("meta_description_score", 0) < 70:
            recommendations.append({
                "title": "Optimize meta description",
                "description": "Create compelling meta description within 150-160 characters",
                "priority": "high",
                "impact": "medium"
            })
        
        # Technical recommendations
        if technical.get("page_speed_score", 0) < 70:
            recommendations.append({
                "title": "Improve page speed",
                "description": "
