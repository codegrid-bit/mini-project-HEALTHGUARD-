import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
ML_DATA_DIR = BASE_DIR / 'ml_data'
MODEL_DIR = BASE_DIR / 'ml_models'

def train_improved_diabetes_model():
    """Train improved diabetes model with better feature engineering"""
    print("Training improved diabetes model...")
    
    df = pd.read_csv(ML_DATA_DIR / 'diabetes.csv')
    
    # Feature engineering - add interaction terms
    df['BMI_Age'] = df['BMI'] * df['Age']
    df['Glucose_BMI'] = df['Glucose'] * df['BMI']
    df['BP_Age'] = df['BloodPressure'] * df['Age']
    
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Apply SMOTE
    smote = SMOTE(random_state=42, sampling_strategy=0.8)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest with optimized hyperparameters
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train_resampled)
    
    # Cross-validation
    cv_scores = cross_val_score(rf_model, X_train_scaled, y_train_resampled, cv=5)
    
    # Evaluate
    train_score = rf_model.score(X_train_scaled, y_train_resampled)
    test_score = rf_model.score(X_test_scaled, y_test)
    y_pred = rf_model.predict(X_test_scaled)
    
    print(f"Diabetes Model Performance:")
    print(f"  Train Score: {train_score:.3f}")
    print(f"  Test Score: {test_score:.3f}")
    print(f"  CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Diabetes', 'Diabetes']))
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(f"\nTop 5 Important Features:")
    print(feature_importance.head())
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf_model, MODEL_DIR / 'diabetes_model_v2.pkl')
    joblib.dump(scaler, MODEL_DIR / 'diabetes_scaler_v2.pkl')
    joblib.dump(list(X.columns), MODEL_DIR / 'diabetes_features_v2.pkl')
    
    print("\n✅ Improved diabetes model saved successfully!")
    return rf_model, scaler, feature_importance

def train_improved_cholesterol_model():
    """Train improved cholesterol model"""
    print("\nTraining improved cholesterol model...")
    
    df = pd.read_csv(ML_DATA_DIR / 'cholesterol.csv')
    df['target'] = (df['num'] > 0).astype(int)
    
    # Convert string columns
    df['ca'] = pd.to_numeric(df['ca'], errors='coerce')
    df['thal'] = pd.to_numeric(df['thal'], errors='coerce')
    
    # Feature engineering
    df['age_chol'] = df['age'] * df['chol']
    df['bp_chol'] = df['trestbps'] * df['chol']
    df['age_thalach'] = df['age'] * df['thalach']
    
    feature_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                   'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal',
                   'age_chol', 'bp_chol', 'age_thalach']
    
    X = df[feature_cols]
    y = df['target']
    
    # Handle missing values
    for col in X.columns:
        if X[col].dtype in ['float64', 'int64']:
            X[col] = X[col].fillna(X[col].median())
        else:
            X[col] = X[col].fillna(0)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # SMOTE
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train_resampled)
    
    # Cross-validation
    cv_scores = cross_val_score(rf_model, X_train_scaled, y_train_resampled, cv=5)
    
    # Evaluate
    train_score = rf_model.score(X_train_scaled, y_train_resampled)
    test_score = rf_model.score(X_test_scaled, y_test)
    y_pred = rf_model.predict(X_test_scaled)
    
    print(f"Cholesterol Model Performance:")
    print(f"  Train Score: {train_score:.3f}")
    print(f"  Test Score: {test_score:.3f}")
    print(f"  CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Disease', 'Heart Disease']))
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save
    joblib.dump(rf_model, MODEL_DIR / 'cholesterol_model_v2.pkl')
    joblib.dump(scaler, MODEL_DIR / 'cholesterol_scaler_v2.pkl')
    joblib.dump(list(X.columns), MODEL_DIR / 'cholesterol_features_v2.pkl')
    
    print("\n✅ Improved cholesterol model saved successfully!")
    return rf_model, scaler

if __name__ == "__main__":
    print("=" * 60)
    print("TRAINING IMPROVED ML MODELS FOR MEDICAL-GRADE ACCURACY")
    print("=" * 60)
    train_improved_diabetes_model()
    train_improved_cholesterol_model()
    print("\n" + "=" * 60)
    print("✅ ALL MODELS TRAINED AND SAVED SUCCESSFULLY")
    print("=" * 60)
