
"""
Historical Cohort 2021 Generator
================================
Creates CSV files with historical student data
"""
import pandas as pd
import numpy as np
from datetime import datetime
import random
from pathlib import Path

np.random.seed(42)
random.seed(42)

print("\n" + "🎓" * 35)
print("GENERATING HISTORICAL COHORT 2021")
print("🎓" * 35 + "\n")

# Create directory
print("📁 Creating data/historical directory...")
Path('data/historical').mkdir(parents=True, exist_ok=True)
print("   ✅ Directory ready\n")

# Generate 5000 students
print("👥 Generating 5,000 students...")
students = []
student_counter = 1

schools = {
    'SBS': 1200,
    'SCES': 1300,
    'SIMS': 800,
    'SHSS': 1000,
    'SLS': 700
}

programs = {
    'SBS': ['BCOM', 'BSCM', 'BFS'],
    'SCES': ['BBIT', 'BICS', 'BCNC', 'BEEE'],
    'SIMS': ['BBSA', 'BBSE', 'BBSF', 'BSSD'],
    'SHSS': ['BACO', 'BAIS', 'BADS', 'BSCP'],
    'SLS': ['LLB']
}

names_first = ['John', 'Mary', 'Peter', 'Sarah', 'James', 'Grace', 
               'David', 'Faith', 'Michael', 'Jane', 'Daniel', 'Ruth',
               'Joseph', 'Ann', 'Kevin', 'Lucy']
names_last = ['Kamau', 'Wanjiru', 'Ochieng', 'Muthoni', 'Kibet', 
              'Achieng', 'Njoroge', 'Wambui']

for school_id, num_students in schools.items():
    for i in range(num_students):
        # Performance category
        perf = random.choice(['excellent', 'good', 'average', 'struggling'])
        
        if perf == 'excellent':
            attend = random.uniform(0.85, 1.0)
            gpa = random.uniform(3.5, 4.0)
            grade = random.uniform(80, 95)
            lms = random.randint(100, 200)
            dropout_chance = 0.05
        elif perf == 'good':
            attend = random.uniform(0.75, 0.90)
            gpa = random.uniform(2.8, 3.5)
            grade = random.uniform(70, 85)
            lms = random.randint(60, 120)
            dropout_chance = 0.10
        elif perf == 'average':
            attend = random.uniform(0.65, 0.80)
            gpa = random.uniform(2.3, 2.9)
            grade = random.uniform(55, 75)
            lms = random.randint(40, 80)
            dropout_chance = 0.20
        else:  # struggling
            attend = random.uniform(0.30, 0.70)
            gpa = random.uniform(1.5, 2.4)
            grade = random.uniform(30, 60)
            lms = random.randint(10, 50)
            dropout_chance = 0.50
        
        # Determine outcome
        dropped_out = random.random() < dropout_chance
        
        if not dropped_out:
            failed_courses = random.random() < (0.3 if perf in ['average', 'struggling'] else 0.05)
            delayed = random.random() < (0.25 if perf in ['average', 'struggling'] else 0.10)
        else:
            failed_courses = 1
            delayed = 0
        
        students.append({
            'student_id': f'H2021_{100000 + student_counter}',
            'name': f'{random.choice(names_first)} {random.choice(names_last)}',
            'cohort_year': 2021,
            'program_code': random.choice(programs[school_id]),
            'school_id': school_id,
            
            # Year 1 Semester 1 indicators (FEATURES)
            'y1s1_attendance_rate': round(attend, 3),
            'y1s1_gpa': round(gpa, 2),
            'y1s1_avg_grade': round(grade, 1),
            'y1s1_lms_activities': int(lms),
            'y1s1_courses_enrolled': random.choice([6, 6, 7, 7]),
            'y1s1_exam_eligible': 1 if attend >= 0.67 else 0,
            'y1s1_attendance_below_67': 1 if attend < 0.67 else 0,
            'y1s1_gpa_below_2': 1 if gpa < 2.0 else 0,
            'y1s1_grade_below_40': 1 if grade < 40 else 0,
            'y1s1_low_engagement': 1 if lms < 50 else 0,
            
            # Outcomes (TARGETS)
            'dropped_out': 1 if dropped_out else 0,
            'graduated_on_time': 0 if (dropped_out or delayed) else 1,
            'delayed_graduation': 1 if delayed else 0,
            'failed_courses': 1 if failed_courses else 0,
            'final_status': 'DROPPED_OUT' if dropped_out else ('DELAYED' if delayed else 'GRADUATED')
        })
        
        student_counter += 1

# Create DataFrame
df = pd.DataFrame(students)

print(f"   ✅ Generated {len(df):,} students\n")

print("📊 Final Outcomes:")
print(f"   Dropped Out: {df['dropped_out'].sum():,} ({df['dropped_out'].mean()*100:.1f}%)")
print(f"   Graduated: {df['graduated_on_time'].sum():,} ({df['graduated_on_time'].mean()*100:.1f}%)")
print(f"   Delayed: {df['delayed_graduation'].sum():,} ({df['delayed_graduation'].mean()*100:.1f}%)")
print(f"   Failed Courses: {df['failed_courses'].sum():,} ({df['failed_courses'].mean()*100:.1f}%)\n")

# Save full dataset
print("💾 Saving files...")
df.to_csv('data/historical/cohort_2021_historical.csv', index=False)
print("   ✅ data/historical/cohort_2021_historical.csv")

# Split into train/test (80/20)
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_size = int(len(df) * 0.8)

train_df = df_shuffled[:train_size]
test_df = df_shuffled[train_size:]

train_df.to_csv('data/historical/train_cohort_2021.csv', index=False)
print(f"   ✅ data/historical/train_cohort_2021.csv ({len(train_df):,} students)")

test_df.to_csv('data/historical/test_cohort_2021.csv', index=False)
print(f"   ✅ data/historical/test_cohort_2021.csv ({len(test_df):,} students)")

print("\n" + "="*70)
print("✅ HISTORICAL DATA GENERATION COMPLETE!")
print("="*70)
print("\n👉 Next step: Train the model")
print("   python train_model.py\n")


