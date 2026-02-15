
import pandas as pd
import joblib
import numpy as np
import argparse
from pathlib import Path

print("\n" + "🔮" * 35)
print("STUDENT RISK PREDICTION SYSTEM")
print("🔮" * 35 + "\n")

# Load models
print("📂 Loading trained models...")

try:
    dropout_model = joblib.load('models/saved_models/dropped_out_model.pkl')
    dropout_scaler = joblib.load('models/saved_models/dropped_out_scaler.pkl')
    print("   ✅ Dropout model loaded")
except:
    print("   ❌ Dropout model not found")
    exit(1)

try:
    failure_model = joblib.load('models/saved_models/failed_courses_model.pkl')
    failure_scaler = joblib.load('models/saved_models/failed_courses_scaler.pkl')
    print("   ✅ Failure model loaded")
except:
    failure_model = None

try:
    delay_model = joblib.load('models/saved_models/delayed_graduation_model.pkl')
    delay_scaler = joblib.load('models/saved_models/delayed_graduation_scaler.pkl')
    print("   ✅ Delay model loaded")
except:
    delay_model = None

print()


def prepare_features_from_current_data(df):
    """
    Map current data features to historical training features
    """
    features = pd.DataFrame()
    
    # Map to historical feature names
    features['y1s1_attendance_rate'] = df['physical_attendance_rate']
    features['y1s1_gpa'] = df['cumulative_gpa']
    features['y1s1_avg_grade'] = df['avg_grade']
    features['y1s1_lms_activities'] = df['lms_activity_count']
    features['y1s1_courses_enrolled'] = df['courses_enrolled']
    features['y1s1_exam_eligible'] = df['exam_eligible']
    features['y1s1_attendance_below_67'] = (df['physical_attendance_rate'] < 0.67).astype(int)
    features['y1s1_gpa_below_2'] = (df['cumulative_gpa'] < 2.0).astype(int)
    features['y1s1_grade_below_40'] = (df['avg_grade'] < 40).astype(int)
    features['y1s1_low_engagement'] = df['low_lms_engagement']
    
    return features.fillna(0)


def get_risk_level(probability):
    if probability >= 0.7:
        return "🔴 CRITICAL"
    elif probability >= 0.5:
        return "🟠 HIGH"
    elif probability >= 0.3:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"


def predict_from_csv(filepath, limit=20):
    """Predict risk for students"""
    
    print(f"📂 Loading students from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"   ✅ Loaded {len(df):,} students\n")
    
    # Prepare features (map to historical format)
    features = prepare_features_from_current_data(df)
    
    # Scale features
    features_scaled = dropout_scaler.transform(features)
    
    # Predict dropout risk
    dropout_probs = dropout_model.predict_proba(features_scaled)[:, 1]
    df['dropout_probability'] = dropout_probs
    df['dropout_risk_level'] = df['dropout_probability'].apply(get_risk_level)
    
    # Sort by risk
    df_sorted = df.sort_values('dropout_probability', ascending=False)
    
    # Show high-risk students
    high_risk = df_sorted[df_sorted['dropout_probability'] >= 0.5]
    
    print("=" * 70)
    print(f"🚨 HIGH RISK STUDENTS ({len(high_risk)} found)")
    print("=" * 70 + "\n")
    
    if len(high_risk) > 0:
        display_df = high_risk[[
            'student_id', 'name', 'class_level',
            'physical_attendance_rate', 'cumulative_gpa',
            'dropout_probability', 'dropout_risk_level'
        ]].head(limit)
        
        print(display_df.to_string(index=False))
        
        # Save predictions
        print(f"\n💾 Saving predictions to: predictions_output.csv")
        df_sorted[[
            'student_id', 'name', 'class_level', 'school_id',
            'physical_attendance_rate', 'cumulative_gpa', 'avg_grade',
            'dropout_probability', 'dropout_risk_level'
        ]].to_csv('predictions_output.csv', index=False)
        print("   ✅ Saved!\n")
    else:
        print("   ✅ No high-risk students found!\n")
    
    return df_sorted


def predict_single_student(student_data):
    """Predict for single student"""
    
    print("=" * 70)
    print("STUDENT RISK ASSESSMENT")
    print("=" * 70)
    
    print(f"\n📋 Student Information:")
    print(f"   Student ID: {student_data.get('student_id', 'N/A')}")
    print(f"   Name: {student_data.get('name', 'N/A')}")
    print(f"   Class Level: {student_data.get('class_level', 'N/A')}")
    
    print(f"\n📊 Academic Indicators:")
    print(f"   Attendance: {student_data.get('physical_attendance_rate', 0):.1%}")
    print(f"   GPA: {student_data.get('cumulative_gpa', 0):.2f}")
    print(f"   Grade: {student_data.get('avg_grade', 0):.1f}%")
    print(f"   LMS Activities: {student_data.get('lms_activity_count', 0):.0f}")
    
    # Prepare features
    temp_df = pd.DataFrame([student_data])
    features = prepare_features_from_current_data(temp_df)
    features_scaled = dropout_scaler.transform(features)
    
    # Predict
    dropout_prob = dropout_model.predict_proba(features_scaled)[0][1]
    
    print(f"\n" + "=" * 70)
    print("🎯 DROPOUT RISK PREDICTION")
    print("=" * 70)
    print(f"\n   Probability: {dropout_prob:.1%}")
    print(f"   Risk Level: {get_risk_level(dropout_prob)}")
    
    if dropout_prob >= 0.5:
        print(f"\n   ⚠️  ACTION REQUIRED: High dropout risk!")
    
    # Recommendations
    print(f"\n" + "=" * 70)
    print("💡 INTERVENTIONS")
    print("=" * 70)
    
    if student_data.get('physical_attendance_rate', 1) < 0.67:
        print("\n   🚨 Attendance below 67% - Immediate meeting required")
    if student_data.get('cumulative_gpa', 4) < 2.0:
        print("   📚 GPA below 2.0 - Academic counseling needed")
    if student_data.get('avg_grade', 100) < 40:
        print("   ⚠️  Grade below 40% - Tutoring support")
    if dropout_prob >= 0.7:
        print("   🔴 CRITICAL RISK - Dean intervention")
    
    print("\n" + "=" * 70 + "\n")


# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='CSV file')
    parser.add_argument('--student-id', type=str, help='Student ID')
    parser.add_argument('--limit', type=int, default=20)
    
    args = parser.parse_args()
    
    if args.file:
        predict_from_csv(args.file, limit=args.limit)
    elif args.student_id:
        df = pd.read_csv('data/processed/features_engineered.csv')
        student = df[df['student_id'].astype(str) == args.student_id]
        if len(student) > 0:
            predict_single_student(student.iloc[0].to_dict())
        else:
            print(f"❌ Student {args.student_id} not found")
    else:
        if Path('data/processed/features_engineered.csv').exists():
            predict_from_csv('data/processed/features_engineered.csv', limit=args.limit)
        else:
            print("❌ No data file found")
