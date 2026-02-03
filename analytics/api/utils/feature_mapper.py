"""
Feature Mapper - Converts database columns to V2 model features
"""

import pandas as pd
import numpy as np

def map_db_to_model_features(df):
    """
    Map database columns to V2 model features
    
    Database columns -> Model features
    """
    
    # Create a copy
    features = df.copy()
    
    # Rename columns to match model expectations
    column_mapping = {
        'avg_engagement_score': 'engagement_score',
        'avg_time_spent': 'time_spent_minutes',
        'max_consecutive_absences': 'consecutive_absences',
        'avg_consecutive_absences': 'consecutive_absences',  # Use avg if max not available
    }
    
    # Apply renaming
    for old_col, new_col in column_mapping.items():
        if old_col in features.columns and new_col not in features.columns:
            features[new_col] = features[old_col]
    
    # Calculate missing features with reasonable defaults
    if 'forum_posts' not in features.columns:
        # Estimate forum posts from engagement
        if 'engagement_score' in features.columns:
            features['forum_posts'] = (features['engagement_score'] / 10).fillna(0).astype(int)
        else:
            features['forum_posts'] = 0
    
    if 'late_submissions' not in features.columns:
        # Estimate late submissions from completion rate
        if 'assignment_completion_rate' in features.columns:
            # Lower completion = more late submissions
            features['late_submissions'] = ((1 - features['assignment_completion_rate']) * 10).fillna(0).astype(int)
        else:
            features['late_submissions'] = 0
    
    if 'help_requests' not in features.columns:
        # Estimate help requests from grade points
        if 'avg_grade_points' in features.columns:
            # Lower grades = more help requests
            features['help_requests'] = ((4 - features['avg_grade_points']) * 3).fillna(0).astype(int)
        else:
            features['help_requests'] = 0
    
    # Ensure all required V2 model features exist
    required_features = [
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
    
    # Fill missing with 0
    for feature in required_features:
        if feature not in features.columns:
            features[feature] = 0
    
    # Handle percentage values (convert to 0-100 if in 0-1 range)
    if 'attendance_rate' in features.columns:
        if features['attendance_rate'].max() <= 1:
            features['attendance_rate'] = features['attendance_rate'] * 100
    
    if 'assignment_completion_rate' in features.columns:
        if features['assignment_completion_rate'].max() <= 1:
            features['assignment_completion_rate'] = features['assignment_completion_rate'] * 100
    
    # Clean up
    features = features.fillna(0)
    features = features.replace([np.inf, -np.inf], 0)
    
    return features

def get_model_features(df):
    """
    Extract only the features needed by the V2 models
    """
    required_features = [
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
    
    # Map features first
    mapped_df = map_db_to_model_features(df)
    
    # Return only required features
    return mapped_df[required_features]
