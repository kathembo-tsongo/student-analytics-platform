import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import os

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'newpassword'),
            'database': os.getenv('DB_NAME', 'strathmore_analytics'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        
    def get_connection(self):
        return mysql.connector.connect(**self.config)
    
    def get_engine(self):
        connection_string = f"mysql+mysqlconnector://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        return create_engine(connection_string)
    
    def query_to_dataframe(self, query):
        engine = self.get_engine()
        return pd.read_sql(query, engine)
    
    def get_student_data(self, student_id=None):
        """Get comprehensive student data for ML predictions"""
        query = """
        SELECT 
            s.id as student_id,
            s.student_code,
            s.program_id,
            s.school_id,
            s.year_of_study,
            s.gpa,
            s.status,
            DATEDIFF(CURDATE(), s.enrollment_date) as days_enrolled,
            
            COUNT(DISTINCT se.id) as total_enrollments,
            COALESCE(AVG(se.grade_points), 0) as avg_grade_points,
            SUM(CASE WHEN se.is_repeating = 1 THEN 1 ELSE 0 END) as repeat_courses,
            
            COALESCE(AVG(lms.login_count), 0) as avg_login_count,
            COALESCE(AVG(lms.time_spent_minutes), 0) as avg_time_spent,
            COALESCE(AVG(lms.assignments_submitted / NULLIF(lms.assignments_total, 0)), 0) as assignment_completion_rate,
            COALESCE(AVG(lms.avg_assignment_score), 0) as avg_assignment_score,
            COALESCE(AVG(lms.engagement_score), 0) as avg_engagement_score,
            
            COUNT(ar.id) as total_attendance_records,
            COALESCE(SUM(CASE WHEN ar.status = 'present' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(ar.id), 0), 0) as attendance_rate,
            COALESCE(MAX(ar.consecutive_absences), 0) as max_consecutive_absences,
            COALESCE(AVG(ar.consecutive_absences), 0) as avg_consecutive_absences
            
        FROM students s
        LEFT JOIN sis_enrollments se ON s.id = se.student_id
        LEFT JOIN lms_activities lms ON s.id = lms.student_id
        LEFT JOIN attendance_records ar ON s.id = ar.student_id
        """
        
        if student_id:
            query += f" WHERE s.id = {student_id}"
        
        query += " GROUP BY s.id"
        
        return self.query_to_dataframe(query)
