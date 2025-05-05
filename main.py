import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import logging
from typing import Dict, List
import pandas as pd

from scraper import WebsiteScraper
from analyzer import TextAnalyzer
from categorizer import CompanyCategorizer
from output import ReportGenerator
from project_constants import COMPANIES
from project_constants import HEADERS, TIMEOUT


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('probiotics_prospecting.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ProbioticsProspector:
    """
    Main class that orchestrates the entire prospecting process:
    1. Scrapes company websites
    2. Analyzes the content
    3. Categorizes companies
    4. Generates reports
    """
    
    def __init__(self):
        self.scraper = WebsiteScraper(max_workers=5)
        self.analyzer = TextAnalyzer()
        self.categorizer = CompanyCategorizer()
        self.report_generator = ReportGenerator()
    
    def process_companies(self, companies: List[Dict]) -> pd.DataFrame:
        """
        Run the complete prospecting pipeline for a list of companies.
        
        Args:
            companies: List of companies with 'name' and 'website' keys
            
        Returns:
            pandas DataFrame with all results
        """
        logger.info(f"Starting prospecting for {len(companies)} companies")
        
        # Step 1: Scrape websites
        logger.info("Scraping company websites...")
        scraped_data = self.scraper.scrape_websites(companies)
        logger.info(f"Successfully scraped {len([v for v in scraped_data.values() if v['status'] == 'success'])}/{len(companies)} websites")
        
        # Step 2: Analyze content
        logger.info("Analyzing scraped content...")
        analysis_results = {}
        for company_name, data in scraped_data.items():
            if data['status'] == 'success':
                combined_text = f"{data['title']} {data['description']} {data['content']}"
                analysis = self.analyzer.analyze_text(combined_text)
                categorization = self.categorizer.categorize_company(analysis)
                
                # Combine all results
                analysis_results[company_name] = {
                    **analysis,
                    **categorization
                }
            else:
                analysis_results[company_name] = {
                    'category': 'Not Relevant',
                    'relevance_score': 0,
                    'is_relevant': False,
                    'health_segments': 'None',
                    'is_fb': False,
                    'mentions_probiotics': False,
                    'is_manufacturer': False,
                    'is_brand': False,
                    'is_distributor': False
                }
        
        # Step 3: Generate report
        logger.info("Generating Excel report...")
        df = self.report_generator.create_dataframe(companies, scraped_data, analysis_results)
        self.report_generator.generate_excel_report(df)
        logger.info(f"Report generated: probiotics_prospects.xlsx")
        
        return df

def main():
    try:
        start_time = time.time()
        
        prospector = ProbioticsProspector()
        df = prospector.process_companies(COMPANIES)
        
        # Print summary
        print("\nProspecting Summary:")
        print(df[['Company Name', 'Category', 'Relevance Score']].to_string(index=False))
        
        elapsed_time = time.time() - start_time
        print(f"\nCompleted in {elapsed_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()