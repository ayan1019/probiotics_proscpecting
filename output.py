import pandas as pd
from typing import List, Dict
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

class ReportGenerator:
    """
    Handles generation of Excel reports with formatted output.
    Implements conditional formatting and professional styling.
    """
    
    def __init__(self, output_path: str = 'probiotics_prospects.xlsx'):
        self.output_path = output_path
    
    def create_dataframe(self, companies: List[Dict], scraped_data: Dict, analysis_results: Dict) -> pd.DataFrame:
        """
        Combine all data into a structured DataFrame.
        
        Args:
            companies: Original list of companies
            scraped_data: Scraped website data
            analysis_results: Categorization results
            
        Returns:
            pandas DataFrame with all relevant information
        """
        rows = []
        
        for company in companies:
            name = company['name']
            website = company['website']
            
            scraped = scraped_data.get(name, {})
            analysis = analysis_results.get(name, {})
            
            row = {
                'Company Name': name,
                'Website': website,
                'Website Accessible': scraped.get('status', '') == 'success',
                'Category': analysis.get('category', ''),
                'Relevance Score': analysis.get('relevance_score', 0),
                'Is F&B': analysis.get('is_fb', False),
                'Mentions Probiotics': analysis.get('mentions_probiotics', False),
                'Health Segments': analysis.get('health_segments', 'None'),
                'Is Manufacturer': analysis.get('is_manufacturer', False),
                'Is Brand': analysis.get('is_brand', False),
                'Is Distributor': analysis.get('is_distributor', False),
                'Scraping Status': scraped.get('status', 'unknown')
            }
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def generate_excel_report(self, df: pd.DataFrame):
        """
        Generate formatted Excel report with conditional formatting.
        
        Args:
            df: DataFrame with analysis results
        """
        # Create Excel writer
        writer = pd.ExcelWriter(self.output_path, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Prospects')
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Prospects']
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        # Score formats
        score_format_high = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        score_format_med = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C6500'})
        score_format_low = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        
        # Boolean formats
        true_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        false_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        
        # Apply header formatting
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Set column widths
        worksheet.set_column('A:A', 25)  # Company Name
        worksheet.set_column('B:B', 30)  # Website
        worksheet.set_column('C:C', 18)  # Website Accessible
        worksheet.set_column('D:D', 20)  # Category
        worksheet.set_column('E:E', 15)  # Relevance Score
        worksheet.set_column('F:F', 10)  # Is F&B
        worksheet.set_column('G:G', 18)  # Mentions Probiotics
        worksheet.set_column('H:H', 25)  # Health Segments
        worksheet.set_column('I:I', 15)  # Is Manufacturer
        worksheet.set_column('J:J', 10)  # Is Brand
        worksheet.set_column('K:K', 15)  # Is Distributor
        worksheet.set_column('L:L', 30)  # Scraping Status
        
        # Apply conditional formatting
        # Relevance Score
        worksheet.conditional_format('E2:E100', {
            'type': 'cell',
            'criteria': '>=',
            'value': 3.5,
            'format': score_format_high
        })
        worksheet.conditional_format('E2:E100', {
            'type': 'cell',
            'criteria': 'between',
            'minimum': 2,
            'maximum': 3.49,
            'format': score_format_med
        })
        worksheet.conditional_format('E2:E100', {
            'type': 'cell',
            'criteria': '<',
            'value': 2,
            'format': score_format_low
        })
        
        # Boolean columns
        for col in ['F', 'G', 'I', 'J', 'K']:
            col_letter = col
            range_start = xl_rowcol_to_cell(1, ord(col) - ord('A'))
            range_end = xl_rowcol_to_cell(100, ord(col) - ord('A'))
            
            worksheet.conditional_format(f'{range_start}:{range_end}', {
                'type': 'formula',
                'criteria': '=INDIRECT("RC", FALSE)=TRUE',
                'format': true_format
            })
            worksheet.conditional_format(f'{range_start}:{range_end}', {
                'type': 'formula',
                'criteria': '=INDIRECT("RC", FALSE)=FALSE',
                'format': false_format
            })
        
        # Add autofilter
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
        
        # Freeze header row
        worksheet.freeze_panes(1, 0)
        
        # Save the Excel file
        writer.close()