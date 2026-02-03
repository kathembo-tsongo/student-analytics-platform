#!/usr/bin/env python3
"""
Import Realistic Student Data into MySQL
========================================
This script replaces the current 440 students with realistic attendance data.
"""

import pandas as pd
import pymysql
import sys
from datetime import datetime

def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='admin',
            password='admin123',
            database='student_analytics',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"❌ ERROR connecting to MySQL: {e}")
        print("\nPlease ensure:")
        print("  1. MySQL is running")
        print("  2. Database 'student_analytics' exists")
        print("  3. User 'admin' has password 'admin123'")
        sys.exit(1)

def main():
    csv_path = '/home/dieudonne/student-analytics-platform/analytics/scripts/students_realistic_440.csv'
    
    print("=" * 70)
    print("IMPORT REALISTIC STUDENTS TO MYSQL")
    print("=" * 70)
    
    # Load CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"\n✓ Loaded CSV: {len(df)} students")
    except Exception as e:
        print(f"\n❌ ERROR loading CSV: {e}")
        sys.exit(1)
    
    # Connect to MySQL
    print("✓ Connecting to MySQL...")
    connection = connect_to_mysql()
    cursor = connection.cursor()
    
    try:
        # Backup existing data
        print("✓ Creating backup of existing students...")
        backup_table = f"students_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute(f"CREATE TABLE {backup_table} AS SELECT * FROM students")
        backup_count = cursor.execute(f"SELECT COUNT(*) as count FROM {backup_table}")
        cursor.fetchone()
        print(f"  Backed up existing students to: {backup_table}")
        
        # Clear current students
        print("✓ Clearing current students...")
        cursor.execute("DELETE FROM students")
        connection.commit()
        
        # Insert new students
        print("✓ Inserting 440 students with realistic attendance...")
        
        insert_query = """
        INSERT INTO students (
            student_id, name, email, school, program, year_of_study,
            enrollment_date, attendance_rate, avg_engagement_score,
            assignment_completion_rate, avg_assignment_score, avg_grade_points,
            avg_login_count, time_spent_minutes, consecutive_absences,
            repeat_courses, forum_posts, late_submissions, help_requests,
            total_enrollments
        ) VALUES (
            %(student_id)s, %(name)s, %(email)s, %(school)s, %(program)s,
            %(year_of_study)s, %(enrollment_date)s, %(attendance_rate)s,
            %(avg_engagement_score)s, %(assignment_completion_rate)s,
            %(avg_assignment_score)s, %(avg_grade_points)s, %(avg_login_count)s,
            %(time_spent_minutes)s, %(consecutive_absences)s, %(repeat_courses)s,
            %(forum_posts)s, %(late_submissions)s, %(help_requests)s,
            %(total_enrollments)s
        )
        """
        
        # Convert DataFrame to list of dicts
        records = df.to_dict('records')
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            print(f"  Inserted {min(i+batch_size, len(records))}/{len(records)} students...")
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) as count FROM students")
        result = cursor.fetchone()
        count = result['count']
        
        print(f"\n✅ Successfully imported {count} students!")
        
        # Show statistics
        cursor.execute("""
            SELECT 
                AVG(attendance_rate) as avg_attendance,
                MIN(attendance_rate) as min_attendance,
                MAX(attendance_rate) as max_attendance,
                SUM(CASE WHEN attendance_rate < 67 THEN 1 ELSE 0 END) as below_threshold
            FROM students
        """)
        stats = cursor.fetchone()
        
        print("\n" + "=" * 70)
        print("DATABASE STATISTICS:")
        print("=" * 70)
        print(f"Total students:           {count}")
        print(f"Mean attendance:          {stats['avg_attendance']:.1f}%")
        print(f"Min attendance:           {stats['min_attendance']:.1f}%")
        print(f"Max attendance:           {stats['max_attendance']:.1f}%")
        print(f"Students < 67%:           {stats['below_threshold']} ({stats['below_threshold']/count*100:.1f}%)")
        print(f"Students >= 67%:          {count - stats['below_threshold']} ({(count - stats['below_threshold'])/count*100:.1f}%)")
        
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Restart your Flask API:")
        print("   cd ~/student-analytics-platform/analytics")
        print("   python api/app.py")
        print("\n2. Open your dashboard and check predictions!")
        print("\n✅ Your dashboard should now show realistic risk distribution!")
        
    except Exception as e:
        print(f"\n❌ ERROR during import: {e}")
        connection.rollback()
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
