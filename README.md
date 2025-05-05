# Probiotics Company Prospecting Tool

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Project Structure

| File/Folder            | Purpose |
|------------------------|---------|
| `main.py`              | Main execution script |
| `scraper.py`           | Website scraping functionality |
| `analyzer.py`          | Processes scraped text and identifies keywords |
| `categorizer.py`       | Implements business logic for company classification |
| `output.py`            | Generates formatted Excel reports |
| `project_constants.py` | Contains all configurable parameters and keywords |




A data-driven solution to identify potential customers for probiotic products by analyzing company websites and categorizing them based on relevant business segments.

## Features

- **Web Scraping**: Automatically extracts company information from websites
- **Intelligent Categorization**: Classifies companies into:
  - Food & Beverage (F&B)
  - Bulk Manufacturers
  - Finished Formulations
  - Distributors
- **Health Segment Analysis**: Identifies focus on:
  - Gut Health
  - Women's Health  
  - Cognitive Health
  - Sports Nutrition
  - Mental Wellness
- **Relevance Scoring**: Rates companies 0-5 based on probiotic potential
- **Excel Reporting**: Generates formatted reports with color-coded results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/probiotics-prospecting.git
cd probiotics-prospecting
