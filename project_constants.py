# Constants and configurations for the prospecting system

# Keywords for each category
KEYWORDS = {
    'f&b': [
        'food', 'beverage', 'nutrition', 'fortif', 'milk', 'cereal', 'bake', 
        'drink', 'yogurt', 'dairy', 'juice', 'snack', 'supplement', 'functional food'
    ],
    
    'probiotics': [
        'probiotic', 'microbiome', 'gut health', 'digestive', 'lactobacillus', 
        'bifidobacterium', 'bacillus', 'ferment', 'intestinal flora', 'microbial',
        'lactic acid bacteria', 'postbiotic', 'prebiotic'
    ],
    
    'health_segments': {
        'gut_health': [
            'gut', 'digest', 'constipat', 'diarrh', 'stomach', 'intestine',
            'bowel', 'bloating', 'ibs', 'indigestion', 'gastrointestinal',
            'microbiome', 'gut-brain'
        ],
        'womens_health': [
            'women', 'female', 'pcos', 'pcod', 'uti', 'vaginal', 'yeast',
            'menstrual', 'provinorm', 'feminine', 'menopause', 'pregnancy',
            'vaginal health', 'feminine care'
        ],
        'cognitive_health': [
            'cognitive', 'mental', 'brain', 'anxiety', 'stress', 'memory',
            'focus', 'cognisol', 'mood', 'depression', 'brain health',
            'neuro', 'cognitive function'
        ],
        'sports_nutrition': [
            'sports', 'athlete', 'exercise', 'workout', 'recovery',
            'performance', 'endurance', 'muscle', 'protein', 'fitness'
        ],
        'mental_wellness': [
            'wellness', 'wellbeing', 'stress relief', 'relaxation',
            'mood support', 'calm', 'anxiety relief', 'sleep support',
            'mental health', 'emotional balance'
        ]
    },
    
    'manufacturer': [
        'manufactur', 'production', 'capacity', 'plant', 'facility',
        'certif', 'gmp', 'iso', 'production line', 'equipment',
        'contract manufacturer', 'cm(o|os)', 'private label'
    ],
    
    'brand': [
        'product', 'shop', 'buy', 'price', 'store', 'brand', 'retail',
        'consumer', 'purchase', 'order', 'branded', 'direct to consumer'
    ],
    
    'distributor': [
        'distribut', 'supplier', 'raw material', 'ingredient',
        'supply', 'wholesale', 'logistics', 'import', 'export',
        'reseller', 'channel partner', 'value-added reseller'
    ],
    
    'fortification': [
        'fortif', 'enrich', 'vitamin', 'mineral', 'added nutrient',
        'enhanced', 'plus', 'with extra', 'dha', 'omega', 'vit d',
        'vitamin d', 'iron', 'zinc', 'calcium'
    ]
}

# List of 15 diverse companies to analyze
COMPANIES = [
    {'name': 'Nestle', 'website': 'https://www.nestle.com'},
    {'name': 'Danone', 'website': 'https://www.danone.com'},
    {'name': 'Dr. Reddy\'s Laboratories', 'website': 'https://www.drreddys.com'},
    {'name': 'Abbott Nutrition', 'website': 'https://www.abbottnutrition.com'},
    {'name': 'General Mills', 'website': 'https://www.generalmills.com'},
    {'name': 'Probi AB', 'website': 'https://www.probi.com'},
    {'name': 'Chr. Hansen', 'website': 'https://www.chr-hansen.com'},
    {'name': 'Lallemand Health Solutions', 'website': 'https://www.lallemandhealthsolutions.com'},
    {'name': 'Kerry Group', 'website': 'https://www.kerrygroup.com'},
    {'name': 'Bayer Consumer Health', 'website': 'https://www.bayer.com/en/consumer-health'},
    {'name': 'Herbalife Nutrition', 'website': 'https://www.herbalife.com'},
    {'name': 'GNC', 'website': 'https://www.gnc.com'},
    {'name': 'NOW Foods', 'website': 'https://www.nowfoods.com'},
    {'name': 'Nature\'s Way', 'website': 'https://www.naturesway.com'},
    {'name': 'BioGaia', 'website': 'https://www.biogaia.com'}
]

# Request headers for web scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# Timeout settings
TIMEOUT = 15

# Scoring weights for different factors
SCORING_WEIGHTS = {
    'is_fb': 2,
    'mentions_probiotics': 1.5,
    'health_segment': 1,  # Per segment
    'is_manufacturer': 1.5,
    'is_brand': 1,
    'is_distributor': 1,
    'fortification': 0.5
}

# Minimum scores for relevance
MIN_SCORES = {
    'F&B': 2,
    'Bulk (Manufacturer)': 2.5,
    'Bulk (Distributor)': 2,
    'Formulation': 3
}