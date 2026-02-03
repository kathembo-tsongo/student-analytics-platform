import sys
sys.path.append('api')

from api.utils.db_connection import DatabaseConnection
from api.models.dropout_predictor import DropoutRiskPredictor
from api.models.course_failure_predictor import CourseFailurePredictor
from api.models.program_delay_predictor import ProgramDelayPredictor

def train_all_models():
    print("=" * 60)
    print("STRATHMORE ANALYTICS - MODEL TRAINING")
    print("=" * 60)
    
    # Initialize database connection
    print("\n📊 Connecting to database...")
    db = DatabaseConnection()
    
    # Get student data
    print("📥 Fetching student data...")
    student_data = db.get_student_data()
    print(f"✅ Loaded {len(student_data)} student records")
    
    # Prepare features
    print("\n🔧 Preparing features...")
    
    # 1. Train Dropout Risk Model
    print("\n" + "=" * 60)
    print("1️⃣  TRAINING DROPOUT RISK MODEL")
    print("=" * 60)
    dropout_model = DropoutRiskPredictor()
    X_dropout = dropout_model.prepare_features(student_data)
    y_dropout = dropout_model.create_target(student_data)
    print(f"At-risk students: {y_dropout.sum()} / {len(y_dropout)} ({y_dropout.mean()*100:.1f}%)")
    dropout_metrics = dropout_model.train(X_dropout, y_dropout, model_type='random_forest')
    dropout_model.save()
    
    # 2. Train Course Failure Model
    print("\n" + "=" * 60)
    print("2️⃣  TRAINING COURSE FAILURE MODEL")
    print("=" * 60)
    course_model = CourseFailurePredictor()
    X_course = course_model.prepare_features(student_data)
    y_course = course_model.create_target(student_data)
    print(f"Students at risk of failing: {y_course.sum()} / {len(y_course)} ({y_course.mean()*100:.1f}%)")
    course_metrics = course_model.train(X_course, y_course, model_type='random_forest')
    course_model.save()
    
    # 3. Train Program Delay Model
    print("\n" + "=" * 60)
    print("3️⃣  TRAINING PROGRAM DELAY MODEL")
    print("=" * 60)
    delay_model = ProgramDelayPredictor()
    X_delay = delay_model.prepare_features(student_data)
    y_delay = delay_model.create_target(student_data)
    print(f"Students at risk of delay: {y_delay.sum()} / {len(y_delay)} ({y_delay.mean()*100:.1f}%)")
    delay_metrics = delay_model.train(X_delay, y_delay, model_type='random_forest')
    delay_model.save()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 60)
    print("\nModel Performance Summary:")
    print(f"\n1. Dropout Risk Model:")
    print(f"   - Accuracy: {dropout_metrics['accuracy']:.4f}")
    print(f"   - F1 Score: {dropout_metrics['f1_score']:.4f}")
    print(f"\n2. Course Failure Model:")
    print(f"   - Accuracy: {course_metrics['accuracy']:.4f}")
    print(f"   - F1 Score: {course_metrics['f1_score']:.4f}")
    print(f"\n3. Program Delay Model:")
    print(f"   - Accuracy: {delay_metrics['accuracy']:.4f}")
    print(f"   - F1 Score: {delay_metrics['f1_score']:.4f}")
    
    print("\n🎉 Models saved and ready for predictions!")

if __name__ == "__main__":
    train_all_models()
