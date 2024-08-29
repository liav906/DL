import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from data_fix import clean_data

def load_data(file_path: str, sheet_name: str):
    """Load data from an Excel sheet."""
    return pd.read_excel(file_path, sheet_name=sheet_name)

def preprocess_data(df: pd.DataFrame):
    """Preprocess data for deep learning model."""
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df_normalized

def build_model(input_shape):
    """Build a simple neural network model."""
    model = Sequential([
        Dense(64, activation='relu', input_shape=input_shape),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, X, y):
    """Train the deep learning model."""
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

if __name__ == "__main__":
    file_path = r'/Users/liav/Desktop/GIT/DL_Final/DL_Final/data/rehospitalization.xlsx'
    sheet_name = 'hospitalization2'
    df = load_data(file_path, sheet_name)
    
    # Clean the data
    cleaned_df = clean_data(df)
    
    # Preprocess the cleaned data
    df_normalized = preprocess_data(cleaned_df[['Number of Days']])
    model = build_model((df_normalized.shape[1],))
    train_model(model, df_normalized.drop('Number of Days', axis=1), df_normalized['Number of Days'])