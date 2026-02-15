"""
Versioned Model Training
========================
Saves models with timestamps so you don't lose previous versions
"""
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Create version timestamp
version = datetime.now().strftime("%Y%m%d_%H%M%S")
print(f"\n🤖 TRAINING MODELS - Version: {version}\n")

# Create versioned directory
version_dir = Path(f'models/saved_models/v_{version}')
version_dir.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv('data/processed/features_engineered.csv')
print(f"✅ Loaded {len(df):,} students")

# Features
features = [
    'physical_attendance_rate', 'cumulative_gpa', 'avg_grade',
    'lms_activity_count', 'courses_enrolled', 'exam_eligible',
    'gpa_below_2.0', 'grade_below_40', 'low_lms_engagement'
]

results = {}

# Train for each target
for target_name, target_col in [
    ('Dropout', 'dropout_risk'),
    ('Failure', 'failure_risk'),
    ('Delay', 'delay_risk')
]:
    print(f"\n{'='*60}")
    print(f"Training: {target_name}")
    print('='*60)
    
    X = df[features].fillna(0)
    y = df[target_col].fillna(0)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"Accuracy:  {acc:.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall:    {rec:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    
    results[target_name] = {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}
    
    # Save to versioned directory
    joblib.dump(model, version_dir / f'{target_col}_model.pkl')
    joblib.dump(scaler, version_dir / f'{target_col}_scaler.pkl')
    
    # Also save to main directory (latest)
    joblib.dump(model, f'models/saved_models/{target_col}_model.pkl')
    joblib.dump(scaler, f'models/saved_models/{target_col}_scaler.pkl')
    
    print(f"✅ Saved to: {version_dir}")

# Save training report
report = f"""
TRAINING REPORT
===============
Version: {version}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Students: {len(df):,}
Features: {len(features)}

RESULTS:
--------
Dropout Risk:
  Accuracy:  {results['Dropout']['accuracy']:.3f}
  Precision: {results['Dropout']['precision']:.3f}
  Recall:    {results['Dropout']['recall']:.3f}
  F1-Score:  {results['Dropout']['f1']:.3f}

Failure Risk:
  Accuracy:  {results['Failure']['accuracy']:.3f}
  Precision: {results['Failure']['precision']:.3f}
  Recall:    {results['Failure']['recall']:.3f}
  F1-Score:  {results['Failure']['f1']:.3f}

Delay Risk:
  Accuracy:  {results['Delay']['accuracy']:.3f}
  Precision: {results['Delay']['precision']:.3f}
  Recall:    {results['Delay']['recall']:.3f}
  F1-Score:  {results['Delay']['f1']:.3f}
"""

with open(version_dir / 'training_report.txt', 'w') as f:
    f.write(report)

print("\n" + "="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
print(f"\n📂 Models saved in:")
print(f"   Latest: models/saved_models/")
print(f"   Version: {version_dir}")
print(f"\n📊 Report saved: {version_dir}/training_report.txt\n")
