import sys
sys.path.insert(0, 'api')
from utils.db_connection import DatabaseConnection
import pandas as pd

db = DatabaseConnection()
students = db.get_student_data()

print("=== DATA DISTRIBUTION ===")
print(f"\nTotal Students: {len(students)}")
print(f"\nAttendance Rate:")
print(students['attendance_rate'].describe())
print(f"\nEngagement Score:")
print(students['avg_engagement_score'].describe())
print(f"\nAssignment Completion:")
print(students['assignment_completion_rate'].describe())
print(f"\nLogin Count:")
print(students['avg_login_count'].describe())

# Show percentiles
print("\n=== PERCENTILES ===")
print(f"Attendance 25th percentile: {students['attendance_rate'].quantile(0.25):.1f}%")
print(f"Engagement 25th percentile: {students['avg_engagement_score'].quantile(0.25):.1f}")
print(f"Completion 25th percentile: {students['assignment_completion_rate'].quantile(0.25):.2f}")
