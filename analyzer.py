import re
from typing import Dict, List
from collections import defaultdict

from project_constants import HEADERS, TIMEOUT, KEYWORDS

class TextAnalyzer:
    """
    Analyzes scraped text content to identify relevant keywords and patterns.
    Implements text cleaning, keyword matching, and health segment detection.
    """
    
    def __init__(self):
        self._compile_keyword_patterns()
        
    def _compile_keyword_patterns(self):
        """Pre-compile regex patterns for faster matching"""
        self.compiled_patterns = {}
        
        for category, keywords in KEYWORDS.items():
            if isinstance(keywords, dict):  # Health segments
                for segment, seg_keywords in keywords.items():
                    pattern = re.compile(r'\b(?:' + '|'.join(seg_keywords) + r')\b', re.IGNORECASE)
                    self.compiled_patterns[f"{category}_{segment}"] = pattern
            else:
                pattern = re.compile(r'\b(?:' + '|'.join(keywords) + r')\b', re.IGNORECASE)
                self.compiled_patterns[category] = pattern
    
    def clean_text(self, text: str) -> str:
        """Normalize and clean text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase and remove special chars
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def find_keywords(self, text: str, category: str) -> List[str]:
        """
        Find matching keywords in text for a given category.
        
        Args:
            text: Text to analyze
            category: One of 'f&b', 'probiotics', 'manufacturer', 'brand', 'distributor'
            
        Returns:
            List of matched keywords
        """
        text = self.clean_text(text)
        if category not in self.compiled_patterns:
            return []
        
        matches = self.compiled_patterns[category].findall(text)
        return list(set(matches))  # Return unique matches
    
    def detect_health_segments(self, text: str) -> Dict[str, List[str]]:
        """
        Detect which health segments are mentioned in the text.
        
        Returns:
            Dictionary with segment names as keys and lists of matched keywords as values
        """
        text = self.clean_text(text)
        segments = {}
        
        for segment in KEYWORDS['health_segments'].keys():
            pattern_key = f"health_segments_{segment}"
            matches = self.compiled_patterns[pattern_key].findall(text)
            if matches:
                segments[segment] = list(set(matches))
        
        return segments
    
    def analyze_text(self, text: str) -> Dict:
        """
        Perform complete text analysis for all categories.
        
        Returns:
            Dictionary with analysis results including:
            - is_fb: Boolean if F&B company
            - mentions_probiotics: Boolean if probiotics mentioned
            - health_segments: Detected health segments
            - is_manufacturer: Boolean if manufacturer
            - is_brand: Boolean if brand
            - is_distributor: Boolean if distributor
        """
        analysis = {
            'is_fb': False,
            'mentions_probiotics': False,
            'health_segments': {},
            'is_manufacturer': False,
            'is_brand': False,
            'is_distributor': False,
            'matched_keywords': defaultdict(list)
        }
        
        if not text:
            return analysis
        
        # Check each category
        for category in ['f&b', 'probiotics', 'manufacturer', 'brand', 'distributor']:
            matches = self.find_keywords(text, category)
            if matches:
                analysis['matched_keywords'][category] = matches
                
                # Set flags for important categories
                if category == 'f&b':
                    analysis['is_fb'] = True
                elif category == 'probiotics':
                    analysis['mentions_probiotics'] = True
                elif category == 'manufacturer':
                    analysis['is_manufacturer'] = True
                elif category == 'brand':
                    analysis['is_brand'] = True
                elif category == 'distributor':
                    analysis['is_distributor'] = True
        
        # Detect health segments
        analysis['health_segments'] = self.detect_health_segments(text)
        
        return analysis