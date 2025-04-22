import pandas as pd
import numpy as np

def process_data(df):
    """
    Process the traffic data for analysis
    - Check for missing values
    - Normalize numeric columns if needed
    - Add any derived features
    """
    # Check for missing values
    if df.isnull().sum().sum() > 0:
        print("Warning: Dataset contains missing values")
        print(df.isnull().sum())
        # Fill missing values or drop rows as appropriate
        df.fillna(method='ffill', inplace=True)
    
    # Convert time to datetime if needed
    # df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    
    # Add any derived features that might be useful
    # For example, time of day category (morning, afternoon, evening, night)
    hour_mapping = {
        'morning': (5, 12),    # 5 AM to 12 PM
        'afternoon': (12, 17), # 12 PM to 5 PM
        'evening': (17, 21),   # 5 PM to 9 PM
        'night': (21, 5)       # 9 PM to 5 AM
    }
    
    # Print summary of processed data
    print(f"Processed {len(df)} traffic data records")
    print(f"Number of unique crossings: {df['Crossing_Id'].nunique()}")
    print(f"Number of unique lanes: {df['Lane_Id'].nunique()}")
    
    return df


# This code runs when the script is executed directly
if __name__ == "__main__":
    # Read the CSV file into a DataFrame
    df = pd.read_csv("traffic1.csv")
    
    # Display the shape of the DataFrame
    print(df.shape)
    
    # Display basic information about the DataFrame
    print("\nDataFrame Info:")
    print(df.info())
    
    # Display statistical summary
    print("\nStatistical Summary:")
    print(df.describe())
    
    # Display the first 5 rows
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Process the data
    process_data(df)