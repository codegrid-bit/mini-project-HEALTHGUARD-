import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import joblib
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
ML_DATA_DIR = BASE_DIR / 'ml_data'
MODEL_DIR = BASE_DIR / 'ml_models'

def train_diabetes_model():
    """Train Random Forest model for diabetes prediction with SMOTE"""
    print("Training diabetes model...")
    
    # Load diabetes dataset
    df = pd.read_csv(ML_DATA_DIR / 'diabetes.csv')
    
    # Separate features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Apply SMOTE to handle class imbalance
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42
    )
    rf_model.fit(X_train_scaled, y_train_resampled)
    
    # Evaluate
    train_score = rf_model.score(X_train_scaled, y_train_resampled)
    test_score = rf_model.score(X_test_scaled, y_test)
    print(f"Diabetes Model - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
    
    # Save model and scaler
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf_model, MODEL_DIR / 'diabetes_model.pkl')
    joblib.dump(scaler, MODEL_DIR / 'diabetes_scaler.pkl')
    
    # Save feature names
    feature_names = list(X.columns)
    joblib.dump(feature_names, MODEL_DIR / 'diabetes_features.pkl')
    
    print("Diabetes model saved successfully!")
    return rf_model, scaler, feature_names

def train_cholesterol_model():
    """Train Random Forest model for cholesterol/heart disease prediction with SMOTE"""
    print("Training cholesterol model...")
    
    # Load cholesterol dataset
    df = pd.read_csv(ML_DATA_DIR / 'cholesterol.csv')
    
    # Create binary target (0: no disease, 1: disease)
    df['target'] = (df['num'] > 0).astype(int)
    
    # Convert string columns to numeric
    df['ca'] = pd.to_numeric(df['ca'], errors='coerce')
    df['thal'] = pd.to_numeric(df['thal'], errors='coerce')
    
    # Select relevant features
    feature_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                   'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    X = df[feature_cols]
    y = df['target']
    
    # Handle missing values with numeric median
    for col in X.columns:
        if X[col].dtype in ['float64', 'int64']:
            X[col] = X[col].fillna(X[col].median())
        else:
            X[col] = X[col].fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Apply SMOTE
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42
    )
    rf_model.fit(X_train_scaled, y_train_resampled)
    
    # Evaluate
    train_score = rf_model.score(X_train_scaled, y_train_resampled)
    test_score = rf_model.score(X_test_scaled, y_test)
    print(f"Cholesterol Model - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
    
    # Save model and scaler
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf_model, MODEL_DIR / 'cholesterol_model.pkl')
    joblib.dump(scaler, MODEL_DIR / 'cholesterol_scaler.pkl')
    
    # Save feature names
    feature_names = list(X.columns)
    joblib.dump(feature_names, MODEL_DIR / 'cholesterol_features.pkl')
    
    print("Cholesterol model saved successfully!")
    return rf_model, scaler, feature_names

if __name__ == "__main__":
    print("Starting ML model training...")
    train_diabetes_model()
    train_cholesterol_model()
    print("All models trained and saved successfully!")
