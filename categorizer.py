from typing import Dict
from collections import defaultdict

class CompanyCategorizer:
    """
    Implements business logic to categorize companies based on analysis results.
    Follows the flowchart logic from the original PDF.
    """
    
    def __init__(self):
        # Scoring weights for different factors
        self.scoring_weights = {
            'is_fb': 2,
            'mentions_probiotics': 1.5,
            'health_segment': 1,  # Per segment
            'is_manufacturer': 1.5,
            'is_brand': 1,
            'is_distributor': 1
        }
        
        # Minimum scores for relevance
        self.min_scores = {
            'F&B': 2,
            'Bulk (Manufacturer)': 2.5,
            'Bulk (Distributor)': 2,
            'Formulation': 3
        }
    
    def calculate_relevance_score(self, analysis: Dict) -> float:
        """
        Calculate a relevance score (0-5) based on analysis results.
        
        Args:
            analysis: Dictionary from TextAnalyzer.analyze_text()
            
        Returns:
            Float score between 0 and 5
        """
        score = 0.0
        
        # Add points for each relevant factor
        if analysis['is_fb']:
            score += self.scoring_weights['is_fb']
        if analysis['mentions_probiotics']:
            score += self.scoring_weights['mentions_probiotics']
        
        # Add points for health segments
        score += len(analysis['health_segments']) * self.scoring_weights['health_segment']
        
        # Add points for company type
        if analysis['is_manufacturer']:
            score += self.scoring_weights['is_manufacturer']
        if analysis['is_brand']:
            score += self.scoring_weights['is_brand']
        if analysis['is_distributor']:
            score += self.scoring_weights['is_distributor']
        
        # Cap at 5
        return min(5.0, score)
    
    def determine_category(self, analysis: Dict, score: float) -> str:
        """
        Determine the company category based on analysis and score.
        
        Returns one of:
        - 'F&B'
        - 'Bulk (Manufacturer)'
        - 'Bulk (Distributor)'
        - 'Formulation'
        - 'Not Relevant'
        """
        # Rule 1: F&B companies are always prospects
        if analysis['is_fb']:
            return 'F&B'
        
        # Rule 2: Manufacturers in relevant health segments
        if analysis['is_manufacturer'] and score >= self.min_scores['Bulk (Manufacturer)']:
            return 'Bulk (Manufacturer)'
        
        # Rule 3: Distributors into nutraceuticals/probiotics
        if analysis['is_distributor'] and (analysis['mentions_probiotics'] or 
                                          'probiotics' in analysis['matched_keywords'].get('distributor', [])):
            return 'Bulk (Distributor)'
        
        # Rule 4: Brands in relevant health segments
        if analysis['is_brand'] and analysis['health_segments'] and score >= self.min_scores['Formulation']:
            return 'Formulation'
        
        return 'Not Relevant'
    
    def categorize_company(self, analysis: Dict) -> Dict:
        """
        Complete categorization of a company.
        
        Returns dictionary with:
        - category: The determined category
        - relevance_score: Calculated score
        - is_relevant: Boolean if company is relevant
        """
        score = self.calculate_relevance_score(analysis)
        category = self.determine_category(analysis, score)
        
        return {
            'category': category,
            'relevance_score': round(score, 2),
            'is_relevant': category != 'Not Relevant',
            'health_segments': ', '.join(analysis['health_segments'].keys()) or 'None'
        }