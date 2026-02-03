"""
Historical Data Generator for ML Training
Simulates 4 years of student data (2020-2024) with known outcomes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class HistoricalDataGenerator:
    def __init__(self):
        self.random_seed = 42
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        
    def generate_student_history(self, num_students=800):
        """Generate historical student data with known outcomes"""
        print(f"🎓 Generating historical data for {num_students} students...")
        print("="*60)
        
        historical_students = []
        
        # Outcome distribution (60% graduated, 20% dropped, 20% active)
        outcomes = ['graduated'] * int(num_students * 0.60) + \
                   ['dropped_out'] * int(num_students * 0.20) + \
                   ['active'] * int(num_students * 0.20)
        random.shuffle(outcomes)
        
        for i in range(num_students):
            outcome = outcomes[i]
            enrollment_year = random.randint(2020, 2023)
            enrollment_month = random.choice([1, 9])
            enrollment_date = f"{enrollment_year}-{enrollment_month:02d}-01"
            
            student_data = self._generate_student_metrics(outcome, enrollment_date)
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
        
        return df
    
    def _generate_student_metrics(self, outcome, enrollment_date):
        """Generate realistic metrics based on outcome"""
        
        if outcome == 'dropped_out':
            attendance_rate = np.random.normal(38, 8)
            engagement_score = np.random.normal(60, 10)
            assignment_completion = np.random.normal(55, 12)
            avg_grade_points = np.random.normal(1.8, 0.5)
            login_count = np.random.normal(2.5, 1.0)
            time_spent = np.random.normal(120, 40)
            consecutive_absences = np.random.randint(5, 12)
            repeat_courses = np.random.randint(1, 4)
            assignment_score = np.random.normal(52, 15)
            forum_posts = np.random.randint(0, 5)
            
        elif outcome == 'graduated':
            attendance_rate = np.random.normal(78, 8)
            engagement_score = np.random.normal(85, 8)
            assignment_completion = np.random.normal(88, 8)
            avg_grade_points = np.random.normal(3.2, 0.4)
            login_count = np.random.normal(8.5, 2.0)
            time_spent = np.random.normal(320, 60)
            consecutive_absences = np.random.randint(0, 3)
            repeat_courses = np.random.randint(0, 2)
            assignment_score = np.random.normal(82, 10)
            forum_posts = np.random.randint(8, 25)
            
        else:  # active
            attendance_rate = np.random.normal(65, 15)
            engagement_score = np.random.normal(75, 15)
            assignment_completion = np.random.normal(75, 15)
            avg_grade_points = np.random.normal(2.6, 0.6)
            login_count = np.random.normal(6.0, 2.5)
            time_spent = np.random.normal(240, 80)
            consecutive_absences = np.random.randint(2, 6)
            repeat_courses = np.random.randint(0, 2)
            assignment_score = np.random.normal(70, 15)
            forum_posts = np.random.randint(3, 15)
        
        attendance_rate = np.clip(attendance_rate, 20, 95)
        engagement_score = np.clip(engagement_score, 40, 100)
        assignment_completion = np.clip(assignment_completion, 30, 100)
        avg_grade_points = np.clip(avg_grade_points, 0.0, 4.0)
        login_count = np.clip(login_count, 1, 15)
        time_spent = np.clip(time_spent, 60, 500)
        assignment_score = np.clip(assignment_score, 30, 100)
        
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
            'late_submissions': np.random.randint(0, 10),
            'help_requests': np.random.randint(0, 15),
            'total_enrollments': np.random.randint(3, 8),
        }
    
    def save_to_csv(self, df, filename='data/historical/historical_students.csv'):
        """Save historical data to CSV"""
        df.to_csv(filename, index=False)
        print(f"\n✅ Saved to: {filename}")
        print(f"📊 Total records: {len(df)}")

def main():
    print("\n" + "="*60)
    print("🎓 HISTORICAL STUDENT DATA GENERATOR")
    print("="*60 + "\n")
    
    generator = HistoricalDataGenerator()
    df = generator.generate_student_history(num_students=800)
    generator.save_to_csv(df)
    
    print("\n✅ COMPLETE! File: data/historical/historical_students.csv\n")

if __name__ == "__main__":
    main()
