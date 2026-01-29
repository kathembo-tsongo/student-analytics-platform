"""
Strathmore University - Student At-Risk Prediction Platform
Fake Data Generator (Strathmore-Specific)

Schools:
- SCES (School of Computing & Engineering Sciences)
- SBS (Strathmore Business School)
- STH (School of Tourism & Hospitality)
- SLS (Strathmore Law School)
- SHSS (School of Humanities & Social Sciences)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

class StrathmoreDataGenerator:
    def __init__(self, students_per_program=40):
        self.students_per_program = students_per_program
        
        # Strathmore University Schools and Programs
        self.schools_programs = {
            'SCES': {
                'name': 'School of Computing & Engineering Sciences',
                'programs': ['BBIT', 'ICS', 'CNS']
            },
            'SBS': {
                'name': 'Strathmore Business School',
                'programs': ['BCOM', 'BFS', 'BSCM']
            },
            'STH': {
                'name': 'School of Tourism & Hospitality',
                'programs': ['BTM', 'BHM']
            },
            'SLS': {
                'name': 'Strathmore Law School',
                'programs': ['LAW']
            },
            'SHSS': {
                'name': 'School of Humanities & Social Sciences',
                'programs': ['BA', 'COMMON UNITS']
            }
        }
        
        # Course mappings per program
        self.program_courses = {
            # SCES Programs
            'BBIT': [
                'Programming I', 'Programming II', 'Data Structures', 'Algorithms',
                'Database Systems', 'Web Development', 'Software Engineering', 'Networks',
                'Operating Systems', 'System Analysis', 'Project Management', 'Business Intelligence'
            ],
            'ICS': [
                'Information Systems', 'Database Management', 'Systems Analysis',
                'E-Commerce', 'IT Strategy', 'Business Process', 'ERP Systems',
                'Data Analytics', 'Cybersecurity', 'Cloud Computing'
            ],
            'CNS': [
                'Network Security', 'Cryptography', 'Ethical Hacking', 'Digital Forensics',
                'Risk Management', 'Security Policies', 'Intrusion Detection', 'Malware Analysis',
                'Secure Programming', 'Penetration Testing'
            ],
            
            # SBS Programs
            'BCOM': [
                'Financial Accounting', 'Management Accounting', 'Corporate Finance',
                'Marketing', 'Human Resources', 'Strategic Management', 'Business Law',
                'Economics', 'Statistics', 'Entrepreneurship'
            ],
            'BFS': [
                'Financial Markets', 'Investment Analysis', 'Portfolio Management',
                'Derivatives', 'Risk Management', 'Financial Modeling', 'Corporate Finance',
                'International Finance', 'Banking', 'Insurance'
            ],
            'BSCM': [
                'Supply Chain Management', 'Operations Management', 'Logistics',
                'Procurement', 'Inventory Management', 'Quality Management',
                'Project Management', 'Business Analytics', 'Transportation'
            ],
            
            # STH Programs
            'BTM': [
                'Tourism Management', 'Destination Management', 'Tour Operations',
                'Tourism Marketing', 'Event Management', 'Ecotourism',
                'Tourism Policy', 'Cultural Tourism', 'Travel Agency Management'
            ],
            'BHM': [
                'Hotel Operations', 'Food & Beverage', 'Front Office Management',
                'Housekeeping', 'Hotel Marketing', 'Revenue Management',
                'Hospitality Law', 'Customer Service', 'Hotel Accounting'
            ],
            
            # SLS Programs
            'LAW': [
                'Constitutional Law', 'Contract Law', 'Criminal Law', 'Tort Law',
                'Property Law', 'Commercial Law', 'Family Law', 'Legal Research',
                'Jurisprudence', 'Civil Procedure', 'Evidence', 'Human Rights Law'
            ],
            
            # SHSS Programs
            'BA': [
                'Development Studies', 'International Relations', 'Public Policy',
                'Political Science', 'Sociology', 'Psychology', 'Philosophy',
                'Research Methods', 'Ethics', 'Communication Studies'
            ],
            'COMMON UNITS': [
                'English Communication', 'Mathematics', 'Statistics', 'ICT Skills',
                'Critical Thinking', 'Philosophy', 'Ethics', 'Entrepreneurship'
            ]
        }
        
    def generate_all(self):
        """Generate complete Strathmore dataset"""
        print("\n" + "=" * 70)
        print("STRATHMORE UNIVERSITY - STUDENT AT-RISK PREDICTION PLATFORM")
        print("Fake Data Generator v2.0 (Strathmore-Specific)")
        print("=" * 70)
        print("\nGenerating realistic data based on Strathmore structure...")
        print("=" * 70)
        
        # 1. Schools
        schools = self.generate_schools()
        print(f"\n✓ Generated {len(schools)} schools (Strathmore faculties)")
        
        # 2. Programs
        programs = self.generate_programs(schools)
        print(f"✓ Generated {len(programs)} programs")
        
        # 3. Users (Admin, School Admins, Mentors)
        users, school_admins, mentor_assignments = self.generate_users(schools, programs)
        print(f"✓ Generated {len(users)} users")
        
        # 4. Students
        students = self.generate_students(programs)
        print(f"✓ Generated {len(students)} students")
        
        # 5. Courses
        courses = self.generate_courses(programs)
        print(f"✓ Generated {len(courses)} courses")
        
        # 6. SIS: Enrollments & Grades
        sis_enrollments = self.generate_sis_enrollments(students, courses)
        print(f"✓ Generated {len(sis_enrollments)} SIS enrollments")
        
        # 7. LMS: Activity & Engagement
        lms_activities = self.generate_lms_activities(students)
        print(f"✓ Generated {len(lms_activities)} LMS activity records")
        
        # 8. Attendance: Daily records
        attendance = self.generate_attendance(students)
        print(f"✓ Generated {len(attendance)} attendance records")
        
        # Save all
        self.save_all({
            'schools': schools,
            'programs': programs,
            'users': users,
            'school_admins': school_admins,
            'students': students,
            'mentor_assignments': mentor_assignments,
            'courses': courses,
            'sis_enrollments': sis_enrollments,
            'lms_activities': lms_activities,
            'attendance_records': attendance
        })
        
    def generate_schools(self):
        """Generate Strathmore schools"""
        schools = []
        school_id = 1
        
        for code, info in self.schools_programs.items():
            schools.append({
                'id': school_id,
                'school_code': code,
                'school_name': info['name'],
                'university': 'Strathmore University',
                'status': 'active'
            })
            school_id += 1
        
        return pd.DataFrame(schools)
    
    def generate_programs(self, schools):
        """Generate programs per school"""
        programs = []
        program_id = 1
        
        for _, school in schools.iterrows():
            school_code = school['school_code']
            for prog_code in self.schools_programs[school_code]['programs']:
                
                # Determine degree type
                if prog_code == 'COMMON UNITS':
                    degree_type = 'Foundation'
                elif prog_code == 'LAW':
                    degree_type = 'LLB'
                elif prog_code in ['BA', 'BTM', 'BHM']:
                    degree_type = 'Bachelor of Arts'
                else:
                    degree_type = 'Bachelor of Science'
                
                programs.append({
                    'id': program_id,
                    'program_code': prog_code,
                    'program_name': self._get_program_full_name(prog_code),
                    'school_id': school['id'],
                    'degree_type': degree_type,
                    'duration_years': 4 if prog_code != 'COMMON UNITS' else 1,
                    'status': 'active'
                })
                program_id += 1
        
        return pd.DataFrame(programs)
    
    def _get_program_full_name(self, code):
        """Get full program name"""
        names = {
            'BBIT': 'Bachelor of Business Information Technology',
            'ICS': 'Information Communication Systems',
            'CNS': 'Computer and Network Security',
            'BCOM': 'Bachelor of Commerce',
            'BFS': 'Bachelor of Financial Services',
            'BSCM': 'Bachelor of Supply Chain Management',
            'BTM': 'Bachelor of Tourism Management',
            'BHM': 'Bachelor of Hotel Management',
            'LAW': 'Bachelor of Laws',
            'BA': 'Bachelor of Arts',
            'COMMON UNITS': 'Common Units (Foundation)'
        }
        return names.get(code, code)
    
    def generate_users(self, schools, programs):
        """Generate users: admin, school admins, mentors"""
        users = []
        school_admins = []
        mentor_assignments = []
        user_id = 1
        
        # 1 System Admin
        users.append({
            'id': user_id,
            'email': 'admin@strathmore.edu',
            'role': 'admin',
            'name': 'System Administrator',
            'password': 'password123',
            'status': 'active'
        })
        user_id += 1
        
        # School Deans (1 per school)
        for _, school in schools.iterrows():
            users.append({
                'id': user_id,
                'email': f'dean.{school["school_code"].lower()}@strathmore.edu',
                'role': 'school_admin',
                'name': f'Dean of {school["school_code"]}',
                'password': 'password123',
                'status': 'active'
            })
            
            school_admins.append({
                'id': len(school_admins) + 1,
                'user_id': user_id,
                'school_id': school['id'],
                'assigned_date': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            })
            
            user_id += 1
        
        # Mentors (Lecturers) - 1 per program
        assignment_id = 1
        for _, program in programs.iterrows():
            prog_code = program['program_code']
            
            # Create mentor
            users.append({
                'id': user_id,
                'email': f'mentor.{prog_code.lower()}@strathmore.edu',
                'role': 'mentor',
                'name': f'{prog_code} Program Mentor',
                'password': 'password123',
                'status': 'active'
            })
            
            mentor_id = user_id
            user_id += 1
            
            # Will assign students later, store mentor info for now
            # (mentor_assignments will be populated after students are created)
        
        return pd.DataFrame(users), pd.DataFrame(school_admins), mentor_assignments
    
    def generate_students(self, programs):
        """Generate students per program"""
        students = []
        student_id = 1
        
        for _, program in programs.iterrows():
            n_students = self.students_per_program
            
            for i in range(n_students):
                # Enrollment date (within last 4 years)
                enrollment_date = datetime.now() - timedelta(days=random.randint(30, 1460))
                
                # Determine year of study based on enrollment date
                days_since_enrollment = (datetime.now() - enrollment_date).days
                year_of_study = min(4, (days_since_enrollment // 365) + 1)
                
                students.append({
                    'id': student_id,
                    'student_code': f'STU{program["program_code"]}{str(student_id).zfill(5)}',
                    'program_id': program['id'],
                    'school_id': program['school_id'],
                    'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
                    'year_of_study': year_of_study,
                    'status': random.choice(['active'] * 92 + ['inactive'] * 5 + ['graduated'] * 3),
                    'gpa': None  # Will be calculated from enrollments
                })
                student_id += 1
        
        return pd.DataFrame(students)
    
    def generate_courses(self, programs):
        """Generate courses per program"""
        courses = []
        course_id = 1
        
        for _, program in programs.iterrows():
            prog_code = program['program_code']
            course_list = self.program_courses.get(prog_code, [])
            
            for i, course_name in enumerate(course_list):
                # Assign to year levels
                year_level = (i // 3) + 1  # 3 courses per year
                semester = 1 if (i % 2) == 0 else 2
                
                courses.append({
                    'id': course_id,
                    'course_code': f'{prog_code}{year_level}{str(i+1).zfill(2)}',
                    'course_name': course_name,
                    'program_id': program['id'],
                    'school_id': program['school_id'],
                    'credits': random.choice([3, 4]),
                    'year_level': year_level,
                    'semester': semester
                })
                course_id += 1
        
        return pd.DataFrame(courses)
    
    def generate_sis_enrollments(self, students, courses):
        """SIS: Student enrollments with grades"""
        enrollments = []
        enrollment_id = 1
        
        for _, student in students.iterrows():
            # Get courses for this student's program
            program_courses = courses[courses['program_id'] == student['program_id']]
            
            # Student takes courses appropriate to their year
            eligible_courses = program_courses[
                program_courses['year_level'] <= student['year_of_study']
            ]
            
            # Sample 5-8 courses for current semester
            n_courses = min(random.randint(5, 8), len(eligible_courses))
            if n_courses > 0:
                student_courses = eligible_courses.sample(n=n_courses)
                
                for _, course in student_courses.iterrows():
                    # Generate realistic grade distribution
                    # Some students at risk (lower grades)
                    grade_value = random.choices(
                        [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.0, 0.0],
                        weights=[15, 18, 17, 15, 12, 10, 6, 4, 2, 1]
                    )[0]
                    
                    status_choice = random.choices(
                        ['enrolled', 'completed', 'dropped', 'failed'],
                        weights=[65, 28, 4, 3]
                    )[0]
                    
                    # Set grade based on status
                    if status_choice == 'failed':
                        grade_value = random.choice([1.0, 0.0])
                    elif status_choice == 'dropped':
                        grade_value = None
                    
                    enrollments.append({
                        'id': enrollment_id,
                        'student_id': student['id'],
                        'course_id': course['id'],
                        'semester': f'{"Sem1" if course["semester"] == 1 else "Sem2"}_2024',
                        'grade_points': grade_value,
                        'status': status_choice,
                        'enrollment_date': student['enrollment_date'],
                        'is_repeating': random.choice([False] * 95 + [True] * 5)
                    })
                    enrollment_id += 1
        
        return pd.DataFrame(enrollments)
    
    def generate_lms_activities(self, students):
        """LMS: Login activity, assignments, engagement (Strathmore iLearn)"""
        activities = []
        activity_id = 1
        
        for _, student in students.iterrows():
            # Generate weekly LMS data for past 12 weeks
            for week in range(1, 13):
                # Student engagement patterns (some at-risk students have low engagement)
                engagement_level = random.choices(
                    ['high', 'medium', 'low', 'very_low'],
                    weights=[0.50, 0.30, 0.15, 0.05]
                )[0]
                
                if engagement_level == 'high':
                    logins = random.randint(12, 25)
                    time_spent = random.randint(400, 700)
                    assignments_done = random.randint(4, 5)
                    avg_score = random.uniform(75, 95)
                    quiz_attempts = random.randint(3, 5)
                    resources = random.randint(15, 30)
                elif engagement_level == 'medium':
                    logins = random.randint(6, 12)
                    time_spent = random.randint(200, 400)
                    assignments_done = random.randint(3, 4)
                    avg_score = random.uniform(60, 75)
                    quiz_attempts = random.randint(2, 3)
                    resources = random.randint(8, 15)
                elif engagement_level == 'low':
                    logins = random.randint(2, 6)
                    time_spent = random.randint(60, 200)
                    assignments_done = random.randint(1, 3)
                    avg_score = random.uniform(45, 60)
                    quiz_attempts = random.randint(1, 2)
                    resources = random.randint(3, 8)
                else:  # very_low
                    logins = random.randint(0, 2)
                    time_spent = random.randint(0, 60)
                    assignments_done = random.randint(0, 1)
                    avg_score = random.uniform(20, 45)
                    quiz_attempts = random.randint(0, 1)
                    resources = random.randint(0, 3)
                
                # Calculate engagement score (0-100)
                engagement_score = min(100, 
                    (logins * 1.5) + 
                    (assignments_done * 15) + 
                    (quiz_attempts * 10) + 
                    (resources * 0.5)
                ) / 1.5
                
                activities.append({
                    'id': activity_id,
                    'student_id': student['id'],
                    'week_number': week,
                    'academic_year': 2024,
                    'login_count': logins,
                    'time_spent_minutes': time_spent,
                    'assignments_submitted': assignments_done,
                    'assignments_total': 5,
                    'avg_assignment_score': round(avg_score, 2),
                    'quizzes_attempted': quiz_attempts,
                    'resources_accessed': resources,
                    'discussion_posts': random.randint(0, 5),
                    'engagement_score': round(engagement_score, 2)
                })
                activity_id += 1
        
        return pd.DataFrame(activities)
    
    def generate_attendance(self, students):
        """Attendance: Daily records"""
        records = []
        record_id = 1
        
        for _, student in students.iterrows():
            # Generate 60 days of attendance (12 weeks)
            attendance_pattern = random.choices(
                ['excellent', 'good', 'average', 'poor', 'critical'],
                weights=[0.40, 0.35, 0.15, 0.07, 0.03]
            )[0]
            
            # Define attendance probabilities
            if attendance_pattern == 'excellent':
                present_prob = 0.97
            elif attendance_pattern == 'good':
                present_prob = 0.88
            elif attendance_pattern == 'average':
                present_prob = 0.75
            elif attendance_pattern == 'poor':
                present_prob = 0.60
            else:  # critical
                present_prob = 0.45
            
            start_date = datetime.now() - timedelta(days=60)
            consecutive_absences = 0
            
            for day in range(60):
                date = start_date + timedelta(days=day)
                
                # Only weekdays
                if date.weekday() < 5:
                    status = random.choices(
                        ['present', 'absent', 'late', 'excused'],
                        weights=[present_prob, (1-present_prob)*0.7, 0.05, (1-present_prob)*0.3]
                    )[0]
                    
                    if status == 'absent':
                        consecutive_absences += 1
                    else:
                        consecutive_absences = 0
                    
                    records.append({
                        'id': record_id,
                        'student_id': student['id'],
                        'date': date.strftime('%Y-%m-%d'),
                        'status': status,
                        'consecutive_absences': consecutive_absences
                    })
                    record_id += 1
        
        return pd.DataFrame(records)
    
    def save_all(self, data_dict):
        """Save all dataframes to CSV"""
        import os
        os.makedirs('data', exist_ok=True)
        
        print("\n" + "=" * 70)
        print("SAVING STRATHMORE DATA TO CSV FILES")
        print("=" * 70)
        
        for name, df in data_dict.items():
            filepath = f'data/{name}.csv'
            df.to_csv(filepath, index=False)
            print(f"  → {filepath:<40} ({len(df):>6,} records)")
        
        print("\n" + "=" * 70)
        print("✅ STRATHMORE DATA GENERATED SUCCESSFULLY!")
        print("=" * 70)
        
        # Summary statistics
        print("\n📊 DATA SUMMARY:")
        print(f"  • Schools: 5 (SCES, SBS, STH, SLS, SHSS)")
        print(f"  • Programs: {len(data_dict['programs'])}")
        print(f"  • Students: {len(data_dict['students']):,}")
        print(f"  • Users: {len(data_dict['users'])} (1 admin, 5 deans, mentors)")
        print(f"  • Courses: {len(data_dict['courses']):,}")
        print(f"  • Total Records: {sum(len(df) for df in data_dict.values()):,}")
        
        print(f"\n📁 Location: {os.path.abspath('data')}/")
        
        print("\n📋 Generated files:")
        for name in data_dict.keys():
            print(f"  ✓ {name}.csv")
        
        print("\n" + "=" * 70)
        print("🎓 STRATHMORE UNIVERSITY STRUCTURE:")
        print("=" * 70)
        for code, info in self.schools_programs.items():
            print(f"\n{code} - {info['name']}")
            print(f"  Programs: {', '.join(info['programs'])}")
        
        print("\n" + "=" * 70)
        print("\n🎉 Ready for Laravel backend integration!")
        print("Next: Import this data into MySQL database\n")

if __name__ == "__main__":
    generator = StrathmoreDataGenerator(students_per_program=40)
    generator.generate_all()