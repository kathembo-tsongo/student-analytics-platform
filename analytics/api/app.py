from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.db_connection import DatabaseConnection
from models.dropout_predictor import DropoutRiskPredictor
from models.course_failure_predictor import CourseFailurePredictor
from models.program_delay_predictor import ProgramDelayPredictor
from models.risk_scorer import ComprehensiveRiskScorer
from utils.feature_mapper import map_db_to_model_features
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Initialize database connection
db = DatabaseConnection()

# Initialize models
dropout_model = DropoutRiskPredictor()
course_model = CourseFailurePredictor()
delay_model = ProgramDelayPredictor()

# Load pre-trained models
dropout_model.load()
course_model.load()
delay_model.load()

# Initialize comprehensive scorer
risk_scorer = ComprehensiveRiskScorer(dropout_model, course_model, delay_model)

@app.route('/')
def home():
    return jsonify({
        'message': 'Strathmore Analytics ML API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models': {
            'dropout': dropout_model.model is not None,
            'course_failure': course_model.model is not None,
            'program_delay': delay_model.model is not None
        }
    })

@app.route('/api/predict/student/<int:student_id>', methods=['GET'])
def predict_student_risk(student_id):
    """Get comprehensive risk prediction for a student"""
    try:
        # Get student data
        student_data = db.get_student_data(student_id=student_id)
        
        if student_data.empty:
            return jsonify({'error': 'Student not found'}), 404
        
        # Map database features to model features
        student_data = map_db_to_model_features(student_data)
        
        # Get comprehensive risk assessment
        result = risk_scorer.calculate_comprehensive_score(student_data)
        
        # Handle list or single result
        if isinstance(result, list):
            result = result[0]
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/school/<int:school_id>', methods=['GET'])
def predict_school_risks(school_id):
    """Get risk predictions for all students in a school"""
    try:
        # Get all students in school
        query = f"""
        SELECT s.id as student_id,
               s.student_code,
               s.program_id,
               s.school_id,
               s.year_of_study,
               s.gpa,
               s.status,
               DATEDIFF(CURDATE(), s.enrollment_date) as days_enrolled,
               COUNT(DISTINCT se.id) as total_enrollments,
               AVG(se.grade_points) as avg_grade_points,
               SUM(CASE WHEN se.is_repeating = 1 THEN 1 ELSE 0 END) as repeat_courses,
               AVG(lms.login_count) as avg_login_count,
               AVG(lms.time_spent_minutes) as avg_time_spent,
               AVG(lms.assignments_submitted / NULLIF(lms.assignments_total, 0)) as assignment_completion_rate,
               AVG(lms.avg_assignment_score) as avg_assignment_score,
               AVG(lms.engagement_score) as avg_engagement_score,
               COUNT(DISTINCT ar.id) as total_attendance_records,
               SUM(CASE WHEN ar.status = 'present' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(ar.id), 0) as attendance_rate,
               MAX(ar.consecutive_absences) as max_consecutive_absences,
               AVG(ar.consecutive_absences) as avg_consecutive_absences
        FROM students s
        LEFT JOIN sis_enrollments se ON s.id = se.student_id
        LEFT JOIN lms_activities lms ON s.id = lms.student_id
        LEFT JOIN attendance_records ar ON s.id = ar.student_id
        WHERE s.school_id = {school_id}
        GROUP BY s.id
        """
        
        students_data = db.query_to_dataframe(query)
        
        if students_data.empty:
            return jsonify({'students': []})
        
        # Map features
        students_data = map_db_to_model_features(students_data)
        
        # Get predictions
        results = risk_scorer.calculate_comprehensive_score(students_data)
        
        # Sort by risk score
        if isinstance(results, list):
            results.sort(key=lambda x: x['overall_risk_score'], reverse=True)
        
        return jsonify({
            'school_id': school_id,
            'total_students': len(results),
            'high_risk_count': len([r for r in results if r.get('overall_risk_level') in ['CRITICAL', 'HIGH']]),
            'students': results
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get overall risk statistics for dashboard"""
    try:
        # Get all students data
        students_data = db.get_student_data()
        
        if students_data.empty:
            return jsonify({'error': 'No student data available'}), 404
        
        # Map features
        students_data = map_db_to_model_features(students_data)
        
        # Get all predictions
        results = risk_scorer.calculate_comprehensive_score(students_data)
        
        # Calculate statistics
        stats = {
            'total_students': len(results),
            'critical_risk': len([r for r in results if r.get('overall_risk_level') == 'CRITICAL']),
            'high_risk': len([r for r in results if r.get('overall_risk_level') == 'HIGH']),
            'medium_risk': len([r for r in results if r.get('overall_risk_level') == 'MEDIUM']),
            'low_risk': len([r for r in results if r.get('overall_risk_level') == 'LOW']),
            'avg_risk_score': round(sum(r.get('overall_risk_score', 0) for r in results) / len(results), 2) if results else 0,
            'students_needing_intervention': len([r for r in results if r.get('overall_risk_level') in ['CRITICAL', 'HIGH']])
        }
        
        return jsonify(stats)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
