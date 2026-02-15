
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

print("\n📊 CREATING PREDICTION VISUALIZATIONS\n")

# Create output directory
Path('visualizations').mkdir(exist_ok=True)

# Load predictions
print("📂 Loading predictions...")
df = pd.read_csv('predictions_output.csv')
print(f"   ✅ Loaded {len(df):,} students\n")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# ============================================================================
# 1. RISK LEVEL DISTRIBUTION (Pie + Bar)
# ============================================================================
print("📊 Creating Risk Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Count students by risk level
risk_counts = df['dropout_risk_level'].value_counts()
colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']

# Pie chart
ax1.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%',
        colors=colors[:len(risk_counts)], startangle=90)
ax1.set_title('Student Risk Distribution', fontsize=16, fontweight='bold')

# Bar chart
risk_counts.plot(kind='bar', ax=ax2, color=colors[:len(risk_counts)])
ax2.set_title('Risk Level Counts', fontsize=16, fontweight='bold')
ax2.set_xlabel('Risk Level', fontsize=12)
ax2.set_ylabel('Number of Students', fontsize=12)
ax2.tick_params(axis='x', rotation=0)
for i, v in enumerate(risk_counts.values):
    ax2.text(i, v + 10, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/1_risk_distribution.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: visualizations/1_risk_distribution.png")
plt.close()

# ============================================================================
# 2. DROPOUT PROBABILITY HISTOGRAM
# ============================================================================
print("📊 Creating Probability Histogram...")

plt.figure(figsize=(12, 6))
plt.hist(df['dropout_probability'], bins=50, color='steelblue', 
         edgecolor='black', alpha=0.7)
plt.axvline(x=0.5, color='orange', linestyle='--', linewidth=2, 
            label='High Risk (50%)')
plt.axvline(x=0.7, color='red', linestyle='--', linewidth=2, 
            label='Critical Risk (70%)')
plt.xlabel('Dropout Probability', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.title('Distribution of Dropout Probabilities', fontsize=16, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/2_probability_histogram.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: visualizations/2_probability_histogram.png")
plt.close()

# ============================================================================
# 3. RISK BY SCHOOL
# ============================================================================
print("📊 Creating Risk by School...")

school_risk = df.groupby('school_id').agg({
    'dropout_probability': 'mean',
    'student_id': 'count'
}).reset_index()
school_risk.columns = ['School', 'Avg_Risk', 'Students']
school_risk = school_risk.sort_values('Avg_Risk', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(school_risk['School'], school_risk['Avg_Risk'], 
               color='coral', edgecolor='black')
ax.set_xlabel('Average Dropout Probability', fontsize=12)
ax.set_title('Average Dropout Risk by School', fontsize=16, fontweight='bold')

for i, (risk, count) in enumerate(zip(school_risk['Avg_Risk'], school_risk['Students'])):
    ax.text(risk + 0.005, i, f'{risk:.1%} ({count:,} students)', 
            va='center', fontsize=10)

plt.tight_layout()
plt.savefig('visualizations/3_risk_by_school.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: visualizations/3_risk_by_school.png")
plt.close()

# ============================================================================
# 4. ATTENDANCE VS GPA SCATTER (Color by Risk)
# ============================================================================
print("📊 Creating Attendance vs GPA Scatter...")

plt.figure(figsize=(12, 8))
scatter = plt.scatter(
    df['physical_attendance_rate'], 
    df['cumulative_gpa'],
    c=df['dropout_probability'],
    cmap='RdYlGn_r',
    s=50,
    alpha=0.6,
    edgecolors='black',
    linewidth=0.5
)
cbar = plt.colorbar(scatter, label='Dropout Probability')
plt.axhline(y=2.0, color='red', linestyle='--', alpha=0.5, label='GPA 2.0')
plt.axvline(x=0.67, color='blue', linestyle='--', alpha=0.5, label='67% Attendance')
plt.xlabel('Attendance Rate', fontsize=12)
plt.ylabel('Cumulative GPA', fontsize=12)
plt.title('Student Risk: Attendance vs GPA', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/4_attendance_vs_gpa.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: visualizations/4_attendance_vs_gpa.png")
plt.close()

# ============================================================================
# 5. TOP 20 HIGHEST RISK STUDENTS
# ============================================================================
print("📊 Creating Top 20 High Risk Chart...")

