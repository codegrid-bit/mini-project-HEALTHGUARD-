import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List
import os

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / 'ml_models'

class EnhancedMLPredictor:
    def __init__(self):
        self.diabetes_model = None
        self.diabetes_scaler = None
        self.diabetes_features = None
        self.cholesterol_model = None
        self.cholesterol_scaler = None
        self.cholesterol_features = None
        self.load_models()
    
    def load_models(self):
        """Load trained v2 models"""
        try:
            # Try loading v2 models first
            if os.path.exists(MODEL_DIR / 'diabetes_model_v2.pkl'):
                self.diabetes_model = joblib.load(MODEL_DIR / 'diabetes_model_v2.pkl')
                self.diabetes_scaler = joblib.load(MODEL_DIR / 'diabetes_scaler_v2.pkl')
                self.diabetes_features = joblib.load(MODEL_DIR / 'diabetes_features_v2.pkl')
                print("✅ Loaded improved diabetes model (v2)")
            else:
                # Fallback to v1
                self.diabetes_model = joblib.load(MODEL_DIR / 'diabetes_model.pkl')
                self.diabetes_scaler = joblib.load(MODEL_DIR / 'diabetes_scaler.pkl')
                self.diabetes_features = joblib.load(MODEL_DIR / 'diabetes_features.pkl')
                print("⚠️ Using original diabetes model (v1)")
            
            if os.path.exists(MODEL_DIR / 'cholesterol_model_v2.pkl'):
                self.cholesterol_model = joblib.load(MODEL_DIR / 'cholesterol_model_v2.pkl')
                self.cholesterol_scaler = joblib.load(MODEL_DIR / 'cholesterol_scaler_v2.pkl')
                self.cholesterol_features = joblib.load(MODEL_DIR / 'cholesterol_features_v2.pkl')
                print("✅ Loaded improved cholesterol model (v2)")
            else:
                self.cholesterol_model = joblib.load(MODEL_DIR / 'cholesterol_model.pkl')
                self.cholesterol_scaler = joblib.load(MODEL_DIR / 'cholesterol_scaler.pkl')
                self.cholesterol_features = joblib.load(MODEL_DIR / 'cholesterol_features.pkl')
                print("⚠️ Using original cholesterol model (v1)")
                
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def map_quiz_to_diabetes_features(self, quiz_answers: Dict, user_info: Dict) -> Dict:
        """Map quiz answers to diabetes ML model features"""
        # Extract user demographics
        age = user_info.get('age', 30)
        sex = 1 if user_info.get('sex', 'male') == 'female' else 0
        
        # Calculate risk scores from quiz
        diabetes_risk_score = 0
        max_diabetes_score = 0
        
        # Weight-based calculation from quiz
        from quiz_questions import QUIZ_QUESTIONS
        for q in QUIZ_QUESTIONS:
            if q['category'] == 'diabetes':
                max_diabetes_score += q['weight']
                if quiz_answers.get(q['id']) is True:
                    diabetes_risk_score += q['weight']
        
        # Normalize to percentage
        diabetes_percentage = (diabetes_risk_score / max_diabetes_score * 100) if max_diabetes_score > 0 else 0
        
        # Map to model features (Pima diabetes dataset features)
        # Estimate values based on quiz responses and demographics
        
        # Pregnancies (for women, estimate based on age)
        pregnancies = 0
        if sex == 1 and age > 25:
            pregnancies = min(int((age - 25) / 10), 4)  # Rough estimate
        
        # Glucose (estimate from diabetes symptoms)
        glucose = 100  # baseline
        if quiz_answers.get('d1') or quiz_answers.get('d2'):  # thirst, urination
            glucose += 30
        if quiz_answers.get('d3'):  # weight loss
            glucose += 20
        if quiz_answers.get('d8'):  # dark patches
            glucose += 40
        glucose = min(glucose, 200)
        
        # Blood Pressure (estimate from risk factors)
        blood_pressure = 70
        if quiz_answers.get('d13'):  # high BP history
            blood_pressure = 85
        if quiz_answers.get('d10'):  # overweight
            blood_pressure += 10
        
        # Skin Thickness (fixed estimate)
        skin_thickness = 20
        
        # Insulin (estimate from diabetes signs)
        insulin = 80
        if quiz_answers.get('d4') or quiz_answers.get('d6'):  # blurry vision, fatigue
            insulin = 120
        
        # BMI (estimate from self-reported weight status)
        bmi = 25
        if quiz_answers.get('d10'):  # BMI > 25
            bmi = 32
        
        # Diabetes Pedigree Function (family history)
        dpf = 0.3
        if quiz_answers.get('d11'):  # family history
            dpf = 0.8
        if quiz_answers.get('d14') or quiz_answers.get('d15'):  # gestational/PCOS
            dpf += 0.3
        
        features = {
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': blood_pressure,
            'SkinThickness': skin_thickness,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': min(dpf, 2.0),
            'Age': age
        }
        
        # Add interaction terms if model has them
        if 'BMI_Age' in self.diabetes_features:
            features['BMI_Age'] = bmi * age
            features['Glucose_BMI'] = glucose * bmi
            features['BP_Age'] = blood_pressure * age
        
        return features
    
    def map_quiz_to_cholesterol_features(self, quiz_answers: Dict, user_info: Dict) -> Dict:
        """Map quiz answers to cholesterol ML model features"""
        age = user_info.get('age', 30)
        sex = 1 if user_info.get('sex', 'male') == 'male' else 0
        
        # Chest pain type (0-3)
        cp = 0
        if quiz_answers.get('c6'):  # chest pain during exertion
            cp = 2
        
        # Resting blood pressure
        trestbps = 120
        if quiz_answers.get('c9'):  # high BP
            trestbps = 145
        if quiz_answers.get('c8'):  # large waist
            trestbps += 10
        
        # Cholesterol estimate
        chol = 200
        if quiz_answers.get('c2') or quiz_answers.get('c3'):  # xanthelasma, wrist bumps
            chol = 280
        if quiz_answers.get('c7'):  # high fat diet
            chol += 30
        if quiz_answers.get('c1'):  # family history
            chol += 20
        
        # Fasting blood sugar
        fbs = 0
        if quiz_answers.get('d1') or quiz_answers.get('d2'):  # diabetes symptoms
            fbs = 1
        
        # Resting ECG (0-2)
        restecg = 0
        
        # Max heart rate
        thalach = 150
        if age > 50:
            thalach = 130
        if quiz_answers.get('c10'):  # sedentary
            thalach -= 20
        
        # Exercise induced angina
        exang = 1 if quiz_answers.get('c6') else 0
        
        # ST depression
        oldpeak = 0.0
        if quiz_answers.get('c6'):
            oldpeak = 2.0
        
        # Slope (1-3)
        slope = 1
        
        # Number of major vessels (0-3)
        ca = 0
        if quiz_answers.get('c5'):  # smoking
            ca = 1
        if quiz_answers.get('c1'):  # family history
            ca += 1
        
        # Thalassemia (2-7)
        thal = 2
        if quiz_answers.get('c2') or quiz_answers.get('c3'):
            thal = 7
        
        features = {
            'age': age,
            'sex': sex,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal
        }
        
        # Add interaction terms if model has them
        if 'age_chol' in self.cholesterol_features:
            features['age_chol'] = age * chol
            features['bp_chol'] = trestbps * chol
            features['age_thalach'] = age * thalach
        
        return features
    
    def predict_from_quiz(self, quiz_answers: Dict, user_info: Dict) -> Dict:
        """Generate predictions from quiz answers using ML models"""
        
        # Map quiz to features
        diabetes_features = self.map_quiz_to_diabetes_features(quiz_answers, user_info)
        cholesterol_features = self.map_quiz_to_cholesterol_features(quiz_answers, user_info)
        
        # Prepare feature vectors
        diabetes_vector = [diabetes_features[f] for f in self.diabetes_features]
        cholesterol_vector = [cholesterol_features[f] for f in self.cholesterol_features]
        
        # Scale and predict
        diabetes_scaled = self.diabetes_scaler.transform([diabetes_vector])
        cholesterol_scaled = self.cholesterol_scaler.transform([cholesterol_vector])
        
        diabetes_prob = self.diabetes_model.predict_proba(diabetes_scaled)[0][1]
        cholesterol_prob = self.cholesterol_model.predict_proba(cholesterol_scaled)[0][1]
        
        # Convert to percentage scores
        diabetes_score = int(diabetes_prob * 100)
        cholesterol_score = int(cholesterol_prob * 100)
        combined_score = int((diabetes_prob + cholesterol_prob) / 2 * 100)
        
        # Determine risk levels
        if combined_score < 30:
            risk_level = "Low"
        elif combined_score < 60:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'total_score': combined_score,
            'diabetes_score': diabetes_score,
            'cholesterol_score': cholesterol_score,
            'risk_level': risk_level,
            'diabetes_probability': float(diabetes_prob),
            'cholesterol_probability': float(cholesterol_prob),
            'model_version': 'v2_enhanced'
        }

# Global predictor instance
enhanced_predictor = EnhancedMLPredictor()
