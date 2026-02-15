"""
Train ML Model - Using Existing Features
"""
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

print("\n🤖 TRAINING MODEL\n")

# Create directories
Path('../../models/saved_models').mkdir(parents=True, exist_ok=True)
Path('../../models/evaluation').mkdir(parents=True, exist_ok=True)

# Load data
print("📂 Loading data...")
train_df = pd.read_csv('data/historical/train_cohort_2021.csv')
test_df = pd.read_csv('data/historical/test_cohort_2021.csv')
print(f"   ✅ Loaded {len(df):,} students")

# Features
feature_columns = [
    'physical_attendance_rate',
    'cumulative_gpa',
    'avg_grade',
    'lms_activity_count',
    'courses_enrolled',
    'exam_eligible',
    'gpa_below_2.0',
    'grade_below_40',
    'low_lms_engagement'
]

def train_model(target_name, target_column):
    print(f"\n{'='*70}")
    print(f"🎯 Training for: {target_name}")
    print('='*70)
    
    # Prepare data
    X = df[feature_columns].fillna(0)
    y = df[target_column].fillna(0)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n   Train: {len(X_train):,} | Test: {len(X_test):,}")
    print(f"   Target: {y_train.value_counts().to_dict()}")
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    print(f"\n🌲 Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Metrics
    print(f"\n📊 Results:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
    print(f"   Precision: {precision_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"   Recall:    {recall_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.3f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\n📈 Confusion Matrix:")
    print(f"   TN: {tn:4d} | FP: {fp:4d}")
    print(f"   FN: {fn:4d} | TP: {tp:4d}")
    
    # Feature Importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:5]
    print(f"\n🔝 Top 5 Features:")
    for i, idx in enumerate(indices, 1):
        print(f"   {i}. {feature_columns[idx]}: {importances[idx]:.3f}")
    
    # Save
    joblib.dump(model, f'../../models/saved_models/{target_column}_model.pkl')
    joblib.dump(scaler, f'../../models/saved_models/{target_column}_scaler.pkl')
    print(f"\n💾 Saved: {target_column}_model.pkl")

# Train for each target
train_model('Dropout Risk', 'dropout_risk')
train_model('Failure Risk', 'failure_risk')
train_model('Delay Risk', 'delay_risk')

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)
print("\n📁 Models saved in: models/saved_models/")
print("\n")
