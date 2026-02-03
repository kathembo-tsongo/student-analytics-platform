from .base_model import BaseRiskModel
import pandas as pd

class CourseFailurePredictor(BaseRiskModel):
    def __init__(self):
        super().__init__(model_name='course_failure_model')
    
    def create_target(self, df):
        """Based on actual data - no GPA available"""
        failure_score = 0
        
        # Assignment scores (using avg_assignment_score)
        failure_score += (df['avg_assignment_score'] < 70).astype(int) * 3
        
        # Attendance
        failure_score += (df['attendance_rate'] < 45).astype(int) * 2
        
        # Login frequency
        failure_score += (df['avg_login_count'] < 3).astype(int) * 2
        
        # Assignment completion
        failure_score += (df['assignment_completion_rate'] < 0.68).astype(int) * 2
        
        return (failure_score >= 4).astype(int)
    
    def predict_course_risk(self, student_data):
        predictions, probabilities = self.predict(student_data)
        
        results = []
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            row = student_data.iloc[idx]
            
            struggling_areas = []
            if row['avg_assignment_score'] < 70:
                struggling_areas.append(f"Low Assignment Scores ({row['avg_assignment_score']:.1f})")
            if row['avg_login_count'] < 3:
                struggling_areas.append(f"Minimal LMS Engagement ({row['avg_login_count']:.1f} logins)")
            if row['attendance_rate'] < 45:
                struggling_areas.append(f"Poor Class Attendance ({row['attendance_rate']:.1f}%)")
            if row['assignment_completion_rate'] < 0.68:
                struggling_areas.append(f"Low Completion Rate ({row['assignment_completion_rate']*100:.1f}%)")
            
            results.append({
                'student_id': int(row['student_id']) if 'student_id' in student_data.columns else None,
                'failure_risk': bool(pred),
                'failure_probability': float(prob),
                'risk_level': self.get_risk_level(prob),
                'struggling_areas': struggling_areas,
                'current_gpa': None,  # GPA not available
                'recommendation': self.get_intervention(prob, struggling_areas)
            })
        
        return results
    
    def get_risk_level(self, probability):
        if probability >= 0.65:
            return 'HIGH'
        elif probability >= 0.35:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_intervention(self, probability, areas):
        if probability >= 0.65:
            return 'Urgent: Recommend course tutoring and academic counseling'
        elif probability >= 0.35:
            return 'Advisory: Suggest study groups and office hours attendance'
        else:
            return 'Maintain current study habits'
