"""
Week 1: Data Cleaning & Merging
================================
Cleans and merges all Strathmore data into a unified ML-ready dataset.

This script:
1. Loads raw CSV files
2. Cleans each dataset (remove duplicates, handle missing values)
3. Aggregates attendance and LMS data by student
4. Merges everything into one unified dataset
5. Saves clean data for ML model training

Usage:
    python analytics/data_processing/data_cleaning.py

Output:
    data/processed/strathmore_clean_data.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_cleaning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StrathmoreDataCleaner:
    """Cleans and merges Strathmore University data"""
    
    def __init__(self, raw_data_path='data/raw', processed_path='data/processed'):
        self.raw_path = Path(raw_data_path)
        self.processed_path = Path(processed_path)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("=" * 70)
        logger.info("🧹 STRATHMORE DATA CLEANING & MERGING")
        logger.info("=" * 70)
    
    def load_raw_data(self):
        """Load all raw CSV files"""
        logger.info("\n📂 Loading raw data files...")
        
        data = {}
        
        try:
            # Load each CSV file
            data['students'] = pd.read_csv(self.raw_path / 'students.csv')
            logger.info(f"   ✅ students.csv: {len(data['students'])} records")
            
            data['courses'] = pd.read_csv(self.raw_path / 'courses.csv')
            logger.info(f"   ✅ courses.csv: {len(data['courses'])} records")
            
            data['enrollments'] = pd.read_csv(self.raw_path / 'sis_enrollments.csv')
            logger.info(f"   ✅ sis_enrollments.csv: {len(data['enrollments'])} records")
            
            data['attendance'] = pd.read_csv(self.raw_path / 'attendance_records.csv')
            logger.info(f"   ✅ attendance_records.csv: {len(data['attendance'])} records")
            
            data['lms'] = pd.read_csv(self.raw_path / 'lms_activities.csv')
            logger.info(f"   ✅ lms_activities.csv: {len(data['lms'])} records")
            
            data['schools'] = pd.read_csv(self.raw_path / 'schools.csv')
            logger.info(f"   ✅ schools.csv: {len(data['schools'])} records")
            
            data['programs'] = pd.read_csv(self.raw_path / 'programs.csv')
            logger.info(f"   ✅ programs.csv: {len(data['programs'])} records")
            
            return data
            
        except FileNotFoundError as e:
            logger.error(f"❌ Missing file: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            raise
    
    def clean_students(self, df):
        """Clean students dataset"""
        logger.info("\n🧹 Cleaning students data...")
        
        df_clean = df.copy()
        
        # Remove duplicates on student_id
        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['student_id'], keep='first')
        removed = initial_count - len(df_clean)
        
        if removed > 0:
            logger.info(f"   ⚠️  Removed {removed} duplicate students")
        
        # Convert student_id to string
        df_clean['student_id'] = df_clean['student_id'].astype(str)
        
        # Handle missing emails (create placeholder)
        if df_clean['email'].isnull().sum() > 0:
            df_clean.loc[df_clean['email'].isnull(), 'email'] = \
                df_clean.loc[df_clean['email'].isnull(), 'student_id'] + '@student.strathmore.edu'
            logger.info(f"   ⚠️  Fixed {df_clean['email'].isnull().sum()} missing emails")
        
        logger.info(f"   ✅ Clean students: {len(df_clean)} records")
        return df_clean
    
    def clean_enrollments(self, df):
        """Clean enrollment/academic records"""
        logger.info("\n🧹 Cleaning enrollment data...")
        
        df_clean = df.copy()
        
        # Convert IDs to string
        df_clean['student_id'] = df_clean['student_id'].astype(str)
        df_clean['course_id'] = df_clean['course_id'].astype(str)
        
        # Remove duplicates (keep latest enrollment)
        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(
            subset=['student_id', 'course_id'], 
            keep='last'
        )
        removed = initial_count - len(df_clean)
        
        if removed > 0:
            logger.info(f"   ⚠️  Removed {removed} duplicate enrollments")
        
        # Clean grades (ensure numeric)
        if 'grade' in df_clean.columns:
            df_clean['grade'] = pd.to_numeric(df_clean['grade'], errors='coerce')
        
        # Ensure GPA is within valid range
        if 'gpa' in df_clean.columns:
            df_clean['gpa'] = pd.to_numeric(df_clean['gpa'], errors='coerce')
            df_clean['gpa'] = df_clean['gpa'].clip(0, 4.0)
        
        logger.info(f"   ✅ Clean enrollments: {len(df_clean)} records")
        return df_clean
    
    def clean_attendance(self, df):
        """Clean attendance records"""
        logger.info("\n🧹 Cleaning attendance data...")
        
        df_clean = df.copy()
        
        # Convert IDs to string
        df_clean['student_id'] = df_clean['student_id'].astype(str)
        df_clean['course_id'] = df_clean['course_id'].astype(str)
        
        # Convert date column to datetime
        if 'session_date' in df_clean.columns:
            df_clean['session_date'] = pd.to_datetime(df_clean['session_date'], errors='coerce')
        
        # Standardize status column
        if 'status' in df_clean.columns:
            # Map various attendance statuses to boolean
            status_map = {
                'present': True,
                'absent': False,
                'late': True,
                'excused': False,
                'p': True,
                'a': False,
                'l': True
            }
            df_clean['attended'] = df_clean['status'].str.lower().map(status_map)
            df_clean['attended'] = df_clean['attended'].fillna(
                df_clean['status'].map({1: True, 0: False})
            )
        
        logger.info(f"   ✅ Clean attendance: {len(df_clean)} records")
        return df_clean
    
    def clean_lms(self, df):
        """Clean LMS activity data"""
        logger.info("\n🧹 Cleaning LMS data...")
        
        df_clean = df.copy()
        
        # Convert IDs to string
        df_clean['student_id'] = df_clean['student_id'].astype(str)
        
        # Convert date/time columns
        if 'timestamp' in df_clean.columns:
            df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], errors='coerce')
        elif 'activity_date' in df_clean.columns:
            df_clean['timestamp'] = pd.to_datetime(df_clean['activity_date'], errors='coerce')
        
        # Clean duration (ensure numeric, in minutes)
        if 'duration_minutes' in df_clean.columns:
            df_clean['duration_minutes'] = pd.to_numeric(
                df_clean['duration_minutes'], 
                errors='coerce'
            )
            # Cap unrealistic durations
            df_clean['duration_minutes'] = df_clean['duration_minutes'].clip(0, 480)  # Max 8 hours
        
        logger.info(f"   ✅ Clean LMS: {len(df_clean)} records")
        return df_clean
    
    def aggregate_attendance_by_student_course(self, df):
        """
        Aggregate attendance to student-course level
        Calculate attendance rate for each student in each course
        """
        logger.info("\n📊 Aggregating attendance by student and course...")
        
        # Create attended column if using 'status'
        if 'attended' not in df.columns and 'status' in df.columns:
            df['attended'] = df['status'].str.lower().isin(['present', 'p', 'late', 'l'])
        
        # Group by student and course
        agg_attendance = df.groupby(['student_id', 'course_id']).agg({
            'attended': ['sum', 'count'],  # Total attended, total sessions
        }).reset_index()
        
        # Flatten column names
        agg_attendance.columns = ['student_id', 'course_id', 'sessions_attended', 'sessions_total']
        
        # Calculate attendance rate
        agg_attendance['physical_attendance_rate'] = (
            agg_attendance['sessions_attended'] / 
            agg_attendance['sessions_total']
        )
        
        logger.info(f"   ✅ Aggregated to {len(agg_attendance)} student-course combinations")
        
        return agg_attendance
    
    def aggregate_lms_by_student(self, df):
        """
        Aggregate LMS activities to student level
        Calculate engagement metrics
        """
        logger.info("\n📊 Aggregating LMS activities by student...")
        
        # Group by student
        agg_lms = df.groupby('student_id').agg({
            'activity_id': 'count',  # Total activities
            'duration_minutes': ['sum', 'mean']  # Total and average duration
        }).reset_index()
        
        # Flatten column names
        agg_lms.columns = ['student_id', 'lms_activity_count', 'lms_total_minutes', 'lms_avg_session_minutes']
        
        # Calculate monthly login rate (assuming data is for one semester ~4 months)
        agg_lms['lms_logins_monthly'] = agg_lms['lms_activity_count'] / 4
        
        logger.info(f"   ✅ Aggregated to {len(agg_lms)} students")
        
        return agg_lms
    
    def merge_all_data(self, data_dict):
        """
        Merge all datasets into unified student dataset
        """
        logger.info("\n🔗 Merging all datasets...")
        
        # Start with students as base
        merged_df = data_dict.get('students')
        if merged_df is None:
            raise ValueError("Students data is required")
        
        logger.info(f"   Base: students ({len(merged_df)} records)")
        
        # Merge enrollments (academic data)
        if 'enrollments' in data_dict:
            # Aggregate enrollments to student level
            enroll_agg = data_dict['enrollments'].groupby('student_id').agg({
                'grade': 'mean',
                'gpa': 'mean',
                'course_id': 'count'  # Number of courses
            }).reset_index()
            enroll_agg.columns = ['student_id', 'avg_grade', 'cumulative_gpa', 'courses_enrolled']
            
            merged_df = merged_df.merge(enroll_agg, on='student_id', how='left')
            logger.info(f"   + enrollments: {len(merged_df)} records")
        
        # Merge aggregated attendance
        if 'attendance_agg' in data_dict:
            # Average attendance across all courses
            attend_avg = data_dict['attendance_agg'].groupby('student_id').agg({
                'physical_attendance_rate': 'mean',
                'sessions_attended': 'sum',
                'sessions_total': 'sum'
            }).reset_index()
            
            merged_df = merged_df.merge(attend_avg, on='student_id', how='left')
            logger.info(f"   + attendance: {len(merged_df)} records")
        
        # Merge aggregated LMS
        if 'lms_agg' in data_dict:
            merged_df = merged_df.merge(data_dict['lms_agg'], on='student_id', how='left')
            logger.info(f"   + lms: {len(merged_df)} records")
        
        # Merge schools info
        if 'schools' in data_dict and 'school_id' in merged_df.columns:
            schools_df = data_dict['schools'][['school_id', 'name']].rename(
                columns={'name': 'school_name'}
            )
            merged_df = merged_df.merge(schools_df, on='school_id', how='left')
            logger.info(f"   + schools: {len(merged_df)} records")
        
        # Merge programs info
        if 'programs' in data_dict and 'program_id' in merged_df.columns:
            programs_df = data_dict['programs'][['program_id', 'name']].rename(
                columns={'name': 'program_name'}
            )
            merged_df = merged_df.merge(programs_df, on='program_id', how='left')
            logger.info(f"   + programs: {len(merged_df)} records")
        
        logger.info(f"   ✅ Final merged dataset: {merged_df.shape}")
        
        return merged_df
    
    def final_cleaning(self, df):
        """Final cleaning steps"""
        logger.info("\n🎯 Final cleaning...")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['student_id'])
        
        # Handle remaining missing values
        # Numeric columns: fill with 0 or median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                # Fill with 0 for counts, median for rates/scores
                if 'count' in col.lower() or 'total' in col.lower():
                    df[col].fillna(0, inplace=True)
                else:
                    df[col].fillna(df[col].median(), inplace=True)
                
                logger.info(f"   ⚠️  Filled {col}: {df[col].isnull().sum()} missing values")
        
        logger.info(f"   ✅ Final dataset: {df.shape}")
        
        return df
    
    def generate_summary_report(self, df):
        """Generate data summary report"""
        logger.info("\n" + "=" * 70)
        logger.info("📊 DATA SUMMARY REPORT")
        logger.info("=" * 70)
        
        logger.info(f"\n📈 Dataset Overview:")
        logger.info(f"   Total Students: {len(df):,}")
        logger.info(f"   Total Features: {len(df.columns)}")
        logger.info(f"   Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        if 'status' in df.columns:
            logger.info(f"\n👥 Student Status:")
            logger.info(f"   Active: {(df['status'] == 'Active').sum():,}")
            logger.info(f"   On Leave: {(df['status'] == 'On Leave').sum():,}")
        
        if 'cumulative_gpa' in df.columns:
            logger.info(f"\n🎓 Academic Performance:")
            logger.info(f"   Average GPA: {df['cumulative_gpa'].mean():.2f}")
            logger.info(f"   Below 2.0 GPA: {(df['cumulative_gpa'] < 2.0).sum():,}")
        
        if 'avg_grade' in df.columns:
            logger.info(f"   Average Grade: {df['avg_grade'].mean():.1f}%")
            logger.info(f"   Below 40%: {(df['avg_grade'] < 40).sum():,}")
        
        if 'physical_attendance_rate' in df.columns:
            logger.info(f"\n✋ Attendance:")
            logger.info(f"   Average Attendance: {df['physical_attendance_rate'].mean():.1%}")
            logger.info(f"   Below 67%: {(df['physical_attendance_rate'] < 0.67).sum():,}")
        
        if 'lms_activity_count' in df.columns:
            logger.info(f"\n💻 LMS Engagement:")
            logger.info(f"   Average Activities: {df['lms_activity_count'].mean():.0f}")
            logger.info(f"   Average Duration: {df['lms_total_minutes'].mean():.0f} minutes")
        
        logger.info(f"\n📋 Missing Data:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            for col in missing[missing > 0].index:
                pct = (missing[col] / len(df)) * 100
                logger.info(f"   {col}: {missing[col]} ({pct:.1f}%)")
        else:
            logger.info(f"   ✅ No missing values!")
        
        logger.info("\n" + "=" * 70)
    
    def clean_and_merge_all(self):
        """
        MAIN FUNCTION: Complete cleaning and merging pipeline
        """
        try:
            # Load raw data
            data = self.load_raw_data()
            
            # Clean each dataset
            logger.info("\n" + "=" * 70)
            logger.info("🧹 CLEANING DATASETS")
            logger.info("=" * 70)
            
            data['students'] = self.clean_students(data['students'])
            data['enrollments'] = self.clean_enrollments(data['enrollments'])
            data['attendance'] = self.clean_attendance(data['attendance'])
            data['lms'] = self.clean_lms(data['lms'])
            
            # Aggregate attendance and LMS
            data['attendance_agg'] = self.aggregate_attendance_by_student_course(data['attendance'])
            data['lms_agg'] = self.aggregate_lms_by_student(data['lms'])
            
            # Merge all datasets
            merged_df = self.merge_all_data(data)
            
            # Final cleaning
            merged_df = self.final_cleaning(merged_df)
            
            # Generate summary
            self.generate_summary_report(merged_df)
            
            # Save cleaned data
            output_path = self.processed_path / 'strathmore_clean_data.csv'
            merged_df.to_csv(output_path, index=False)
            
            logger.info("\n" + "=" * 70)
            logger.info("✅ CLEANING & MERGING COMPLETE")
            logger.info("=" * 70)
            logger.info(f"\n💾 Saved to: {output_path}")
            logger.info(f"   Records: {len(merged_df):,}")
            logger.info(f"   Features: {len(merged_df.columns)}")
            logger.info(f"   Size: {output_path.stat().st_size / 1024**2:.2f} MB")
            
            return merged_df
            
        except Exception as e:
            logger.error(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    """Run data cleaning and merging"""
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    cleaner = StrathmoreDataCleaner()
    
    try:
        # Run cleaning and merging
        merged_df = cleaner.clean_and_merge_all()
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Clean dataset ready for ML")
        print("=" * 70)
        print("\n📊 Quick Preview:")
        print(merged_df.head(10).to_string())
        
        print("\n👉 Next Steps:")
        print("   1. Review: data/processed/strathmore_clean_data.csv")
        print("   2. Check: logs/data_cleaning.log for details")
        print("   3. Move to: Week 2 - Feature Engineering")
        print("\n")
        
        return merged_df
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n📝 Check logs/data_cleaning.log for details")
        return None


if __name__ == "__main__":
    merged_df = main()