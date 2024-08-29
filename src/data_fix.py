import pandas as pd

def clean_data(df: pd.DataFrame):
    """Clean the data by handling duplicates, missing, negative, or null values."""
    initial_shape = df.shape
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values (e.g., drop rows with NaN values)
    df = df.dropna()
    
    # Remove negative values in numeric columns
    for column in df.select_dtypes(include=['int64', 'float64']).columns:
        df = df[df[column] >= 0]
    
    cleaned_shape = df.shape
    print(f"Initial data shape: {initial_shape}, Cleaned data shape: {cleaned_shape}")
    
    return df