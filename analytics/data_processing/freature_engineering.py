

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/feature_engineering.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Creates ML features from available Strathmore data"""
    
    def __init__(self, processed_path='data/processed'):
        self.processed_path = Path(processed_path)
        
        # Strathmore policy thresholds
        self.ATTENDANCE_THRESHOLD = 0.67  # 67% attendance required
        self.GPA_THRESHOLD = 2.0           # Minimum GPA 2.0
        self.PASS_GRADE = 40.0             # 40% minimum to pass
        
        logger.info("=" * 70)
        logger.info("🔧 FEATURE ENGINEERING (Simplified - Available Data Only)")
        logger.info("=" * 70)
    
    def load_clean_data(self):
        """Load cleaned data"""
        logger.info("\n📂 Loading clean data...")
        
        filepath = self.processed_path / 'strathmore_clean_data.csv'
        
        if not filepath.exists():
            raise FileNotFoundError(
                f"Clean data not found. Run data_cleaning.py first."
            )
        
        df = pd.read_csv(filepath)
        logger.info(f"   ✅ Loaded {len(df)} students with {len(df.columns)} features")
        
        return df
    
    def create_attendance_features(self, df):
        """
        Physical attendance features (what we actually have!)
        """
        logger.info("\n✋ Creating attendance features...")
        
        df = df.copy()
        
        # 1. Exam Eligibility (67% requirement)
        df['exam_eligible'] = (
            df['physical_attendance_rate'] >= self.ATTENDANCE_THRESHOLD
        ).astype(int)
        
        # 2. Attendance Category
        def categorize_attendance(rate):
            if pd.isna(rate):
                return 'Unknown'
            elif rate >= 0.90:
                return 'Excellent'
            elif rate >= 0.75:
                return 'Good'
            elif rate >= 0.67:
                return 'Borderline'
            else:
                return 'At Risk'
        
        df['attendance_category'] = df['physical_attendance_rate'].apply(
            categorize_attendance
        )
        
        # 3. Attendance compliance
        df['attendance_compliant'] = (
            df['physical_attendance_rate'] >= self.ATTENDANCE_THRESHOLD
        ).astype(int)
        
        logger.info(f"   ✅ Created 3 attendance features")
        logger.info(f"      Exam eligible: {df['exam_eligible'].sum():,}")
        logger.info(f"      At Risk: {(df['attendance_category'] == 'At Risk').sum():,}")
        
        return df
    
    def create_academic_features(self, df):
        """
        Academic performance features (from grades & GPA)
        """
        logger.info("\n📚 Creating academic features...")
        
        df = df.copy()
        
        # 1. GPA compliance
        df['gpa_below_2.0'] = (df['cumulative_gpa'] < self.GPA_THRESHOLD).astype(int)
        
        # 2. Grade compliance
        df['grade_below_40'] = (df['avg_grade'] < self.PASS_GRADE).astype(int)
        
        # 3. Performance Category
        def categorize_performance(gpa):
            if pd.isna(gpa):
                return 'Unknown'
            elif gpa >= 3.5:
                return 'Excellent'
            elif gpa >= 3.0:
                return 'Good'
            elif gpa >= 2.5:
                return 'Average'
            elif gpa >= 2.0:
                return 'Below Average'
            else:
                return 'Poor'
        
        df['performance_category'] = df['cumulative_gpa'].apply(
            categorize_performance
        )
        
        # 4. Academic at-risk flag
        df['academic_at_risk'] = (
            (df['cumulative_gpa'] < 2.5) | 
            (df['avg_grade'] < 50)
        ).astype(int)
        
        logger.info(f"   ✅ Created 4 academic features")
        logger.info(f"      GPA below 2.0: {df['gpa_below_2.0'].sum():,}")
        logger.info(f"      Grade below 40%: {df['grade_below_40'].sum():,}")
        logger.info(f"      Academic at-risk: {df['academic_at_risk'].sum():,}")
        
        return df
    
    def create_lms_features(self, df):
        """
        LMS engagement features (from lms_activities.csv)
        """
        logger.info("\n💻 Creating LMS engagement features...")
        
        df = df.copy()
        
        # 1. LMS Engagement Index (0-100)
        max_activities = df['lms_activity_count'].quantile(0.95)
        df['lms_engagement_index'] = (
            (df['lms_activity_count'] / max_activities * 100).clip(0, 100)
        )
        
        # 2. Low engagement flag
        df['low_lms_engagement'] = (
            df['lms_activity_count'] < df['lms_activity_count'].quantile(0.25)
        ).astype(int)
        
        # 3. Engagement Category
        def categorize_engagement(index):
            if pd.isna(index):
                return 'Unknown'
            elif index >= 75:
                return 'High'
            elif index >= 50:
                return 'Medium'
            elif index >= 25:
                return 'Low'
            else:
                return 'Very Low'
        
        df['engagement_category'] = df['lms_engagement_index'].apply(
            categorize_engagement
        )
        
        logger.info(f"   ✅ Created 3 LMS features")
        logger.info(f"      Low engagement: {df['low_lms_engagement'].sum():,}")
        logger.info(f"      High engagement: {(df['engagement_category'] == 'High').sum():,}")
        
        return df
    
    def create_policy_compliance_features(self, df):
        """
        Strathmore policy compliance indicators
        """
        logger.info("\n📋 Creating policy compliance features...")
        
        df = df.copy()
        
        # 1. Overall compliance score (0-3, higher is better)
        df['compliance_score'] = (
            df['attendance_compliant'] + 
            (1 - df['gpa_below_2.0']) + 
            (1 - df['grade_below_40'])
        )
        
        # 2. Multiple violations flag
        df['multiple_violations'] = (
            (df['attendance_compliant'] == 0) & 
            ((df['gpa_below_2.0'] == 1) | (df['grade_below_40'] == 1))
        ).astype(int)
        
        logger.info(f"   ✅ Created 2 compliance features")
        logger.info(f"      Multiple violations: {df['multiple_violations'].sum():,}")
        
        return df
    
    def create_risk_score(self, df):
        """
        Overall risk scoring (0-10 scale)
        """
        logger.info("\n⚠️  Creating risk scores...")
        
        df = df.copy()
        
        risk_score = 0
        
        # Attendance risk (0-3 points)
        risk_score += (df['physical_attendance_rate'] < 0.67) * 3
        risk_score += (
            (df['physical_attendance_rate'] >= 0.67) & 
            (df['physical_attendance_rate'] < 0.75)
        ) * 1
        
        # Academic risk (0-4 points)
        risk_score += (df['cumulative_gpa'] < 2.0) * 4
        risk_score += (
            (df['cumulative_gpa'] >= 2.0) & 
            (df['cumulative_gpa'] < 2.5)
        ) * 2
        
        # LMS engagement risk (0-3 points)
        risk_score += (df['low_lms_engagement'] == 1) * 3
        
        df['overall_risk_score'] = risk_score
        
        # Risk Level Category
        def categorize_risk(score):
            if score >= 7:
                return 'Critical'
            elif score >= 5:
                return 'High'
            elif score >= 3:
                return 'Medium'
            else:
                return 'Low'
        
        df['risk_level'] = df['overall_risk_score'].apply(categorize_risk)
        
        logger.info(f"   ✅ Created 2 risk features")
        logger.info(f"      Critical: {(df['risk_level'] == 'Critical').sum():,}")
        logger.info(f"      High: {(df['risk_level'] == 'High').sum():,}")
        logger.info(f"      Medium: {(df['risk_level'] == 'Medium').sum():,}")
        logger.info(f"      Low: {(df['risk_level'] == 'Low').sum():,}")
        
        return df
    
    def create_target_variables(self, df):
        """
        TARGET VARIABLES for ML models
        """
        logger.info("\n🎯 Creating target variables...")
        
        df = df.copy()
        
        # 1. DROPOUT RISK
        dropout_score = 0
        dropout_score += (df['physical_attendance_rate'] < 0.67) * 5
        dropout_score += (df['cumulative_gpa'] < 2.0) * 4
        dropout_score += (df['low_lms_engagement'] == 1) * 3
        
        df['dropout_risk_score'] = dropout_score
        df['dropout_risk'] = (dropout_score >= 6).astype(int)
        
        # 2. COURSE FAILURE RISK
        failure_score = 0
        failure_score += (df['physical_attendance_rate'] < 0.67) * 4
        failure_score += (df['avg_grade'] < 40) * 3
        failure_score += (df['cumulative_gpa'] < 2.0) * 3
        
        df['failure_risk_score'] = failure_score
        df['failure_risk'] = (failure_score >= 5).astype(int)
        
        # 3. PROGRAM DELAY RISK
        delay_score = 0
        delay_score += (df['cumulative_gpa'] < 2.5) * 2
        delay_score += (df['courses_enrolled'] < 4) * 3
        delay_score += (df['avg_grade'] < 50) * 2
        
        df['delay_risk_score'] = delay_score
        df['delay_risk'] = (delay_score >= 4).astype(int)
        
        logger.info(f"   ✅ Created 6 target variables")
        logger.info(f"\n   📊 Target Distribution:")
        logger.info(f"      Dropout Risk: {df['dropout_risk'].sum():,} ({df['dropout_risk'].mean():.1%})")
        logger.info(f"      Failure Risk: {df['failure_risk'].sum():,} ({df['failure_risk'].mean():.1%})")
        logger.info(f"      Delay Risk: {df['delay_risk'].sum():,} ({df['delay_risk'].mean():.1%})")
        
        return df
    
    def engineer_features(self):
        """MAIN: Run complete feature engineering"""
        try:
            # Load data
            df = self.load_clean_data()
            
            # Create features
            df = self.create_attendance_features(df)
            df = self.create_academic_features(df)
            df = self.create_lms_features(df)
            df = self.create_policy_compliance_features(df)
            df = self.create_risk_score(df)
            df = self.create_target_variables(df)
            
            # Summary
            logger.info("\n" + "=" * 70)
            logger.info("📊 FEATURE ENGINEERING COMPLETE")
            logger.info("=" * 70)
            logger.info(f"\n   Total Features: {len(df.columns)}")
            logger.info(f"   New Features Created: ~20")
            logger.info(f"   Students: {len(df):,}")
            
            # Save
            output_path = self.processed_path / 'features_engineered.csv'
            df.to_csv(output_path, index=False)
            
            logger.info(f"\n💾 Saved to: {output_path}")
            logger.info(f"   Size: {output_path.stat().st_size / 1024**2:.2f} MB")
            
            return df
            
        except Exception as e:
            logger.error(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    print("\n" + "🔧" * 35)
    print("WEEK 2: FEATURE ENGINEERING")
    print("Using Available Data Only (No Zoom/Meet Required!)")
    print("🔧" * 35 + "\n")
    
    Path('logs').mkdir(exist_ok=True)
    
    engineer = FeatureEngineer()
    df = engineer.engineer_features()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Features ready for ML training")
    print("=" * 70)
    print("\n📊 Preview:")
    print(df[['student_id', 'risk_level', 'dropout_risk', 'failure_risk']].head(10))
    
    print("\n👉 Next Steps:")
    print("   1. Review: data/processed/features_engineered.csv")
    print("   2. Check: logs/feature_engineering.log")
    print("   3. Move to: Week 3 - Model Training!")
    print("\n")
    
    return df


if __name__ == "__main__":
    df = main()