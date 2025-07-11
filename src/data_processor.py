import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from typing import List, Dict, Optional, Tuple

class DataProcessor:
    """
    Handles data loading, cleaning, and preprocessing for earthquake data.
    """
    
    def __init__(self, data_path: str = "."):
        self.data_path = data_path
        self.earthquake_data = None
        self.processed_data = None
        
        # Load data
        self.load_data()
    
    def load_data(self):
        """Load earthquake data from CSV files."""
        try:
            # Load the main earthquake dataset
            main_file = os.path.join(self.data_path, "Significant Earthquake Dataset 1900-2023.csv")
            if os.path.exists(main_file):
                self.earthquake_data = pd.read_csv(main_file)
                print(f"Loaded {len(self.earthquake_data)} earthquake records")
                self._preprocess_data()
            else:
                print("Earthquake dataset not found.")
                self.earthquake_data = pd.DataFrame()
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.earthquake_data = pd.DataFrame()
    
    def _preprocess_data(self):
        """Clean and preprocess the earthquake data."""
        if self.earthquake_data is None or self.earthquake_data.empty:
            return
        
        # Create a copy for processing
        self.processed_data = self.earthquake_data.copy()
        
        # Convert time column to datetime
        if 'Time' in self.processed_data.columns:
            self.processed_data['time'] = pd.to_datetime(self.processed_data['Time'])
        
        # Handle missing values
        if 'Mag' in self.processed_data.columns:
            self.processed_data['mag'] = self.processed_data['Mag']
        if 'Depth' in self.processed_data.columns:
            self.processed_data['depth'] = self.processed_data['Depth']
        
        # Fill missing values
        self.processed_data['mag'].fillna(self.processed_data['mag'].median(), inplace=True)
        self.processed_data['depth'].fillna(self.processed_data['depth'].median(), inplace=True)
        
        # Add derived columns
        self.processed_data['year'] = self.processed_data['time'].dt.year
        self.processed_data['month'] = self.processed_data['time'].dt.month
        self.processed_data['day'] = self.processed_data['time'].dt.day
        
        # Add magnitude categories
        self.processed_data['magnitude_category'] = pd.cut(
            self.processed_data['mag'],
            bins=[0, 4, 6, 7, 10],
            labels=['Minor', 'Moderate', 'Strong', 'Major'],
            include_lowest=True
        )
        
        # Extract country from place
        def extract_country(place):
            if not isinstance(place, str):
                return None
            if ',' in place:
                return place.split(',')[-1].strip()
            
            # Manual mapping for known named earthquakes
            place_lower = place.lower()
            if "assam" in place_lower or "tibet" in place_lower:
                return "India"
            elif "ecuador" in place_lower:
                return "Ecuador"
            elif "valdivia" in place_lower or "chilean" in place_lower:
                return "Chile"
            elif "sumatra" in place_lower or "andaman" in place_lower:
                return "Indonesia"
            
            return None  # Or "Unknown"
        self.processed_data['country'] = self.processed_data['Place'].apply(extract_country)

        
        # Filter out invalid coordinates
        self.processed_data = self.processed_data[
            (self.processed_data['Latitude'].between(-90, 90)) &
            (self.processed_data['Longitude'].between(-180, 180))
        ]
        
        print(f"Preprocessed {len(self.processed_data)} earthquake records")
    
    def get_filtered_data(self, 
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         magnitude_range: Optional[Tuple[float, float]] = None,
                         country: Optional[str] = None) -> pd.DataFrame:
        """Get filtered earthquake data based on criteria."""
        if self.processed_data is None or self.processed_data.empty:
            return pd.DataFrame()
        
        data = self.processed_data.copy()
        
        # Filter by date range
        if start_date:
            data = data[data['time'] >= pd.to_datetime(start_date)]
        if end_date:
            data = data[data['time'] <= pd.to_datetime(end_date)]
        
        # Filter by magnitude range
        if magnitude_range:
            data = data[data['mag'].between(magnitude_range[0], magnitude_range[1])]
        
        # Filter by country
        if country and country != 'all':
            data = data[data['country'].str.contains(country, case=False, na=False)]
        
        return data
    
    def get_countries(self) -> List[str]:
        """Get list of unique countries in the dataset."""
        if self.processed_data is None or self.processed_data.empty:
            return []
        
        countries = self.processed_data['country'].dropna().unique()
        return sorted([c.strip() for c in countries if c.strip()])
    
    def get_significant_earthquakes(self) -> List[Dict]:
        """Get list of significant earthquakes for impact analysis."""
        if self.processed_data is None or self.processed_data.empty:
            return []
        
        # Get earthquakes with magnitude >= 6.0
        significant = self.processed_data[
            self.processed_data['mag'] >= 6.0
        ].copy()
        
        # Sort by magnitude
        significant = significant.sort_values('mag', ascending=False)
        
        # Convert to list of dictionaries
        return significant.head(100).to_dict('records')
    
    def get_time_series_data(self, 
                            magnitude_filter: str = 'all',
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            country: Optional[str] = None) -> pd.DataFrame:
        """Get time series data for plotting."""
        data = self.get_filtered_data(start_date, end_date, country=country)
        
        if data.empty:
            return pd.DataFrame()
        
        # Apply magnitude filter
        if magnitude_filter == 'minor':
            data = data[data['mag'] < 4.0]
        elif magnitude_filter == 'moderate':
            data = data[data['mag'].between(4.0, 5.9)]
        elif magnitude_filter == 'strong':
            data = data[data['mag'].between(6.0, 6.9)]
        elif magnitude_filter == 'major':
            data = data[data['mag'] >= 7.0]
        
        # Group by year and month
        data['year_month'] = data['time'].dt.to_period('M')
        time_series = data.groupby('year_month').agg({
            'ID': 'count',
            'mag': ['mean', 'max'],
            'depth': 'mean'
        }).reset_index()
        
        time_series.columns = ['year_month', 'count', 'avg_magnitude', 'max_magnitude', 'avg_depth']
        time_series['date'] = time_series['year_month'].dt.to_timestamp()
        
        return time_series
    
    def get_country_statistics(self, country: str) -> Dict:
        """Get statistics for a specific country."""
        if self.processed_data is None or self.processed_data.empty:
            return {}
        
        country_data = self.processed_data[
            self.processed_data['country'].str.contains(country, case=False, na=False)
        ]
        
        if country_data.empty:
            return {}
        
        return {
            'total_earthquakes': len(country_data),
            'avg_magnitude': country_data['mag'].mean(),
            'max_magnitude': country_data['mag'].max(),
            'avg_depth': country_data['depth'].mean(),
            'date_range': {
                'start': country_data['time'].min().strftime('%Y-%m-%d'),
                'end': country_data['time'].max().strftime('%Y-%m-%d')
            }
        }
    
    def get_risk_map_data(self, metric: str = 'count') -> pd.DataFrame:
        """Get data for the global risk map."""
        if self.processed_data is None or self.processed_data.empty:
            return pd.DataFrame()
        
        # Group by country
        risk_data = self.processed_data.groupby('country').agg({
            'ID': 'count',
            'mag': ['mean', 'max']
        }).reset_index()
        
        risk_data.columns = ['country', 'count', 'avg_magnitude', 'max_magnitude']
        
        # Select the metric to display
        if metric == 'count':
            risk_data['value'] = risk_data['count']
        elif metric == 'avg_magnitude':
            risk_data['value'] = risk_data['avg_magnitude']
        elif metric == 'max_magnitude':
            risk_data['value'] = risk_data['max_magnitude']
        
        return risk_data
    
    def save_processed_data(self, filename: str = "processed_earthquakes.csv"):
        """Save processed data to CSV file."""
        if self.processed_data is not None:
            filepath = os.path.join(self.data_path, filename)
            self.processed_data.to_csv(filepath, index=False)
            print(f"Processed data saved to {filepath}") 