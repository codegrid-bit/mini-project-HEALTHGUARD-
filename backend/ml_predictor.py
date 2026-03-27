import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Tuple

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / 'ml_models'

class MLPredictor:
    def __init__(self):
        self.diabetes_model = None
        self.diabetes_scaler = None
        self.cholesterol_model = None
        self.cholesterol_scaler = None
        self.load_models()
    
    def load_models(self):
        """Load trained models and scalers"""
        try:
            self.diabetes_model = joblib.load(MODEL_DIR / 'diabetes_model.pkl')
            self.diabetes_scaler = joblib.load(MODEL_DIR / 'diabetes_scaler.pkl')
            self.cholesterol_model = joblib.load(MODEL_DIR / 'cholesterol_model.pkl')
            self.cholesterol_scaler = joblib.load(MODEL_DIR / 'cholesterol_scaler.pkl')
            print("ML models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def predict_diabetes_risk(self, features: Dict) -> Tuple[int, float, str]:
        """Predict diabetes risk from quiz answers"""
        # Map quiz answers to model features
        # Expected features: Pregnancies, Glucose, BloodPressure, SkinThickness, 
        # Insulin, BMI, DiabetesPedigreeFunction, Age
        
        feature_vector = [
            features.get('pregnancies', 0),
            features.get('glucose', 100),
            features.get('blood_pressure', 70),
            features.get('skin_thickness', 20),
            features.get('insulin', 80),
            features.get('bmi', 25),
            features.get('diabetes_pedigree', 0.5),
            features.get('age', 30)
        ]
        
        # Scale features
        X = np.array(feature_vector).reshape(1, -1)
        X_scaled = self.diabetes_scaler.transform(X)
        
        # Predict
        prediction = self.diabetes_model.predict(X_scaled)[0]
        probability = self.diabetes_model.predict_proba(X_scaled)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return int(prediction), float(probability), risk_level
    
    def predict_cholesterol_risk(self, features: Dict) -> Tuple[int, float, str]:
        """Predict cholesterol/heart disease risk"""
        # Expected features: age, sex, cp, trestbps, chol, fbs, 
        # restecg, thalach, exang, oldpeak, slope, ca, thal
        
        feature_vector = [
            features.get('age', 30),
            features.get('sex', 1),
            features.get('cp', 0),
            features.get('trestbps', 120),
            features.get('chol', 200),
            features.get('fbs', 0),
            features.get('restecg', 0),
            features.get('thalach', 150),
            features.get('exang', 0),
            features.get('oldpeak', 0),
            features.get('slope', 1),
            features.get('ca', 0),
            features.get('thal', 2)
        ]
        
        # Scale features
        X = np.array(feature_vector).reshape(1, -1)
        X_scaled = self.cholesterol_scaler.transform(X)
        
        # Predict
        prediction = self.cholesterol_model.predict(X_scaled)[0]
        probability = self.cholesterol_model.predict_proba(X_scaled)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return int(prediction), float(probability), risk_level
    
    def calculate_combined_risk(self, diabetes_prob: float, cholesterol_prob: float) -> Tuple[int, str]:
        """Calculate combined risk score from both predictions"""
        # Combined score (0-100)
        combined_score = int((diabetes_prob + cholesterol_prob) / 2 * 100)
        
        # Determine overall risk level
        if combined_score < 30:
            risk_level = "Low"
        elif combined_score < 60:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return combined_score, risk_level

predictor = MLPredictor()
