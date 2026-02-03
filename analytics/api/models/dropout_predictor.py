from .base_model import BaseRiskModel
import pandas as pd
import numpy as np

class DropoutRiskPredictor(BaseRiskModel):
    def __init__(self):
        super().__init__(model_name='dropout_risk_model')
        
    def create_target(self, df):
        """
        Create dropout risk based on ACTUAL data distribution:
        - Attendance: mean=53%, range 20-72%
        - Engagement: mean=78, range 55-95
        - Assignment completion: mean=74%, range 52-90%
        """
        risk_score = 0
        
        # Attendance risk (below 45% = 25th percentile)
        risk_score += (df['attendance_rate'] < 45).astype(int) * 3
        
        # Very low attendance (below 35%)
        risk_score += (df['attendance_rate'] < 35).astype(int) * 2
        
        # Engagement risk (below 73 = 25th percentile)
        risk_score += (df['avg_engagement_score'] < 73).astype(int) * 2
        
        # Very low engagement (below 65)
        risk_score += (df['avg_engagement_score'] < 65).astype(int) * 2
        
        # Assignment completion risk (below 68% = 25th percentile)
        risk_score += (df['assignment_completion_rate'] < 0.68).astype(int) * 2
        
        # Very low completion (below 60%)
        risk_score += (df['assignment_completion_rate'] < 0.60).astype(int) * 2
        
        # Low login frequency
        risk_score += (df['avg_login_count'] < 3).astype(int) * 1
        
        # High risk if score >= 5
        return (risk_score >= 5).astype(int)
    
    def get_risk_level(self, probability):
        if probability >= 0.7:
            return 'HIGH'
        elif probability >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def predict_with_details(self, student_data):
        predictions, probabilities = self.predict(student_data)
        
        results = []
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            risk_level = self.get_risk_level(prob)
            row = student_data.iloc[idx]
            
            risk_factors = []
            if row['attendance_rate'] < 45:
                risk_factors.append(f"Low Attendance ({row['attendance_rate']:.1f}%)")
            if row['avg_engagement_score'] < 73:
                risk_factors.append(f"Low Engagement ({row['avg_engagement_score']:.1f})")
            if row['assignment_completion_rate'] < 0.68:
                risk_factors.append(f"Low Assignment Completion ({row['assignment_completion_rate']*100:.1f}%)")
            if row['avg_login_count'] < 3:
                risk_factors.append(f"Low Login Frequency ({row['avg_login_count']:.1f})")
            
            results.append({
                'student_id': int(student_data.iloc[idx]['student_id']) if 'student_id' in student_data.columns else None,
                'at_risk': bool(pred),
                'risk_probability': float(prob),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendation': self.get_recommendation(risk_level, risk_factors)
            })
        
        return results
    
    def get_recommendation(self, risk_level, risk_factors):
        if risk_level == 'HIGH':
            return 'Immediate intervention required. Schedule mentor meeting and academic support.'
        elif risk_level == 'MEDIUM':
            return 'Monitor closely. Consider additional tutoring or study groups.'
        else:
            return 'Continue regular monitoring.'
