"""
Enhanced ML Model Training Script (Version 2)
Uses historical data with KNOWN OUTCOMES
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class EnhancedMLTrainer:
    def __init__(self, data_file='data/historical/historical_students.csv'):
        self.data_file = data_file
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        
    def load_historical_data(self):
        """Load historical data with known outcomes"""
        print("\n" + "="*60)
        print("📂 LOADING HISTORICAL DATA")
        print("="*60)
        
        df = pd.read_csv(self.data_file)
        print(f"✅ Loaded {len(df)} student records")
        print(f"\n📊 Outcome Distribution:")
        print(df['outcome'].value_counts())
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for ML training"""
        print("\n" + "="*60)
        print("🔧 PREPARING FEATURES")
        print("="*60)
        
        feature_columns = [
            'attendance_rate',
            'engagement_score',
            'assignment_completion_rate',
            'avg_assignment_score',
            'avg_grade_points',
            'avg_login_count',
            'time_spent_minutes',
            'consecutive_absences',
            'repeat_courses',
            'forum_posts',
            'late_submissions',
            'help_requests',
            'total_enrollments'
        ]
        
        self.feature_names = feature_columns
        X = df[feature_columns].copy()
        X = X.fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        
        print(f"✅ Prepared {len(feature_columns)} features")
        
        return X
    
    def train_dropout_predictor(self, df):
        """Train dropout risk prediction model"""
        print("\n" + "="*60)
        print("🎯 TRAINING DROPOUT RISK PREDICTOR")
        print("="*60)
        
        X = self.prepare_features(df)
        y = (df['outcome'] == 'dropped_out').astype(int)
        
        print(f"📊 Training Set: {len(X)} students")
        print(f"   • Dropped Out: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
        print(f"   • Did Not Drop: {len(y)-y.sum()} ({(len(y)-y.sum())/len(y)*100:.1f}%)")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n🤖 Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        print("\n📊 MODEL PERFORMANCE:")
        print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
        print(f"   Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   F1-Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        print("\n🔍 TOP 5 IMPORTANT FEATURES:")
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.head(5).iterrows():
            print(f"   {row['feature']}: {row['importance']:.4f}")
        
        joblib.dump(model, 'models/dropout_risk_model_v2.pkl')
        joblib.dump(scaler, 'models/dropout_risk_scaler_v2.pkl')
        joblib.dump(self.feature_names, 'models/dropout_risk_features_v2.pkl')
        
        print("\n✅ Model saved: models/dropout_risk_model_v2.pkl")
        
        return model, scaler, accuracy_score(y_test, y_pred)
    
    def train_course_failure_predictor(self, df):
        """Train course failure prediction model"""
        print("\n" + "="*60)
        print("📚 TRAINING COURSE FAILURE PREDICTOR")
        print("="*60)
        
        X = self.prepare_features(df)
        y = ((df['avg_grade_points'] < 2.0) | (df['repeat_courses'] >= 2)).astype(int)
        
        print(f"📊 Training Set: {len(X)} students")
        print(f"   • At Risk: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n🤖 Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        print("\n📊 MODEL PERFORMANCE:")
        print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
        print(f"   Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   F1-Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        joblib.dump(model, 'models/course_failure_model_v2.pkl')
        joblib.dump(scaler, 'models/course_failure_scaler_v2.pkl')
        joblib.dump(self.feature_names, 'models/course_failure_features_v2.pkl')
        
        print("\n✅ Model saved: models/course_failure_model_v2.pkl")
        
        return model, scaler, accuracy_score(y_test, y_pred)
    
    def train_delay_predictor(self, df):
        """Train program delay prediction model"""
        print("\n" + "="*60)
        print("⏱️  TRAINING PROGRAM DELAY PREDICTOR")
        print("="*60)
        
        X = self.prepare_features(df)
        y = ((df['outcome'] == 'dropped_out') | 
             ((df['avg_grade_points'] < 2.5) & (df['repeat_courses'] > 0))).astype(int)
        
        print(f"📊 Training Set: {len(X)} students")
        print(f"   • At Risk: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n🤖 Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        print("\n📊 MODEL PERFORMANCE:")
        print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
        print(f"   Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   F1-Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        joblib.dump(model, 'models/program_delay_model_v2.pkl')
        joblib.dump(scaler, 'models/program_delay_scaler_v2.pkl')
        joblib.dump(self.feature_names, 'models/program_delay_features_v2.pkl')
        
        print("\n✅ Model saved: models/program_delay_model_v2.pkl")
        
        return model, scaler, accuracy_score(y_test, y_pred)
    
    def generate_summary_report(self, results):
        """Generate training summary"""
        print("\n" + "="*60)
        print("📊 TRAINING SUMMARY")
        print("="*60)
        
        print("\n🎯 MODEL ACCURACIES:")
        for model_name, accuracy in results.items():
            print(f"   {model_name}: {accuracy:.2%}")
        
        print("\n✅ All models trained!")
        print("\n📁 SAVED FILES:")
        print("   • dropout_risk_model_v2.pkl")
        print("   • course_failure_model_v2.pkl")
        print("   • program_delay_model_v2.pkl")
        print("   • (+ scalers and features)")
        print("="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("🤖 ENHANCED ML MODEL TRAINING (V2)")
    print("📚 Training on Historical Data")
    print("="*60)
    
    trainer = EnhancedMLTrainer()
    df = trainer.load_historical_data()
    
    results = {}
    
    _, _, acc1 = trainer.train_dropout_predictor(df)
    results['Dropout Risk'] = acc1
    
    _, _, acc2 = trainer.train_course_failure_predictor(df)
    results['Course Failure'] = acc2
    
    _, _, acc3 = trainer.train_delay_predictor(df)
    results['Program Delay'] = acc3
    
    trainer.generate_summary_report(results)
    
    print("🎉 TRAINING COMPLETE!\n")

if __name__ == "__main__":
    main()
