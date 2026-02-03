from utils.strathmore_policies import StrathmoreAcademicPolicies

class ComprehensiveRiskScorer:
    def __init__(self, dropout_model, course_model, delay_model):
        self.dropout_model = dropout_model
        self.course_model = course_model
        self.delay_model = delay_model
    
    def calculate_comprehensive_score(self, student_data):
        """
        Calculate overall risk score with policy integration
        """
        import pandas as pd
        
        # Ensure student_data is DataFrame
        if not isinstance(student_data, pd.DataFrame):
            student_data = pd.DataFrame([student_data])
        
        # Get ML predictions
        dropout_results = self.dropout_model.predict_with_details(student_data)
        course_results = self.course_model.predict_course_risk(student_data)
        delay_results = self.delay_model.predict_delay_risk(student_data)
        
        comprehensive_results = []
        num_students = int(len(student_data))
        
        for i in range(num_students):
            student_dict = student_data.iloc[i].to_dict()
            
            # GET POLICY EVALUATION
            policy_check = StrathmoreAcademicPolicies.evaluate_all_policies(student_dict)
            
            # ML-BASED RISK SCORE (0-100)
            dropout_weight = 0.4
            course_weight = 0.35
            delay_weight = 0.25
            
            ml_risk_score = (
                dropout_results[i]['risk_probability'] * dropout_weight +
                course_results[i]['failure_probability'] * course_weight +
                delay_results[i]['delay_probability'] * delay_weight
            ) * 100
            
            # POLICY-BASED RISK SCORE (0-100)
            policy_risk_score = policy_check['policy_risk_score']
            
            # COMBINED RISK SCORE (take the higher of ML or Policy)
            final_risk_score = max(ml_risk_score, policy_risk_score)
            
            # DETERMINE OVERALL RISK LEVEL
            # If policy says CRITICAL, override ML
            if policy_check['overall_policy_risk'] == 'CRITICAL':
                overall_level = 'CRITICAL'
                priority = 1
            elif final_risk_score >= 70:
                overall_level = 'CRITICAL'
                priority = 1
            elif final_risk_score >= 50 or policy_check['overall_policy_risk'] == 'HIGH':
                overall_level = 'HIGH'
                priority = 2
            elif final_risk_score >= 30 or policy_check['overall_policy_risk'] == 'MEDIUM':
                overall_level = 'MEDIUM'
                priority = 3
            else:
                overall_level = 'LOW'
                priority = 4
            
            # COMBINE RISK FACTORS
            all_risk_factors = list(set(
                dropout_results[i].get('risk_factors', []) +
                course_results[i].get('struggling_areas', []) +
                delay_results[i].get('contributing_factors', [])
            ))
            
            # ADD POLICY VIOLATIONS AS RISK FACTORS
            for violation in policy_check['violations']:
                all_risk_factors.append(f"POLICY: {violation['policy']}")
            
            # GENERATE RECOMMENDATIONS
            recommendations = self._generate_recommendations(
                dropout_results[i],
                course_results[i],
                delay_results[i],
                policy_check
            )
            
            comprehensive_results.append({
                'student_id': dropout_results[i].get('student_id', student_dict.get('student_id', i+1)),
                'overall_risk_score': round(final_risk_score, 2),
                'overall_risk_level': overall_level,
                'priority': priority,
                
                # ML Predictions
                'ml_risk_score': round(ml_risk_score, 2),
                'dropout_risk': dropout_results[i],
                'course_failure_risk': course_results[i],
                'program_delay_risk': delay_results[i],
                
                # Policy Evaluation
                'policy_risk_score': policy_risk_score,
                'policy_check': policy_check,
                'policy_compliant': policy_check['policy_compliant'],
                'policy_violations': policy_check['violations'],
                'policy_warnings': policy_check['warnings'],
                
                # Combined Assessment
                'all_risk_factors': all_risk_factors,
                'recommended_actions': recommendations,
                'intervention_urgency': 'IMMEDIATE' if priority == 1 else ('HIGH' if priority == 2 else 'ROUTINE'),
                'requires_immediate_action': policy_check['requires_immediate_action']
            })
        
        return comprehensive_results
    
    def _generate_recommendations(self, dropout_risk, course_risk, delay_risk, policy_check):
        """Generate actionable recommendations"""
        recommendations = []
        
        # POLICY-BASED RECOMMENDATIONS (HIGHEST PRIORITY)
        if policy_check['violations']:
            for violation in policy_check['violations'][:3]:  # Top 3
                recommendations.append(f"🚨 {violation['action']}")
        
        # ML-BASED RECOMMENDATIONS
        if dropout_risk.get('risk_probability', 0) > 0.5:
            recommendations.append("📞 Schedule immediate one-on-one meeting")
            recommendations.append("🤝 Connect with academic advisor")
        
        if course_risk.get('failure_probability', 0) > 0.5:
            recommendations.append("📚 Arrange tutoring or peer support")
            recommendations.append("📊 Review course performance weekly")
        
        if delay_risk.get('delay_probability', 0) > 0.5:
            recommendations.append("📅 Review academic plan and timeline")
            recommendations.append("✅ Ensure prerequisite courses completed")
        
        # POLICY WARNINGS
        if policy_check['warnings']:
            for warning in policy_check['warnings'][:2]:  # Top 2
                recommendations.append(f"⚠️ {warning['action']}")
        
        return recommendations[:8]  # Limit to 8 recommendations
