from .base_model import BaseRiskModel
import pandas as pd

class ProgramDelayPredictor(BaseRiskModel):
    def __init__(self):
        super().__init__(model_name='program_delay_model')
    
    def create_target(self, df):
        """Based on actual data"""
        delay_score = 0
        
        # Low completion rate
        delay_score += (df['assignment_completion_rate'] < 0.68).astype(int) * 3
        
        # Very low completion
        delay_score += (df['assignment_completion_rate'] < 0.60).astype(int) * 2
        
        # Poor attendance
        delay_score += (df['attendance_rate'] < 45).astype(int) * 2
        
        # Low engagement
        delay_score += (df['avg_engagement_score'] < 73).astype(int) * 2
        
        return (delay_score >= 4).astype(int)
    
    def predict_delay_risk(self, student_data):
        predictions, probabilities = self.predict(student_data)
        
        results = []
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            row = student_data.iloc[idx]
            
            # Estimate delay based on performance
            delay_factors = 0
            if row['assignment_completion_rate'] < 0.60:
                delay_factors += 1
            if row['attendance_rate'] < 40:
                delay_factors += 1
            
            estimated_delay = delay_factors * 0.5
            
            contributing_factors = []
            if row['assignment_completion_rate'] < 0.68:
                contributing_factors.append(f"Low Assignment Completion ({row['assignment_completion_rate']*100:.1f}%)")
            if row['attendance_rate'] < 45:
                contributing_factors.append(f"Poor Attendance ({row['attendance_rate']:.1f}%)")
            if row['avg_engagement_score'] < 73:
                contributing_factors.append(f"Low Engagement ({row['avg_engagement_score']:.1f})")
            
            results.append({
                'student_id': int(row['student_id']) if 'student_id' in student_data.columns else None,
                'delay_risk': bool(pred),
                'delay_probability': float(prob),
                'estimated_delay_semesters': float(estimated_delay),
                'risk_level': self.get_risk_level(prob),
                'contributing_factors': contributing_factors,
                'year_of_study': int(row['year_of_study']),
                'recommendation': self.get_action_plan(prob, estimated_delay)
            })
        
        return results
    
    def get_risk_level(self, probability):
        if probability >= 0.7:
            return 'HIGH'
        elif probability >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_action_plan(self, probability, delay):
        if probability >= 0.7:
            return f'Critical: Student may delay graduation by {delay:.1f} semesters. Immediate academic planning required.'
        elif probability >= 0.4:
            return 'Caution: Monitor progress closely and provide academic support resources.'
        else:
            return 'On track: Continue regular academic advising.'
