import pandas as pd

def load_data(file_path: str, sheet_name: str):
    """Load data from an Excel sheet."""
    return pd.read_excel(file_path, sheet_name=sheet_name)

def clean_data(df: pd.DataFrame):
    """Clean the data by handling duplicates, missing, negative, or null values."""
    initial_shape = df.shape
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values (if any column has NaN, drop it for now)
    df = df.dropna()
    
    # Remove negative values if necessary (example: if a column 'Days' should not have negative values)
    for column in df.select_dtypes(include=['int64', 'float64']).columns:
        df = df[df[column] >= 0]
    
    cleaned_shape = df.shape
    print(f"Initial data shape: {initial_shape}, Cleaned data shape: {cleaned_shape}")
    
    return df

if __name__ == "__main__":
    file_path = r'data/rehospitalization.xlsx'
    sheet_name = 'hospitalization1'
    df = load_data(file_path, sheet_name)
    cleaned_df = clean_data(df)
    cleaned_df.to_csv(r'data/cleaned_hospitalization1.csv', index=False)
    print("END data_cleaning")