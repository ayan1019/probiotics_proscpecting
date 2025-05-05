import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Optional
import time

from project_constants import HEADERS, TIMEOUT

class WebsiteScraper:
    """
    Handles scraping of company websites to extract relevant text content.
    Implements retry logic and parallel processing for efficient scraping.
    """
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.ua = UserAgent()
        
    def _get_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract and clean text from BeautifulSoup object"""
        # Remove unwanted tags
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
            element.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return ' '.join(chunk for chunk in chunks if chunk)
    
    def _scrape_single_page(self, url: str, retries: int = 3) -> Optional[Dict]:
        """Scrape a single webpage with retry logic"""
        for attempt in range(retries):
            try:
                # Rotate user agent
                headers = HEADERS.copy()
                headers['User-Agent'] = self.ua.random
                
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=TIMEOUT,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Get meta data
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                description = meta_desc['content'] if meta_desc else ""
                
                title = soup.title.string if soup.title else ""
                
                # Get main content
                main_content = ""
                for tag in ['main', 'article', 'div.content', 'section']:
                    element = soup.find(tag)
                    if element:
                        main_content += self._get_clean_text(element) + " "
                
                # If no main content found, use entire page
                if not main_content.strip():
                    main_content = self._get_clean_text(soup)
                
                return {
                    'title': title.strip(),
                    'description': description.strip(),
                    'content': main_content.strip(),
                    'url': url,
                    'status': 'success'
                }
                
            except Exception as e:
                if attempt == retries - 1:
                    return {
                        'title': "",
                        'description': "",
                        'content': "",
                        'url': url,
                        'status': f'failed: {str(e)}'
                    }
                time.sleep(1)  # Wait before retry
                
        return None
    
    def scrape_websites(self, companies: list) -> Dict[str, Dict]:
        """
        Scrape multiple websites in parallel.
        
        Args:
            companies: List of companies with 'name' and 'website' keys
            
        Returns:
            Dictionary with company names as keys and scraped data as values
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_company = {
                executor.submit(self._scrape_single_page, company['website']): company
                for company in companies
            }
            
            for future in as_completed(future_to_company):
                company = future_to_company[future]
                try:
                    scraped_data = future.result()
                    results[company['name']] = scraped_data
                except Exception as e:
                    results[company['name']] = {
                        'title': "",
                        'description': "",
                        'content': "",
                        'url': company['website'],
                        'status': f'failed: {str(e)}'
                    }
        
        return results