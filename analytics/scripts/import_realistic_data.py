#!/usr/bin/env python3
"""Import realistic student data into all related tables"""

import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import random

def main():
    csv_path = 'scripts/students_realistic_440.csv'
    
    print("=" * 70)
    print("IMPORT REALISTIC STUDENT DATA")
    print("=" * 70)
    
    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"\n✓ Loaded CSV: {len(df)} students")
    
    # Connect
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='newpassword',
        database='strathmore_analytics'
    )
    cursor = conn.cursor()
    print("✓ Connected to MySQL")
    
    try:
        # Don't backup again - they already exist
        print("\n✓ Skipping backup (already created)")
        
        # Clear existing data
        print("\n✓ Clearing old data...")
        cursor.execute("DELETE FROM attendance_records")
        cursor.execute("DELETE FROM lms_activities")
        cursor.execute("DELETE FROM sis_enrollments")
        cursor.execute("DELETE FROM students")
        conn.commit()
        
        # Insert students and related data
        print("\n✓ Inserting 440 students with realistic data...")
        
        current_year = datetime.now().year
        
        for idx, row in df.iterrows():
            # 1. Insert student
            cursor.execute("""
                INSERT INTO students (student_code, program_id, school_id, 
                                     enrollment_date, year_of_study, status, gpa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['student_id'],
                row.get('program_id', random.randint(1, 20)),
                row.get('school_id', random.randint(1, 5)),
                row['enrollment_date'],
                row['year_of_study'],
                'active',
                row['avg_grade_points']
            ))
            student_db_id = cursor.lastrowid
            
            # 2. Insert attendance records (60 days)
            attendance_rate = row['attendance_rate'] / 100
            for day in range(60):
                date = datetime.now() - timedelta(days=60-day)
                if date.weekday() < 5:  # Weekdays only
                    status = 'present' if random.random() < attendance_rate else 'absent'
                    cursor.execute("""
                        INSERT INTO attendance_records 
                        (student_id, date, status, consecutive_absences)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        student_db_id,
                        date.date(),
                        status,
                        row['consecutive_absences'] if status == 'absent' else 0
                    ))
            
            # 3. Insert LMS activities (FIXED - added academic_year)
            cursor.execute("""
                INSERT INTO lms_activities 
                (student_id, week_number, academic_year, login_count, 
                 time_spent_minutes, assignments_submitted, assignments_total, 
                 avg_assignment_score, quizzes_attempted, resources_accessed,
                 discussion_posts, engagement_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student_db_id,
                12,  # Week 12
                current_year,  # FIXED: Added academic_year
                int(row['avg_login_count']),
                int(row['time_spent_minutes']),
                int(row['assignment_completion_rate'] * row['total_enrollments'] * 3),
                row['total_enrollments'] * 3,
                row['avg_assignment_score'],
                int(row['total_enrollments'] * 2),  # quizzes_attempted
                int(row['avg_engagement_score']),   # resources_accessed
                row.get('forum_posts', 5),          # discussion_posts
                row['avg_engagement_score']
            ))
            
            # 4. Insert enrollments (FIXED - added enrollment_date and status)
            for course_num in range(int(row['total_enrollments'])):
                cursor.execute("""
                    INSERT INTO sis_enrollments 
                    (student_id, course_id, semester, enrollment_date, 
                     status, grade_points, is_repeating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    student_db_id,
                    random.randint(1, 50),
                    'Fall 2024',
                    row['enrollment_date'],  # FIXED: Added enrollment_date
                    'enrolled',              # FIXED: Added status
                    float(row['avg_grade_points']) + random.uniform(-0.5, 0.5),
                    1 if course_num < row['repeat_courses'] else 0
                ))
            
            if (idx + 1) % 50 == 0:
                conn.commit()
                print(f"  Processed {idx + 1}/{len(df)} students...")
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_records")
        attendance_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT AVG(ar.attendance_rate) as avg_att
            FROM (
                SELECT student_id, 
                       SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) / COUNT(*) * 100 as attendance_rate
                FROM attendance_records
                GROUP BY student_id
            ) ar
        """)
        avg_attendance = cursor.fetchone()[0]
        
        print(f"\n" + "=" * 70)
        print("✅ IMPORT COMPLETE!")
        print("=" * 70)
        print(f"Students imported:        {student_count}")
        print(f"Attendance records:       {attendance_count}")
        print(f"Mean attendance:          {avg_attendance:.1f}%")
        
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Run: python check_data_distribution.py")
        print("2. Restart Flask API")
        print("3. Check your dashboard - should show realistic predictions!")
        
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
