import sys
sys.path.insert(0, 'api')

from utils.db_connection import DatabaseConnection
from utils.feature_mapper import map_db_to_model_features
from models.dropout_predictor import DropoutRiskPredictor
from models.course_failure_predictor import CourseFailurePredictor
from models.program_delay_predictor import ProgramDelayPredictor
from models.risk_scorer import ComprehensiveRiskScorer

print("Step 1: Loading models...")
dropout_model = DropoutRiskPredictor()
course_model = CourseFailurePredictor()
delay_model = ProgramDelayPredictor()

dropout_model.load()
course_model.load()
delay_model.load()
print("✅ Models loaded")

print("\nStep 2: Getting student data...")
db = DatabaseConnection()
student_data = db.get_student_data(student_id=1)
print(f"✅ Got data: {student_data.shape}")
print(f"Columns: {student_data.columns.tolist()}")

print("\nStep 3: Mapping features...")
mapped_data = map_db_to_model_features(student_data)
print(f"✅ Mapped data: {mapped_data.shape}")

print("\nStep 4: Creating risk scorer...")
risk_scorer = ComprehensiveRiskScorer(dropout_model, course_model, delay_model)
print("✅ Risk scorer created")

print("\nStep 5: Calculating risk...")
try:
    result = risk_scorer.calculate_comprehensive_score(mapped_data)
    print(f"✅ Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
