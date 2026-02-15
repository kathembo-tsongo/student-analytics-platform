"""
Train ML Models on Historical Data
===================================
"""
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

print("\n" + "🤖" * 35)
print("MODEL TRAINING - HISTORICAL DATA")
print("🤖" * 35 + "\n")

# Create models directory
Path('models/saved_models').mkdir(parents=True, exist_ok=True)

# Load data
print("📂 Loading historical data...")
train_df = pd.read_csv('data/historical/train_cohort_2021.csv')
test_df = pd.read_csv('data/historical/test_cohort_2021.csv')

print(f"   ✅ Training set: {len(train_df):,} students")
print(f"   ✅ Test set: {len(test_df):,} students\n")

# Features (Year 1 Semester 1 indicators)
feature_columns = [
    'y1s1_attendance_rate',
    'y1s1_gpa',
    'y1s1_avg_grade',
    'y1s1_lms_activities',
    'y1s1_courses_enrolled',
    'y1s1_exam_eligible',
    'y1s1_attendance_below_67',
    'y1s1_gpa_below_2',
    'y1s1_grade_below_40',
    'y1s1_low_engagement'
]

# Prepare features
X_train = train_df[feature_columns].fillna(0)
X_test = test_df[feature_columns].fillna(0)

print(f"📊 Using {len(feature_columns)} features")

# Targets to predict
targets = [
    ('Dropout Risk', 'dropped_out'),
    ('Course Failure Risk', 'failed_courses'),
    ('Delayed Graduation Risk', 'delayed_graduation')
]

# Train for each target
for target_name, target_col in targets:
    print(f"\n{'='*70}")
    print(f"🎯 Training: {target_name}")
    print('='*70)
    
    # Get target variable
    y_train = train_df[target_col].fillna(0)
    y_test = test_df[target_col].fillna(0)
    
    print(f"\n   Target distribution (training):")
    train_counts = y_train.value_counts().to_dict()
    print(f"      No Risk (0): {train_counts.get(0, 0):,}")
    print(f"      At Risk (1): {train_counts.get(1, 0):,}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print(f"\n🌲 Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        class_weight='balanced',  # Handle imbalanced data
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluate
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\n📊 Results:")
    print(f"   Accuracy:  {acc:.3f}")
    print(f"   Precision: {prec:.3f}")
    print(f"   Recall:    {rec:.3f} ⭐ (catching at-risk students)")
    print(f"   F1-Score:  {f1:.3f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\n📈 Confusion Matrix:")
    print(f"   True Negatives:  {tn:4d} (correctly predicted no risk)")
    print(f"   False Positives: {fp:4d} (false alarms - OK for intervention!)")
    print(f"   False Negatives: {fn:4d} (MISSED at-risk - want this LOW!)")
    print(f"   True Positives:  {tp:4d} (correctly caught at-risk) ✅")
    
    # Feature Importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:5]
    
    print(f"\n🔝 Top 5 Important Features:")
    for i, idx in enumerate(indices, 1):
        print(f"   {i}. {feature_columns[idx]:30s} {importances[idx]:.3f}")
    
    # Save models
    model_file = f'models/saved_models/{target_col}_model.pkl'
    scaler_file = f'models/saved_models/{target_col}_scaler.pkl'
    
    joblib.dump(model, model_file)
    joblib.dump(scaler, scaler_file)
    
    print(f"\n💾 Saved:")
    print(f"   {model_file}")
    print(f"   {scaler_file}")

print("\n" + "="*70)
print("✅ MODEL TRAINING COMPLETE!")
print("="*70)
print("\n📁 All models saved in: models/saved_models/")
print("\n👉 Next step: Run predictions")
print("   python predict_student.py")
print("\n")
