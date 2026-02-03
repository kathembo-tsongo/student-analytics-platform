class ComprehensiveRiskScorer:
    def __init__(self, dropout_model, course_model, delay_model):
        self.dropout_model = dropout_model
        self.course_model = course_model
        self.delay_model = delay_model
    
    def calculate_comprehensive_score(self, student_data):
        """Calculate overall risk score (0-100)"""
        import pandas as pd
        
        # Ensure student_data is a DataFrame
        if not isinstance(student_data, pd.DataFrame):
            student_data = pd.DataFrame([student_data])
        
        # Get predictions from all models
        dropout_results = self.dropout_model.predict_with_details(student_data)
        course_results = self.course_model.predict_course_risk(student_data)
        delay_results = self.delay_model.predict_delay_risk(student_data)
        
        comprehensive_results = []
        
        # Convert to int to avoid numpy.int64 issues
        num_students = int(len(student_data))
        
        for i in range(num_students):
            # Weighted risk score
            dropout_weight = 0.4
            course_weight = 0.35
            delay_weight = 0.25
            
            risk_score = (
                dropout_results[i]['risk_probability'] * dropout_weight +
                course_results[i]['failure_probability'] * course_weight +
                delay_results[i]['delay_probability'] * delay_weight
            ) * 100
            
            # Overall risk level
            if risk_score >= 70:
                overall_level = 'CRITICAL'
                priority = 1
            elif risk_score >= 50:
                overall_level = 'HIGH'
                priority = 2
            elif risk_score >= 30:
                overall_level = 'MEDIUM'
                priority = 3
            else:
                overall_level = 'LOW'
                priority = 4
            
            # Combine all risk factors
            all_risk_factors = list(set(
                dropout_results[i].get('risk_factors', []) +
                course_results[i].get('struggling_areas', []) +
                delay_results[i].get('contributing_factors', [])
            ))
            
            # Get recommendations
            recommendations = self._generate_recommendations(
                dropout_results[i],
                course_results[i],
                delay_results[i]
            )
            
            comprehensive_results.append({
                'student_id': dropout_results[i].get('student_id', i+1),
                'overall_risk_score': round(risk_score, 2),
                'overall_risk_level': overall_level,
                'priority': priority,
                'dropout_risk': dropout_results[i],
                'course_failure_risk': course_results[i],
                'program_delay_risk': delay_results[i],
                'all_risk_factors': all_risk_factors,
                'recommended_actions': recommendations,
                'intervention_urgency': 'IMMEDIATE' if priority <= 2 else 'ROUTINE'
            })
        
        return comprehensive_results
    
    def _generate_recommendations(self, dropout_risk, course_risk, delay_risk):
        """Generate actionable recommendations"""
        recommendations = []
        
        if dropout_risk.get('risk_probability', 0) > 0.5:
            recommendations.append("Schedule immediate meeting with student")
            recommendations.append("Connect with academic advisor")
        
        if course_risk.get('failure_probability', 0) > 0.5:
            recommendations.append("Arrange tutoring or peer support")
            recommendations.append("Review course performance weekly")
        
        if delay_risk.get('delay_probability', 0) > 0.5:
            recommendations.append("Review academic plan and timeline")
            recommendations.append("Identify courses for next semester")
        
        if 'Low attendance' in str(dropout_risk.get('risk_factors', [])):
            recommendations.append("Monitor attendance daily")
        
        return recommendations
