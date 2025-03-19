import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import traceback
import sys

class CovidDataProcessor:
    def __init__(self):
        self.data = None
        self.country_data = None
        self.debug_info = []  # Store debug information
        
    def log_debug(self, message):
        """Add debug message and print it"""
        self.debug_info.append(message)
        print(f"DEBUG: {message}")
        
    def load_data(self):
        """Load COVID-19 data from JHU CSSE GitHub repository"""
        try:
            self.log_debug("Starting to load data")
            url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
            
            # Load the data
            self.data = pd.read_csv(url)
            self.log_debug(f"Data loaded successfully. Shape: {self.data.shape}")
            self.log_debug(f"Columns: {list(self.data.columns[:10])}...")
            
            # Process the data right away
            processed_data = self.process_data()
            self.log_debug("Data processed successfully")
            
            return processed_data
            
        except Exception as e:
            error_info = traceback.format_exc()
            self.log_debug(f"Error loading data: {str(e)}\n{error_info}")
            raise Exception(f"Error loading data: {str(e)}")
            
    def process_data(self):
        """Process and transform the raw data"""
        try:
            if self.data is None:
                self.log_debug("No data to process")
                raise ValueError("No data to process. Please load data first.")
                
            self.log_debug("Starting data processing")
            
            # Create a copy of the data
            df = self.data.copy()
            self.log_debug(f"Original data columns: {list(df.columns[:10])}...")
            
            # Identify date columns (all columns after the 4th column)
            date_columns = df.columns[4:]
            self.log_debug(f"Identified {len(date_columns)} date columns")
            
            # Melt the dataframe to convert dates from columns to rows
            self.log_debug("Melting dataframe...")
            melted_df = df.melt(
                id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                value_vars=date_columns,
                var_name='Date', 
                value_name='Confirmed'
            )
            self.log_debug(f"Melted dataframe shape: {melted_df.shape}")
            self.log_debug(f"Melted dataframe columns: {list(melted_df.columns)}")
            
            # Verify Date column exists after melting
            if 'Date' not in melted_df.columns:
                self.log_debug("Date column missing after melting!")
                raise ValueError("Date column is missing after melting operation")
                
            # Convert date strings to datetime objects
            self.log_debug("Converting dates to datetime objects")
            melted_df['Date'] = pd.to_datetime(melted_df['Date'], errors='coerce')
            
            # Check for NaT values after conversion
            nat_count = melted_df['Date'].isna().sum()
            self.log_debug(f"NaT values after date conversion: {nat_count}")
            
            if nat_count > 0:
                # If there are NaT values, try an alternative parsing approach
                self.log_debug("Trying alternative date parsing")
                melted_df['Date'] = pd.to_datetime(melted_df['Date'], format='%m/%d/%y', errors='coerce')
                nat_count = melted_df['Date'].isna().sum()
                self.log_debug(f"NaT values after alternative date parsing: {nat_count}")
            
            # Group by country and date, summing the confirmed cases
            self.log_debug("Grouping by country and date")
            country_data = melted_df.groupby(['Country/Region', 'Date'])['Confirmed'].sum().reset_index()
            self.log_debug(f"Country data shape after grouping: {country_data.shape}")
            self.log_debug(f"Country data columns: {list(country_data.columns)}")
            
            # Verify Date column exists after grouping
            if 'Date' not in country_data.columns:
                self.log_debug("Date column missing after grouping!")
                raise ValueError("Date column is missing after grouping operation")
            
            # Calculate daily new cases
            self.log_debug("Calculating daily new cases")
            country_data['Daily_New'] = country_data.groupby('Country/Region')['Confirmed'].diff().fillna(0)
            
            # Replace negative values with 0
            country_data['Daily_New'] = country_data['Daily_New'].clip(lower=0)
            
            # Calculate 7-day moving average
            self.log_debug("Calculating 7-day moving average")
            country_data['Seven_Day_Average'] = country_data.groupby('Country/Region')['Daily_New']\
                .rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
            
            # Final check for Date column
            if 'Date' not in country_data.columns:
                self.log_debug("Date column missing in final data!")
                raise ValueError("Date column is missing from the final processed data")
                
            # Store processed data
            self.country_data = country_data.copy()
            self.log_debug(f"Final country data shape: {self.country_data.shape}")
            self.log_debug(f"Final country data columns: {list(self.country_data.columns)}")
            
            # Ensure country_data is not empty
            if self.country_data.empty:
                self.log_debug("Warning: country_data is empty")
            
            return self.country_data
            
        except Exception as e:
            error_info = traceback.format_exc()
            self.log_debug(f"Error in process_data: {str(e)}\n{error_info}")
            raise
            
    def get_country_list(self):
        """Return sorted list of countries"""
        try:
            if self.data is None:
                self.log_debug("Data not loaded for get_country_list")
                return []
                
            countries = sorted(self.data['Country/Region'].unique())
            self.log_debug(f"Found {len(countries)} countries")
            return countries
            
        except Exception as e:
            self.log_debug(f"Error in get_country_list: {str(e)}")
            return []
            
    def filter_data(self, country, start_date, end_date):
        """Filter data by country and date range"""
        try:
            self.log_debug(f"Filter request - Country: {country}, Start: {start_date}, End: {end_date}")
            
            # Ensure we have processed data
            if self.country_data is None:
                self.log_debug("country_data is None in filter_data")
                self.log_debug("Attempting to process data")
                
                if self.data is not None:
                    self.process_data()
                else:
                    self.log_debug("No data loaded to process")
                    raise ValueError("No data loaded. Please load data first.")
                    
                if self.country_data is None:
                    self.log_debug("country_data still None after processing")
                    raise ValueError("Data processing failed. country_data is still None.")
            
            # Make a copy to avoid SettingWithCopyWarning
            filtered_data = self.country_data.copy()
            
            # Debug country_data state
            self.log_debug(f"country_data shape: {self.country_data.shape}")
            self.log_debug(f"country_data columns: {list(self.country_data.columns)}")
            
            # Verify the Date column exists
            if 'Date' not in filtered_data.columns:
                self.log_debug(f"Date column missing in filter_data! Available columns: {list(filtered_data.columns)}")
                raise ValueError("Date column is missing from the processed data.")
            
            # Filter by country
            filtered_data = filtered_data[filtered_data['Country/Region'] == country]
            self.log_debug(f"After country filter, shape: {filtered_data.shape}")
            
            # Check if filtered data is empty
            if filtered_data.empty:
                self.log_debug(f"No data found for country: {country}")
                return filtered_data
            
            # Filter by date range
            filtered_data = filtered_data[
                (filtered_data['Date'] >= pd.to_datetime(start_date)) & 
                (filtered_data['Date'] <= pd.to_datetime(end_date))
            ]
            
            self.log_debug(f"After date filter, shape: {filtered_data.shape}")
            
            # Confirm Date column still exists
            if 'Date' not in filtered_data.columns:
                self.log_debug("Date column lost after filtering!")
            
            return filtered_data
            
        except Exception as e:
            error_info = traceback.format_exc()
            self.log_debug(f"Error in filter_data: {str(e)}\n{error_info}")
            raise e