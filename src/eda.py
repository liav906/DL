import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path: str, sheet_name: str):
    """Load data from an Excel sheet."""
    return pd.read_excel(file_path, sheet_name=sheet_name)

def save_plot(fig, filename):
    """Save the plot to the specified filename."""
    output_dir = 'eda'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig.savefig(os.path.join(output_dir, filename))
    plt.close(fig)

def visualize_data_quality(df: pd.DataFrame, stage: str):
    """Visualize data quality to show missing, duplicated, and invalid data."""
    missing_data = df.isnull().mean() * 100  # Percentage of missing values
    duplicated_data = df.duplicated().mean() * 100  # Percentage of duplicated rows
    negative_data = (df.select_dtypes(include=['int64', 'float64']) < 0).mean() * 100  # Percentage of negative values in numeric columns

    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    missing_data.plot(kind='bar', ax=ax[0], color='skyblue')
    ax[0].set_title(f'Missing Data Percentage ({stage})')
    ax[0].set_ylabel('Percentage')

    ax[1].bar(['Duplicated Rows'], [duplicated_data], color='orange')
    ax[1].set_title(f'Duplicated Data Percentage ({stage})')
    ax[1].set_ylabel('Percentage')

    negative_data.plot(kind='bar', ax=ax[2], color='lightgreen')
    ax[2].set_title(f'Negative Data Percentage ({stage})')
    ax[2].set_ylabel('Percentage')

    plt.tight_layout()
    save_plot(fig, f'data_quality_{stage}.png')

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

def perform_eda(df: pd.DataFrame):
    """Perform exploratory data analysis."""
    print("Basic Statistics:\n", df.describe())
    print("Data Info:\n", df.info())
    
    # Save basic statistics to a CSV file
    df.describe().to_csv('eda/basic_statistics.csv')

    # Plot distributions for each numeric column
    for column in df.select_dtypes(include=['int64', 'float64']).columns:
        fig = plt.figure()
        sns.histplot(df[column], kde=True)
        plt.title(f'Distribution of {column}')
        save_plot(fig, f'distribution_{column}.png')
    
    # Compute and plot correlations only for numeric columns
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    if not numeric_df.empty:
        fig = plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f")
        plt.title('Correlation Matrix')
        save_plot(fig, 'correlation_matrix.png')
    else:
        print("No numeric data available to compute correlations.")

if __name__ == "__main__":
    file_path = r'data/rehospitalization.xlsx'
    sheet_name = 'erBeforeHospitalization2'
    df = load_data(file_path, sheet_name)

    # Visualize data quality before cleaning
    visualize_data_quality(df, stage='before_cleaning')

    # Clean the data
    cleaned_df = clean_data(df)

    # Visualize data quality after cleaning
    visualize_data_quality(cleaned_df, stage='after_cleaning')

    # Perform EDA on cleaned data
    perform_eda(cleaned_df)

    print("END eda")