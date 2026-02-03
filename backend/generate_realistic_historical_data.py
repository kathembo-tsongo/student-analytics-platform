"""
Realistic Historical Data Generator for Strathmore University
Generates data that reflects actual university student distributions
with realistic policy compliance rates
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class RealisticHistoricalDataGenerator:
    def __init__(self):
        self.random_seed = 42
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        
    def generate_realistic_student_history(self, num_students=800):
        """
        Generate realistic historical student data
        
        Distribution aligned with typical university:
        - 60% graduated (good students)
        - 20% dropped out (struggled significantly)
        - 20% still active (mixed performance)
        """
        print(f"🎓 Generating REALISTIC historical data for {num_students} students...")
        print("="*70)
        
        historical_students = []
        
        # Realistic outcome distribution
        outcomes = (
            ['graduated'] * int(num_students * 0.60) +  # 480 students
            ['dropped_out'] * int(num_students * 0.20) + # 160 students
            ['active'] * int(num_students * 0.20)        # 160 students
        )
        random.shuffle(outcomes)
        
        for i in range(num_students):
            outcome = outcomes[i]
            enrollment_year = random.randint(2020, 2023)
            enrollment_month = random.choice([1, 9])
            enrollment_date = f"{enrollment_year}-{enrollment_month:02d}-01"
            
            student_data = self._generate_realistic_metrics(outcome, enrollment_date)
            student_data['student_id'] = 1000 + i
            student_data['outcome'] = outcome
            student_data['enrollment_date'] = enrollment_date
            student_data['school_id'] = random.randint(1, 5)
            student_data['program_id'] = random.randint(1, 20)
            student_data['year_of_study'] = random.randint(1, 4)
            
            historical_students.append(student_data)
        
        df = pd.DataFrame(historical_students)
        
        print(f"✅ Generated {len(df)} student records")
        print(f"\n📊 Outcome Distribution:")
        print(df['outcome'].value_counts())
        
        # Show policy compliance stats
        self._show_policy_compliance(df)
        
        return df
    
    def _generate_realistic_metrics(self, outcome, enrollment_date):
        """
        Generate realistic metrics based on outcome
        Following Strathmore University policies
        """
        
        if outcome == 'dropped_out':
            # Students who dropped out - BELOW policy thresholds
            # But not ALL violated policies (some just struggled academically)
            
            # 70% had attendance issues (< 67%)
            if random.random() < 0.7:
                attendance_rate = np.random.normal(50, 12)  # Below threshold
            else:
                attendance_rate = np.random.normal(68, 5)   # Just above threshold
            
            # 60% had GPA issues (< 2.0)
            if random.random() < 0.6:
                avg_grade_points = np.random.normal(1.7, 0.3)
            else:
                avg_grade_points = np.random.normal(2.3, 0.4)
            
            engagement_score = np.random.normal(55, 12)
            assignment_completion = np.random.normal(58, 15)
            assignment_score = np.random.normal(45, 12)
            login_count = np.random.normal(3.0, 1.5)
            time_spent = np.random.normal(140, 50)
            consecutive_absences = np.random.randint(4, 15)
            repeat_courses = np.random.choice([0, 1, 2, 3], p=[0.2, 0.3, 0.3, 0.2])
            forum_posts = np.random.randint(0, 8)
            late_submissions = np.random.randint(3, 12)
            help_requests = np.random.randint(2, 15)
            
        elif outcome == 'graduated':
            # Successful students - ABOVE policy thresholds
            # Most comply with all policies
            
            # 95% have good attendance (> 67%)
            if random.random() < 0.95:
                attendance_rate = np.random.normal(82, 8)   # Well above threshold
            else:
                attendance_rate = np.random.normal(69, 2)   # Just above threshold
            
            # 98% have good GPA (> 2.0)
            if random.random() < 0.98:
                avg_grade_points = np.random.normal(3.1, 0.5)
            else:
                avg_grade_points = np.random.normal(2.2, 0.2)
            
            engagement_score = np.random.normal(82, 10)
            assignment_completion = np.random.normal(85, 10)
            assignment_score = np.random.normal(75, 12)
            login_count = np.random.normal(8.0, 2.0)
            time_spent = np.random.normal(300, 70)
            consecutive_absences = np.random.randint(0, 4)
            repeat_courses = np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05])
            forum_posts = np.random.randint(10, 30)
            late_submissions = np.random.randint(0, 5)
            help_requests = np.random.randint(1, 8)
            
        else:  # active students - MIXED performance
            # Currently enrolled - realistic distribution
            
            # 80% have acceptable attendance
            if random.random() < 0.8:
                attendance_rate = np.random.normal(75, 10)
            else:
                attendance_rate = np.random.normal(60, 8)
            
            # 85% have acceptable GPA
            if random.random() < 0.85:
                avg_grade_points = np.random.normal(2.7, 0.5)
            else:
                avg_grade_points = np.random.normal(1.9, 0.3)
            
            engagement_score = np.random.normal(72, 15)
            assignment_completion = np.random.normal(75, 15)
            assignment_score = np.random.normal(65, 15)
            login_count = np.random.normal(6.0, 2.5)
            time_spent = np.random.normal(230, 80)
            consecutive_absences = np.random.randint(1, 7)
            repeat_courses = np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1])
            forum_posts = np.random.randint(5, 20)
            late_submissions = np.random.randint(1, 8)
            help_requests = np.random.randint(2, 12)
        
        # Ensure values are within realistic bounds
        attendance_rate = np.clip(attendance_rate, 15, 100)
        engagement_score = np.clip(engagement_score, 30, 100)
        assignment_completion = np.clip(assignment_completion, 20, 100)
        assignment_score = np.clip(assignment_score, 25, 100)
        avg_grade_points = np.clip(avg_grade_points, 0.0, 4.0)
        login_count = np.clip(login_count, 0.5, 20)
        time_spent = np.clip(time_spent, 30, 600)
        
        return {
            'attendance_rate': round(attendance_rate, 2),
            'engagement_score': round(engagement_score, 2),
            'assignment_completion_rate': round(assignment_completion, 2),
            'avg_assignment_score': round(assignment_score, 2),
            'avg_grade_points': round(avg_grade_points, 2),
            'avg_login_count': round(login_count, 2),
            'time_spent_minutes': round(time_spent, 2),
            'consecutive_absences': int(consecutive_absences),
            'repeat_courses': int(repeat_courses),
            'forum_posts': int(forum_posts),
            'late_submissions': int(late_submissions),
            'help_requests': int(help_requests),
            'total_enrollments': np.random.randint(4, 9),
        }
    
    def _show_policy_compliance(self, df):
        """Show how many students comply with Strathmore policies"""
        print("\n📋 POLICY COMPLIANCE ANALYSIS:")
        print("="*70)
        
        # Policy 1: Attendance >= 67%
        below_attendance = (df['attendance_rate'] < 67).sum()
        print(f"\n1. Attendance Policy (67% minimum):")
        print(f"   ✅ Compliant: {len(df) - below_attendance} ({(len(df)-below_attendance)/len(df)*100:.1f}%)")
        print(f"   ❌ Below threshold: {below_attendance} ({below_attendance/len(df)*100:.1f}%)")
        
        # Policy 2: Pass mark >= 40%
        below_pass = (df['avg_assignment_score'] < 40).sum()
        print(f"\n2. Pass Mark Policy (40% minimum):")
        print(f"   ✅ Passing: {len(df) - below_pass} ({(len(df)-below_pass)/len(df)*100:.1f}%)")
        print(f"   ❌ Below pass mark: {below_pass} ({below_pass/len(df)*100:.1f}%)")
        
        # Policy 3: GPA >= 2.0
        below_gpa = (df['avg_grade_points'] < 2.0).sum()
        print(f"\n3. Academic Standing (GPA 2.0 minimum):")
        print(f"   ✅ Good standing: {len(df) - below_gpa} ({(len(df)-below_gpa)/len(df)*100:.1f}%)")
        print(f"   ❌ Below 2.0: {below_gpa} ({below_gpa/len(df)*100:.1f}%)")
        
        # Policy 4: Course repetitions <= 3
        excessive_repeats = (df['repeat_courses'] > 3).sum()
        print(f"\n4. Course Repetition (Max 3):")
        print(f"   ✅ Within limit: {len(df) - excessive_repeats} ({(len(df)-excessive_repeats)/len(df)*100:.1f}%)")
        print(f"   ❌ Exceeded limit: {excessive_repeats} ({excessive_repeats/len(df)*100:.1f}%)")
        
        # Overall policy compliance
        any_violation = (
            (df['attendance_rate'] < 67) |
            (df['avg_assignment_score'] < 40) |
            (df['avg_grade_points'] < 2.0) |
            (df['repeat_courses'] > 3)
        ).sum()
        
        print(f"\n📊 OVERALL COMPLIANCE:")
        print(f"   ✅ All policies compliant: {len(df) - any_violation} ({(len(df)-any_violation)/len(df)*100:.1f}%)")
        print(f"   ⚠️  At least one violation: {any_violation} ({any_violation/len(df)*100:.1f}%)")
    
    def save_to_csv(self, df, filename='data/historical/historical_students.csv'):
        """Save historical data to CSV"""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"\n✅ Saved to: {filename}")
        print(f"📊 Total records: {len(df)}")
        print("="*70)

def main():
    print("\n" + "="*70)
    print("🎓 REALISTIC STRATHMORE HISTORICAL DATA GENERATOR")
    print("   Aligned with University Policies")
    print("="*70 + "\n")
    
    generator = RealisticHistoricalDataGenerator()
    df = generator.generate_realistic_student_history(num_students=800)
    generator.save_to_csv(df)
    
    print("\n✅ COMPLETE!")
    print("\n💡 Next steps:")
    print("   1. Review data/historical/historical_students.csv")
    print("   2. Run: python train_models_v2.py")
    print("   3. Restart Flask API")
    print("   4. Check predictions (should be more realistic now)")
    print("\n")

if __name__ == "__main__":
    main()
