import pandas as pd


class DataProcessor:
    def __init__(self, raw_data_path):
        self.df = pd.read_csv(raw_data_path)
    
    def clean_data(self):
        # Convert earnings to numeric
        self.df['earnings'] = pd.to_numeric(self.df['Earnings_USD'], errors='coerce')
        
        # Fill missing experience with 'Unknown'
        self.df['experience'] = self.df['Experience_Level'].fillna('Unknown')
        
        return self.df
    
    def create_analytics_tables(self):
        # Create analytics tables
        region_stats = self.df.groupby('Client_Region')['earnings'].describe()
        crypto_stats = self.df[self.df['Payment_Method'] == 'Crypto']
        return {
            'region_stats': region_stats,
            'crypto_comparison': crypto_stats
        }
