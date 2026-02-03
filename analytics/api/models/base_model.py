from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import joblib
import os

class BaseRiskModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.scaler = None
        self.feature_columns = None
        
        # UPDATE: Use V2 models (trained on historical data)
        self.model_path = f'models/{model_name}_model_v2.pkl'
        self.scaler_path = f'models/{model_name}_scaler_v2.pkl'
        self.features_path = f'models/{model_name}_features_v2.pkl'
        
    def load(self):
        """Load trained model, scaler, and features from disk"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.feature_columns = joblib.load(self.features_path)
                print(f"✅ Loaded {self.model_name} (V2 - Enhanced)")
                return True
            else:
                print(f"⚠️  Model not found: {self.model_path}")
                return False
        except Exception as e:
            print(f"❌ Error loading {self.model_name}: {str(e)}")
            return False
    
    def save(self):
        """Save trained model, scaler, and features to disk"""
        try:
            os.makedirs('models', exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            joblib.dump(self.feature_columns, self.features_path)
            print(f"✅ Saved {self.model_name} (V2)")
            return True
        except Exception as e:
            print(f"❌ Error saving {self.model_name}: {str(e)}")
            return False
    
    def predict(self, student_data):
        """Make prediction for students"""
        if self.model is None or self.scaler is None:
            raise Exception(f"{self.model_name} not loaded. Call load() first.")
        
        # Convert to DataFrame if needed
        if isinstance(student_data, dict):
            student_data = pd.DataFrame([student_data])
        
        # Ensure we have the right features in the right order
        if self.feature_columns:
            # Select only the columns we need, in the right order
            student_data = student_data[self.feature_columns]
        
        # Handle NaN and inf
        student_data = student_data.fillna(0)
        student_data = student_data.replace([np.inf, -np.inf], 0)
        
        # Scale features
        X_scaled = self.scaler.transform(student_data)
        
        # Predict
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        return predictions, probabilities
    
    def get_risk_level(self, probability):
        """Convert probability to risk level"""
        if probability >= 0.7:
            return 'HIGH'
        elif probability >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
