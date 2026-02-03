#!/usr/bin/env python3
"""
Fresh Import: 440 Students with Realistic Attendance
====================================================
Creates brand new data with proper attendance distribution
"""

import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import random
import numpy as np

np.random.seed(42)
random.seed(42)

def generate_realistic_attendance(num_students=440):
    """Generate realistic attendance distribution"""
    n_compliant = int(num_students * 0.80)    # 352: 67-95%
    n_borderline = int(num_students * 0.15)   # 66: 60-67%
    n_violation = num_students - n_compliant - n_borderline  # 22: <60%
    
    attendance_rates = []
    attendance_rates.extend(np.random.beta(5, 2, n_compliant) * 28 + 67)
    attendance_rates.extend(np.random.uniform(60, 67, n_borderline))
    attendance_rates.extend(np.random.beta(2, 3, n_violation) * 40 + 20)
    
    np.random.shuffle(attendance_rates)
    return np.clip(attendance_rates, 20, 95)

def main():
    print("=" * 70)
    print("FRESH IMPORT: 440 STUDENTS WITH REALISTIC ATTENDANCE")
    print("=" * 70)
    
    # Connect
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='newpassword',
        database='strathmore_analytics'
    )
    cursor = conn.cursor()
    print("\n✓ Connected to MySQL")
    
    # Get available schools, programs, courses
    cursor.execute("SELECT id FROM schools")
    school_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, school_id FROM programs")
    programs = cursor.fetchall()
    
    cursor.execute("SELECT id, program_id FROM courses")
    courses = cursor.fetchall()
    
    print(f"✓ Found {len(school_ids)} schools, {len(programs)} programs, {len(courses)} courses")
    
    try:
        # Clear old data
        print("\n✓ Clearing old data...")
        cursor.execute("DELETE FROM attendance_records")
        cursor.execute("DELETE FROM lms_activities")
        cursor.execute("DELETE FROM sis_enrollments")
        cursor.execute("DELETE FROM students")
        conn.commit()
        
        # Generate attendance
        print("\n✓ Generating 440 students...")
        attendance_rates = generate_realistic_attendance(440)
        current_year = datetime.now().year
        
        for i in range(440):
            attendance = attendance_rates[i]
            
            # Pick random program
            program_id, school_id = random.choice(programs)
            year_of_study = random.choices([1, 2, 3, 4], weights=[0.3, 0.3, 0.25, 0.15])[0]
            enrollment_date = datetime.now() - timedelta(days=365 * year_of_study + random.randint(0, 180))
            
            # Generate correlated metrics
            engagement = np.clip(attendance * 0.8 + np.random.normal(10, 5), 50, 95)
            completion = np.clip((attendance / 100) * 0.9 + np.random.normal(0, 0.1), 0.5, 0.95)
            gpa = np.clip((engagement / 25 + completion * 2) + np.random.normal(0, 0.3), 1.0, 4.0)
            
            # 1. Insert student
            cursor.execute("""
                INSERT INTO students (student_code, program_id, school_id, 
                                     enrollment_date, year_of_study, status, gpa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                f'STU{20000 + i}',
                program_id,
                school_id,
                enrollment_date.date(),
                year_of_study,
                'active',
                round(gpa, 2)
            ))
            student_db_id = cursor.lastrowid
            
            # 2. Attendance records (60 days)
            present_count = 0
            total_days = 0
            for day in range(60):
                date = datetime.now() - timedelta(days=60-day)
                if date.weekday() < 5:
                    total_days += 1
                    status = 'present' if random.random() < (attendance/100) else 'absent'
                    if status == 'present':
                        present_count += 1
                    
                    cursor.execute("""
                        INSERT INTO attendance_records 
                        (student_id, date, status, consecutive_absences)
                        VALUES (%s, %s, %s, %s)
                    """, (student_db_id, date.date(), status, 0))
            
            # 3. LMS activities
            cursor.execute("""
                INSERT INTO lms_activities 
                (student_id, week_number, academic_year, login_count, 
                 time_spent_minutes, assignments_submitted, assignments_total, 
                 avg_assignment_score, quizzes_attempted, resources_accessed,
                 discussion_posts, engagement_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student_db_id, 12, current_year,
                int(engagement / 8 + random.randint(5, 15)),
                int(engagement * 2 + random.randint(80, 250)),
                int(completion * 15),
                15,
                round(gpa * 20 + random.randint(10, 15), 2),
                random.randint(8, 20),
                int(engagement),
                random.randint(3, 15),
                round(engagement, 2)
            ))
            
            # 4. Course enrollments
            program_courses = [c[0] for c in courses if c[1] == program_id]
            if not program_courses:
                program_courses = [random.randint(1, 90) for _ in range(6)]
            
            for _ in range(min(6, len(program_courses))):
                course_id = random.choice(program_courses)
                cursor.execute("""
                    INSERT INTO sis_enrollments 
                    (student_id, course_id, semester, enrollment_date, 
                     status, grade_points, is_repeating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    student_db_id, course_id, 'Fall 2024',
                    enrollment_date.date(), 'enrolled',
                    round(gpa + random.uniform(-0.3, 0.3), 2), 0
                ))
            
            if (i + 1) % 50 == 0:
                conn.commit()
                print(f"  Imported {i + 1}/440 students...")
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT AVG(
                (SELECT COUNT(*) FROM attendance_records ar 
                 WHERE ar.student_id = s.id AND ar.status = 'present') * 100.0 / 
                NULLIF((SELECT COUNT(*) FROM attendance_records ar2 
                        WHERE ar2.student_id = s.id), 0)
            ) FROM students s
        """)
        avg_attendance = cursor.fetchone()[0]
        
        print(f"\n" + "=" * 70)
        print("✅ IMPORT COMPLETE!")
        print("=" * 70)
        print(f"Students:             {student_count}")
        print(f"Mean attendance:      {avg_attendance:.1f}%")
        
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Run: python check_data_distribution.py")
        print("2. Restart Flask: pkill -f app.py && python api/app.py")
        print("3. Check dashboard - predictions should be realistic!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
