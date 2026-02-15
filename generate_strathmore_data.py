"""
Strathmore Data Generator - SIMPLIFIED VERSION
===============================================
Core Data Only:
- Class levels: BBIT1.1, BCOM2.2
- Unit codes: BIT101, ACC201
- Realistic course loads: Y1=6-7, Y2=6-7, Y3=5-6, Y4=4-5
- Physical attendance tracking
- LMS activities (assignments, quizzes)

NO Zoom/Google Meet tracking

Usage: python generate_strathmore_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

np.random.seed(42)
random.seed(42)


class StrathmoreDataGenerator:
    """Generates simplified Strathmore data - core features only"""
    
    def __init__(self, num_students=5000, output_path='data/raw'):
        self.num_students = num_students
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        self.semester_start = datetime(2026, 1, 7)
        self.semester_end = datetime(2026, 4, 11)
        
        print(f"🏭 Strathmore Data Generator")
        print(f"   Students: {num_students}")
        print(f"   Output: {output_path}\n")
    
    def generate_schools(self):
        """Generate 5 Strathmore schools"""
        return pd.DataFrame({
            'school_id': ['SBS', 'SCES', 'SIMS', 'SHSS', 'SLS'],
            'name': [
                'Strathmore University Business School',
                'School of Computing and Engineering Sciences',
                'Strathmore Institute of Mathematical Sciences',
                'School of Humanities and Social Sciences',
                'Strathmore Law School'
            ],
            'dean': [
                'Prof. Mary Wanjiru',
                'Dr. John Kamau',
                'Prof. David Muthoni',
                'Dr. James Kibet',
                'Prof. Sarah Ochieng'
            ],
            'building': [
                'Business School',
                'ICT Building',
                'Block of Management',
                'Oval Building',
                'Sir Thomas More'
            ]
        })
    
    def generate_programs(self, schools_df):
        """Generate programs with program codes"""
        programs = []
        
        # SBS Programs
        for code, name in [('BCOM', 'Bachelor of Commerce'),
                          ('BSCM', 'Bachelor of Science in Supply Chain and Operations Management'),
                          ('BFS', 'Bachelor of Financial Services')]:
            programs.append({
                'program_id': f"SBS_{code}", 'program_code': code, 'name': name,
                'school_id': 'SBS', 'degree_type': 'Undergraduate',
                'duration_years': 4, 'credits_required': 120
            })
        
        # SCES Programs
        for code, name in [('BBIT', 'Bachelor of Business Information Technology'),
                          ('BICS', 'Bachelor of Science in Informatics and Computer Science'),
                          ('BCNC', 'Bachelor of Science in Computer Networks and Cyber Security'),
                          ('BEEE', 'Bachelor of Science in Electrical and Electronics Engineering')]:
            programs.append({
                'program_id': f"SCES_{code}", 'program_code': code, 'name': name,
                'school_id': 'SCES', 'degree_type': 'Undergraduate',
                'duration_years': 4, 'credits_required': 120
            })
        
        # SIMS, SHSS, SLS Programs
        for code, name, school in [
            ('BBSA', 'Bachelor of Business Science in Actuarial Science', 'SIMS'),
            ('BBSE', 'Bachelor of Business Science in Financial Economics', 'SIMS'),
            ('BBSF', 'Bachelor of Business Science in Financial Engineering', 'SIMS'),
            ('BSSD', 'Bachelor of Science in Statistics and Data Science', 'SIMS'),
            ('BACO', 'Bachelor of Arts in Communication', 'SHSS'),
            ('BAIS', 'Bachelor of Arts in International Studies', 'SHSS'),
            ('BADS', 'Bachelor of Arts in Development Studies and Philosophy', 'SHSS'),
            ('BSCP', 'Bachelor of Science in Psychology', 'SHSS'),
            ('LLB', 'Bachelor of Laws', 'SLS')
        ]:
            programs.append({
                'program_id': f"{school}_{code}", 'program_code': code, 'name': name,
                'school_id': school, 'degree_type': 'Undergraduate',
                'duration_years': 4, 'credits_required': 120
            })
        
        return pd.DataFrame(programs)
    
    def generate_courses(self):
        """Generate courses across all schools and years"""
        courses = []
        
        course_templates = [
            # SCES courses
            ('BIT101', 'Introduction to Programming', 1, 1, 4, 2, 2, 'SCES'),
            ('BIT102', 'Computer Systems Architecture', 1, 1, 3, 2, 1, 'SCES'),
            ('BIT103', 'Mathematics for IT I', 1, 1, 3, 2, 1, 'SCES'),
            ('BIT104', 'Digital Logic Design', 1, 1, 3, 2, 1, 'SCES'),
            ('BIT105', 'Communication Skills I', 1, 1, 3, 2, 1, 'SCES'),
            ('BIT106', 'Introduction to IT', 1, 1, 3, 2, 1, 'SCES'),
            ('BIT111', 'Programming II', 1, 2, 4, 2, 2, 'SCES'),
            ('BIT112', 'Database Fundamentals', 1, 2, 4, 2, 2, 'SCES'),
            ('BIT113', 'Mathematics for IT II', 1, 2, 3, 2, 1, 'SCES'),
            ('BIT114', 'Web Development I', 1, 2, 3, 2, 1, 'SCES'),
            ('BIT115', 'Communication Skills II', 1, 2, 3, 2, 1, 'SCES'),
            ('BIT116', 'Computer Ethics', 1, 2, 3, 2, 1, 'SCES'),
            ('BIT201', 'Data Structures and Algorithms', 2, 1, 4, 2, 2, 'SCES'),
            ('BIT202', 'Object-Oriented Programming', 2, 1, 4, 2, 2, 'SCES'),
            ('BIT203', 'Operating Systems', 2, 1, 3, 2, 1, 'SCES'),
            ('BIT204', 'Discrete Mathematics', 2, 1, 3, 2, 1, 'SCES'),
            ('BIT205', 'Systems Analysis & Design', 2, 1, 3, 2, 1, 'SCES'),
            ('BIT206', 'Human Computer Interaction', 2, 1, 3, 2, 1, 'SCES'),
            ('BIT211', 'Computer Networks', 2, 2, 4, 3, 1, 'SCES'),
            ('BIT212', 'Database Management Systems', 2, 2, 4, 2, 2, 'SCES'),
            ('BIT213', 'Software Engineering I', 2, 2, 3, 2, 1, 'SCES'),
            ('BIT214', 'Internet & Web Technology', 2, 2, 3, 2, 1, 'SCES'),
            ('BIT215', 'Business Information Systems', 2, 2, 3, 2, 1, 'SCES'),
            ('BIT301', 'Software Engineering II', 3, 1, 3, 2, 1, 'SCES'),
            ('BIT302', 'Cybersecurity Fundamentals', 3, 1, 3, 2, 1, 'SCES'),
            ('BIT303', 'Mobile Application Development', 3, 1, 4, 2, 2, 'SCES'),
            ('BIT304', 'Data Mining & Analytics', 3, 1, 3, 2, 1, 'SCES'),
            ('BIT305', 'IT Project Management', 3, 1, 3, 2, 1, 'SCES'),
            ('BIT311', 'Cloud Computing', 3, 2, 3, 2, 1, 'SCES'),
            ('BIT312', 'Artificial Intelligence', 3, 2, 4, 2, 2, 'SCES'),
            ('BIT313', 'Network Security', 3, 2, 3, 2, 1, 'SCES'),
            ('BIT314', 'Enterprise Systems', 3, 2, 3, 2, 1, 'SCES'),
            ('BIT401', 'Machine Learning', 4, 1, 4, 2, 2, 'SCES'),
            ('BIT402', 'Research Methods', 4, 1, 3, 2, 1, 'SCES'),
            ('BIT403', 'Final Year Project I', 4, 1, 4, 1, 3, 'SCES'),
            ('BIT404', 'IT Strategy & Governance', 4, 1, 3, 2, 1, 'SCES'),
            ('BIT411', 'Final Year Project II', 4, 2, 4, 1, 3, 'SCES'),
            ('BIT412', 'Emerging Technologies', 4, 2, 3, 2, 1, 'SCES'),
            
            # SBS courses
            ('ACC101', 'Financial Accounting I', 1, 1, 4, 2, 2, 'SBS'),
            ('BUS101', 'Introduction to Business', 1, 1, 3, 2, 1, 'SBS'),
            ('ECO101', 'Microeconomics', 1, 1, 3, 2, 1, 'SBS'),
            ('MAT111', 'Business Mathematics I', 1, 1, 3, 2, 1, 'SBS'),
            ('COM111', 'Business Communication I', 1, 1, 3, 2, 1, 'SBS'),
            ('MGT101', 'Introduction to Management', 1, 1, 3, 2, 1, 'SBS'),
            ('ACC102', 'Financial Accounting II', 1, 2, 4, 2, 2, 'SBS'),
            ('ECO102', 'Macroeconomics', 1, 2, 3, 2, 1, 'SBS'),
            ('MAT112', 'Business Mathematics II', 1, 2, 3, 2, 1, 'SBS'),
            ('LAW111', 'Business Law', 1, 2, 3, 2, 1, 'SBS'),
            ('COM112', 'Business Communication II', 1, 2, 3, 2, 1, 'SBS'),
            ('BUS102', 'Business Environment', 1, 2, 3, 2, 1, 'SBS'),
            ('ACC201', 'Management Accounting', 2, 1, 4, 2, 2, 'SBS'),
            ('MKT201', 'Marketing Principles', 2, 1, 3, 2, 1, 'SBS'),
            ('FIN201', 'Corporate Finance I', 2, 1, 4, 2, 2, 'SBS'),
            ('HRM201', 'Human Resource Management', 2, 1, 3, 2, 1, 'SBS'),
            ('BUS201', 'Business Analytics', 2, 1, 3, 2, 1, 'SBS'),
            ('OMG201', 'Operations Management', 2, 1, 3, 2, 1, 'SBS'),
            ('ACC202', 'Cost Accounting', 2, 2, 4, 2, 2, 'SBS'),
            ('FIN202', 'Corporate Finance II', 2, 2, 4, 2, 2, 'SBS'),
            ('MKT202', 'Consumer Behavior', 2, 2, 3, 2, 1, 'SBS'),
            ('BUS202', 'Business Statistics', 2, 2, 3, 2, 1, 'SBS'),
            ('ENT201', 'Entrepreneurship', 2, 2, 3, 2, 1, 'SBS'),
            ('ACC301', 'Advanced Accounting', 3, 1, 4, 2, 2, 'SBS'),
            ('SCM301', 'Supply Chain Management', 3, 1, 3, 2, 1, 'SBS'),
            ('MKT301', 'Digital Marketing', 3, 1, 3, 2, 1, 'SBS'),
            ('FIN301', 'Investment Analysis', 3, 1, 3, 2, 1, 'SBS'),
            ('MGT301', 'Organizational Behavior', 3, 1, 3, 2, 1, 'SBS'),
            ('ACC302', 'Auditing', 3, 2, 4, 2, 2, 'SBS'),
            ('MKT302', 'Brand Management', 3, 2, 3, 2, 1, 'SBS'),
            ('FIN302', 'Financial Markets', 3, 2, 3, 2, 1, 'SBS'),
            ('BUS301', 'Business Research Methods', 3, 2, 3, 2, 1, 'SBS'),
            ('STR401', 'Strategic Management', 4, 1, 3, 2, 1, 'SBS'),
            ('BUS401', 'Business Ethics', 4, 1, 3, 2, 1, 'SBS'),
            ('MGT401', 'Change Management', 4, 1, 3, 2, 1, 'SBS'),
            ('BUS411', 'Business Project I', 4, 1, 4, 1, 3, 'SBS'),
            ('BUS412', 'Business Project II', 4, 2, 4, 1, 3, 'SBS'),
            ('MKT401', 'Strategic Marketing', 4, 2, 3, 2, 1, 'SBS'),
            
            # SIMS, SHSS, SLS courses
            ('MAT101', 'Calculus I', 1, 1, 4, 2, 2, 'SIMS'),
            ('STA101', 'Probability Theory', 1, 1, 4, 2, 2, 'SIMS'),
            ('MAT102', 'Calculus II', 1, 2, 4, 2, 2, 'SIMS'),
            ('STA102', 'Statistics I', 1, 2, 4, 2, 2, 'SIMS'),
            ('COM101', 'Introduction to Communication', 1, 1, 3, 2, 1, 'SHSS'),
            ('PSY101', 'Introduction to Psychology', 1, 1, 3, 2, 1, 'SHSS'),
            ('LAW101', 'Legal Methods', 1, 1, 3, 2, 1, 'SLS'),
            ('LAW102', 'Constitutional Law I', 1, 1, 3, 2, 1, 'SLS'),
        ]
        
        for unit_code, name, year, sem, credits, phys, online, school in course_templates:
            total = phys + online
            courses.append({
                'course_id': unit_code,
                'unit_code': unit_code,
                'course_name': name,
                'year_level': year,
                'semester': sem,
                'school_id': school,
                'credit_hours': credits,
                'physical_hours_per_week': phys,
                'online_hours_per_week': online,
                'total_weeks': 14,
                'physical_sessions_total': phys * 14,
                'online_sessions_total': online * 14,
                'physical_percentage': round(phys/total, 2),
                'online_percentage': round(online/total, 2)
            })
        
        return pd.DataFrame(courses)
    
    def generate_students(self, programs_df):
        """Generate students with class levels"""
        first_names = ['John', 'Mary', 'Peter', 'Sarah', 'James', 'Grace', 
                      'David', 'Faith', 'Michael', 'Jane', 'Daniel', 'Ruth',
                      'Joseph', 'Ann', 'Kevin', 'Lucy', 'Brian', 'Nancy',
                      'Samuel', 'Caroline', 'Emmanuel', 'Joyce', 'Vincent', 'Rose']
        
        last_names = ['Kamau', 'Wanjiru', 'Ochieng', 'Muthoni', 'Kibet', 'Achieng',
                     'Njoroge', 'Wambui', 'Otieno', 'Nyambura', 'Mutua', 'Chebet',
                     'Mwangi', 'Njeri', 'Kariuki', 'Wangui', 'Kipchoge', 'Jepkorir']
        
        students = []
        students_per_school = {'SBS': 1200, 'SCES': 1300, 'SIMS': 800, 'SHSS': 1000, 'SLS': 700}
        student_counter = 1
        
        for school_id, num_students in students_per_school.items():
            school_programs = programs_df[programs_df['school_id'] == school_id]
            
            for i in range(num_students):
                first = random.choice(first_names)
                last = random.choice(last_names)
                program = school_programs.sample(1).iloc[0]
                year = random.randint(1, 4)
                semester = random.randint(1, 2)
                class_level = f"{program['program_code']}{year}.{semester}"
                
                students.append({
                    'student_id': f'{100000 + student_counter}',
                    'name': f'{first} {last}',
                    'email': f'{first.lower()}.{last.lower()}{student_counter}@strathmore.edu',
                    'gender': random.choice(['Male', 'Female']),
                    'age': 17 + year + random.randint(0, 3),
                    'program_id': program['program_id'],
                    'program_code': program['program_code'],
                    'school_id': program['school_id'],
                    'year_of_study': year,
                    'semester': semester,
                    'class_level': class_level,
                    'enrollment_date': (self.semester_start - timedelta(days=365*year + random.randint(0, 180))).strftime('%Y-%m-%d'),
                    'status': random.choices(['Active', 'On Leave'], weights=[92, 8])[0]
                })
                
                student_counter += 1
        
        return pd.DataFrame(students)
    
    def generate_users(self, students_df):
        return pd.DataFrame([{
            'user_id': f"U_{s['student_id']}",
            'username': s['email'].split('@')[0],
            'email': s['email'],
            'role': 'student',
            'full_name': s['name'],
            'is_active': s['status'] == 'Active'
        } for _, s in students_df.iterrows()])
    
    def generate_admins(self, schools_df):
        return pd.DataFrame([{
            'admin_id': f"ADMIN_{s['school_id']}",
            'name': s['dean'],
            'school_id': s['school_id'],
            'email': f"dean.{s['school_id'].lower()}@strathmore.edu"
        } for _, s in schools_df.iterrows()])
    
    def generate_enrollments(self, students_df, courses_df):
        """Generate enrollments with realistic workloads"""
        enrollments = []
        active = students_df[students_df['status'] == 'Active']
        
        course_load_distribution = {
            1: [6, 6, 6, 7, 7, 7],
            2: [6, 6, 6, 7, 7],
            3: [5, 5, 5, 6, 6],
            4: [4, 4, 4, 5, 5]
        }
        
        print(f"\n   Generating enrollments...")
        print(f"   Course load: Y1=6-7, Y2=6-7, Y3=5-6, Y4=4-5 units")
        
        for idx, (_, student) in enumerate(active.iterrows(), 1):
            student_year = student['year_of_study']
            student_school = student['school_id']
            student_semester = student['semester']
            
            num_courses = random.choice(course_load_distribution[student_year])
            
            school_courses = courses_df[
                (courses_df['year_level'] == student_year) &
                (courses_df['school_id'] == student_school) &
                (courses_df['semester'] == student_semester)
            ]
            
            if len(school_courses) < num_courses:
                electives = courses_df[
                    (courses_df['year_level'] == student_year) &
                    (courses_df['semester'] == student_semester) &
                    (courses_df['school_id'] != student_school)
                ]
                available_courses = pd.concat([school_courses, electives])
            else:
                available_courses = school_courses
            
            if len(available_courses) == 0:
                continue
            
            num_to_take = min(num_courses, len(available_courses))
            student_courses = available_courses.sample(num_to_take)
            
            for _, course in student_courses.iterrows():
                struggle = random.random()
                
                if struggle > 0.85:
                    grade = random.uniform(30, 55)
                elif struggle > 0.70:
                    grade = random.uniform(55, 70)
                else:
                    grade = random.uniform(70, 95)
                
                gpa = min(4.0, max(0.0, grade / 25))
                
                enrollments.append({
                    'enrollment_id': f"ENR_{len(enrollments)+1:06d}",
                    'student_id': student['student_id'],
                    'course_id': course['course_id'],
                    'unit_code': course['unit_code'],
                    'semester': 'Spring 2026',
                    'year_level': student_year,
                    'class_level': student['class_level'],
                    'grade': round(grade, 1),
                    'gpa': round(gpa, 2),
                    'credits': course['credit_hours'],
                    'status': 'Enrolled'
                })
            
            if idx % 500 == 0:
                print(f"      {idx}/{len(active)} students...")
        
        return pd.DataFrame(enrollments)
    
    def generate_attendance(self, students_df, courses_df, enrollments_df):
        """Generate physical attendance"""
        attendance = []
        
        print(f"\n   Generating physical attendance...")
        
        for idx, (_, enr) in enumerate(enrollments_df.iterrows(), 1):
            course = courses_df[courses_df['course_id'] == enr['course_id']].iloc[0]
            total_sessions = course['physical_sessions_total']
            
            if enr['grade'] >= 80:
                rate = random.uniform(0.85, 1.0)
            elif enr['grade'] >= 70:
                rate = random.uniform(0.75, 0.90)
            elif enr['grade'] >= 60:
                rate = random.uniform(0.65, 0.80)
            else:
                rate = random.uniform(0.30, 0.60)
            
            for session in range(int(total_sessions)):
                date = self.semester_start + timedelta(weeks=session//2, days=(session%2)*2)
                attended = random.random() < rate
                
                attendance.append({
                    'attendance_id': f"ATT_{len(attendance)+1:08d}",
                    'student_id': enr['student_id'],
                    'course_id': enr['course_id'],
                    'unit_code': enr['unit_code'],
                    'session_date': date.strftime('%Y-%m-%d'),
                    'session_type': 'Lecture',
                    'status': 'Present' if attended else 'Absent',
                    'late': random.random() < 0.15 if attended else False
                })
            
            if idx % 2000 == 0:
                print(f"      {idx}/{len(enrollments_df)} enrollments...")
        
        return pd.DataFrame(attendance)
    
    def generate_lms(self, students_df, courses_df, enrollments_df):
        """Generate LMS activities (assignments, quizzes, etc.)"""
        activities = []
        types = ['quiz_attempt', 'assignment_submit', 'resource_download']
        
        print(f"\n   Generating LMS activities...")
        
        for idx, (_, enr) in enumerate(enrollments_df.iterrows(), 1):
            grade = enr['grade']
            
            if grade >= 80:
                count = random.randint(80, 150)
                duration = random.uniform(25, 45)
            elif grade >= 70:
                count = random.randint(50, 90)
                duration = random.uniform(20, 35)
            elif grade >= 60:
                count = random.randint(30, 60)
                duration = random.uniform(15, 30)
            else:
                count = random.randint(10, 40)
                duration = random.uniform(5, 20)
            
            for _ in range(count):
                date = self.semester_start + timedelta(days=random.randint(0, 95))
                activities.append({
                    'activity_id': f"LMS_{len(activities)+1:08d}",
                    'student_id': enr['student_id'],
                    'course_id': enr['course_id'],
                    'unit_code': enr['unit_code'],
                    'activity_type': random.choice(types),
                    'activity_date': date.strftime('%Y-%m-%d'),
                    'timestamp': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration_minutes': max(1, int(np.random.normal(duration, 10))),
                    'completed': random.random() < 0.85
                })
            
            if idx % 2000 == 0:
                print(f"      {idx}/{len(enrollments_df)} enrollments...")
        
        return pd.DataFrame(activities)
    
    def generate_all(self):
        """Generate all datasets"""
        print("Generating datasets...\n")
        
        schools = self.generate_schools()
        print(f"✅ Schools: {len(schools)}")
        
        programs = self.generate_programs(schools)
        print(f"✅ Programs: {len(programs)}")
        
        courses = self.generate_courses()
        print(f"✅ Courses: {len(courses)}")
        
        students = self.generate_students(programs)
        print(f"✅ Students: {len(students)} ({(students['status']=='Active').sum()} active)")
        
        users = self.generate_users(students)
        print(f"✅ Users: {len(users)}")
        
        admins = self.generate_admins(schools)
        print(f"✅ Admins: {len(admins)}")
        
        enrollments = self.generate_enrollments(students, courses)
        print(f"✅ Enrollments: {len(enrollments)}")
        
        attendance = self.generate_attendance(students, courses, enrollments)
        print(f"✅ Physical Attendance: {len(attendance)}")
        
        lms = self.generate_lms(students, courses, enrollments)
        print(f"✅ LMS Activities: {len(lms)}")
        
        data = {
            'schools': schools,
            'programs': programs,
            'courses': courses,
            'students': students,
            'users': users,
            'school_admins': admins,
            'sis_enrollments': enrollments,
            'attendance_records': attendance,
            'lms_activities': lms
        }
        
        print(f"\nSaving to {self.output_path}...")
        for name, df in data.items():
            path = self.output_path / f"{name}.csv"
            df.to_csv(path, index=False)
            size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
            print(f"  💾 {name}.csv ({len(df):,} records, {size_mb:.1f} MB)")
        
        print(f"\n✅ All data generated successfully!")
        print(f"\n📊 Statistics:")
        print(f"   Average GPA: {enrollments['gpa'].mean():.2f}")
        print(f"   Students below 40%: {(enrollments['grade'] < 40).sum():,}")
        print(f"   Attendance rate: {(attendance['status']=='Present').sum()/len(attendance):.1%}")
        
        return data


if __name__ == "__main__":
    print("\n" + "🏭"*35)
    print("STRATHMORE DATA GENERATOR")
    print("Core Data Only - Simplified")
    print("🏭"*35 + "\n")
    
    generator = StrathmoreDataGenerator(num_students=5000)
    data = generator.generate_all()
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Your Strathmore dataset is ready!")
    print("="*70)
    print("\n👉 Next: Run Week 1 extraction and cleaning scripts!\n")