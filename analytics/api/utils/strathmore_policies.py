"""
Strathmore University Academic Policies Engine
Official institutional policies for early warning system
"""

class StrathmoreAcademicPolicies:
    """
    Official Strathmore University Academic Policies
    Based on actual institutional requirements
    """
    
    # POLICY 1: Attendance Requirement
    MINIMUM_ATTENDANCE = 67
    ATTENDANCE_WARNING = 70
    ATTENDANCE_SAFE = 75
    
    # POLICY 2: Pass Mark Requirement
    MINIMUM_PASS_MARK = 40
    PASS_WARNING = 45
    PASS_SAFE = 50
    
    # POLICY 3: Course Repetition Limits
    MAX_SAME_COURSE_REPEATS = 2
    MAX_TOTAL_REPEATS = 3
    
    # POLICY 4: Academic Standing (GPA)
    DISCONTINUATION_GPA = 2.0
    PROBATION_WARNING = 2.5
    GOOD_STANDING_GPA = 3.0
    
    # POLICY 5: Maximum Study Duration
    NORMAL_DURATION = 4  # Years
    MAXIMUM_DURATION = 6  # Years
    
    @staticmethod
    def evaluate_all_policies(student_data):
        """
        Evaluate student against all Strathmore policies
        Returns comprehensive policy compliance report
        """
        violations = []
        warnings = []
        risk_scores = []
        
        # 1. CHECK ATTENDANCE (HIGHEST PRIORITY)
        attendance = float(student_data.get('attendance_rate', 100))
        if attendance < 60:
            violations.append({
                'policy': 'Attendance Requirement',
                'severity': 'CRITICAL',
                'value': f'{attendance:.1f}%',
                'threshold': '67% minimum',
                'consequence': '🚨 CANNOT SIT FOR EXAM - Automatic course failure',
                'action': '⚡ IMMEDIATE: Meet with student TODAY',
                'priority': 1
            })
            risk_scores.append(95)
        elif attendance < 67:
            violations.append({
                'policy': 'Attendance Requirement',
                'severity': 'CRITICAL',
                'value': f'{attendance:.1f}%',
                'threshold': '67% minimum',
                'consequence': '❌ Will NOT be allowed to sit for exam',
                'action': '🔴 URGENT: Improve attendance immediately',
                'priority': 1
            })
            risk_scores.append(90)
        elif attendance < 70:
            warnings.append({
                'policy': 'Attendance Requirement',
                'severity': 'HIGH',
                'value': f'{attendance:.1f}%',
                'threshold': '67% minimum',
                'consequence': 'Dangerously close to exam ineligibility',
                'action': '🟠 Monitor closely - approaching danger zone',
                'priority': 2
            })
            risk_scores.append(70)
        elif attendance < 75:
            warnings.append({
                'policy': 'Attendance Requirement',
                'severity': 'MEDIUM',
                'value': f'{attendance:.1f}%',
                'threshold': '75% recommended',
                'action': '🟡 Attendance needs improvement',
                'priority': 3
            })
            risk_scores.append(50)
        
        # 2. CHECK PASS MARK
        avg_score = float(student_data.get('avg_assignment_score', 100))
        if avg_score < 35:
            violations.append({
                'policy': 'Pass Mark Requirement',
                'severity': 'CRITICAL',
                'value': f'{avg_score:.1f}%',
                'threshold': '40% minimum',
                'consequence': '❌ Likely to FAIL course',
                'action': '🔴 Arrange intensive tutoring and academic support',
                'priority': 1
            })
            risk_scores.append(85)
        elif avg_score < 40:
            violations.append({
                'policy': 'Pass Mark Requirement',
                'severity': 'CRITICAL',
                'value': f'{avg_score:.1f}%',
                'threshold': '40% minimum',
                'consequence': '⚠️ Below pass mark - course failure imminent',
                'action': '🔴 URGENT: Academic intervention required',
                'priority': 1
            })
            risk_scores.append(80)
        elif avg_score < 45:
            warnings.append({
                'policy': 'Pass Mark Requirement',
                'severity': 'HIGH',
                'value': f'{avg_score:.1f}%',
                'threshold': '40% minimum',
                'consequence': 'Borderline passing',
                'action': '🟠 Additional support needed to ensure pass',
                'priority': 2
            })
            risk_scores.append(60)
        elif avg_score < 50:
            warnings.append({
                'policy': 'Pass Mark Requirement',
                'severity': 'MEDIUM',
                'value': f'{avg_score:.1f}%',
                'threshold': '50% recommended',
                'action': '🟡 Performance could be stronger',
                'priority': 3
            })
            risk_scores.append(45)
        
        # 3. CHECK COURSE REPETITIONS
        repeats = int(student_data.get('repeat_courses', 0))
        if repeats >= 4:
            violations.append({
                'policy': 'Course Repetition Limit',
                'severity': 'CRITICAL',
                'value': f'{repeats} courses repeated',
                'threshold': 'Maximum 3 total',
                'consequence': '🚨 Academic probation / DISCONTINUATION risk',
                'action': '🔴 Academic counseling and intervention required',
                'priority': 1
            })
            risk_scores.append(85)
        elif repeats == 3:
            warnings.append({
                'policy': 'Course Repetition Limit',
                'severity': 'HIGH',
                'value': f'{repeats} courses repeated',
                'threshold': 'Maximum 3 total',
                'consequence': 'At maximum limit - no more failures allowed',
                'action': '🟠 Cannot fail any more courses',
                'priority': 2
            })
            risk_scores.append(70)
        elif repeats >= 2:
            warnings.append({
                'policy': 'Course Repetition Limit',
                'severity': 'MEDIUM',
                'value': f'{repeats} courses repeated',
                'threshold': 'Maximum 3 total',
                'consequence': 'Pattern of difficulty emerging',
                'action': '🟡 Academic support recommended',
                'priority': 3
            })
            risk_scores.append(55)
        
        # 4. CHECK GPA / ACADEMIC STANDING
        gpa = float(student_data.get('avg_grade_points', 4.0))
        if gpa < 1.5:
            violations.append({
                'policy': 'Academic Standing (GPA)',
                'severity': 'CRITICAL',
                'value': f'{gpa:.2f}',
                'threshold': '2.0 minimum',
                'consequence': '🚨 DISCONTINUATION highly likely',
                'action': '🔴 Must meet with Dean - exit or significant improvement',
                'priority': 1
            })
            risk_scores.append(90)
        elif gpa < 2.0:
            violations.append({
                'policy': 'Academic Standing (GPA)',
                'severity': 'CRITICAL',
                'value': f'{gpa:.2f}',
                'threshold': '2.0 minimum',
                'consequence': '❌ ACADEMIC PROBATION - must improve next semester',
                'action': '🔴 Academic support plan required',
                'priority': 1
            })
            risk_scores.append(75)
        elif gpa < 2.5:
            warnings.append({
                'policy': 'Academic Standing (GPA)',
                'severity': 'HIGH',
                'value': f'{gpa:.2f}',
                'threshold': '2.5 recommended',
                'consequence': 'Below good standing threshold',
                'action': '🟠 Academic support recommended',
                'priority': 2
            })
            risk_scores.append(55)
        elif gpa < 3.0:
            warnings.append({
                'policy': 'Academic Standing (GPA)',
                'severity': 'MEDIUM',
                'value': f'{gpa:.2f}',
                'threshold': '3.0 good standing',
                'action': '🟡 Room for improvement',
                'priority': 3
            })
            risk_scores.append(40)
        
        # 5. CHECK STUDY DURATION
        year = int(student_data.get('year_of_study', 1))
        if year > 6:
            violations.append({
                'policy': 'Maximum Study Duration',
                'severity': 'CRITICAL',
                'value': f'Year {year}',
                'threshold': '6 years maximum',
                'consequence': '🚨 EXCEEDED maximum - must complete or EXIT',
                'action': '🔴 Completion plan required immediately',
                'priority': 1
            })
            risk_scores.append(80)
        elif year == 6:
            warnings.append({
                'policy': 'Maximum Study Duration',
                'severity': 'HIGH',
                'value': f'Year {year}',
                'threshold': '6 years maximum',
                'consequence': 'Last year allowed - must complete this year',
                'action': '🟠 Ensure all requirements completed',
                'priority': 2
            })
            risk_scores.append(65)
        elif year == 5:
            warnings.append({
                'policy': 'Maximum Study Duration',
                'severity': 'MEDIUM',
                'value': f'Year {year}',
                'threshold': '4 years normal',
                'consequence': '1 year delayed',
                'action': '🟡 Review academic plan for timely completion',
                'priority': 3
            })
            risk_scores.append(50)
        
        # CALCULATE OVERALL POLICY RISK
        if violations:
            overall_risk = 'CRITICAL' if any(v['severity'] == 'CRITICAL' for v in violations) else 'HIGH'
            policy_risk_score = max(risk_scores) if risk_scores else 0
        elif warnings:
            if any(w['severity'] == 'HIGH' for w in warnings):
                overall_risk = 'HIGH'
            else:
                overall_risk = 'MEDIUM'
            policy_risk_score = max(risk_scores) if risk_scores else 0
        else:
            overall_risk = 'LOW'
            policy_risk_score = 10
        
        # Sort violations and warnings by priority
        violations.sort(key=lambda x: x.get('priority', 99))
        warnings.sort(key=lambda x: x.get('priority', 99))
        
        return {
            'policy_compliant': len(violations) == 0,
            'violations': violations,
            'warnings': warnings,
            'overall_policy_risk': overall_risk,
            'policy_risk_score': policy_risk_score,
            'total_violations': len(violations),
            'total_warnings': len(warnings),
            'most_critical_issue': violations[0] if violations else None,
            'requires_immediate_action': len([v for v in violations if v['priority'] == 1]) > 0
        }
    
    @staticmethod
    def get_policy_summary(policy_check):
        """Generate human-readable summary of policy status"""
        summary = []
        
        if policy_check['policy_compliant']:
            summary.append("✅ Student is compliant with all Strathmore policies")
        else:
            summary.append(f"⚠️ {policy_check['total_violations']} POLICY VIOLATION(S) detected")
        
        if policy_check['requires_immediate_action']:
            summary.append("🚨 IMMEDIATE ACTION REQUIRED")
        
        if policy_check['most_critical_issue']:
            critical = policy_check['most_critical_issue']
            summary.append(f"Most Critical: {critical['policy']} - {critical['consequence']}")
        
        return " | ".join(summary)
