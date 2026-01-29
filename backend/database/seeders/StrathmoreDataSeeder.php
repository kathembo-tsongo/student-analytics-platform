<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use App\Models\User;
use Spatie\Permission\Models\Role;

class StrathmoreDataSeeder extends Seeder
{
    private $dataPath;

    public function __construct()
    {
        $this->dataPath = base_path('../analytics/data/');
    }

    public function run(): void
    {
        $this->command->info('🎓 Starting Strathmore data import with Spatie...');
        
        $this->createRoles();
        $this->importSchools();
        $this->importPrograms();
        $this->importUsers();
        $this->importSchoolAdmins();
        $this->importStudents();
        $this->importCourses();
        $this->importSisEnrollments();
        $this->importLmsActivities();
        $this->importAttendanceRecords();
        
        $this->command->info('✅ All data imported successfully with Spatie roles!');
    }

    /**
     * Helper method to check if a foreign key exists
     */
    private function foreignKeyExists($table, $id)
    {
        return DB::table($table)->where('id', $id)->exists();
    }

    /**
     * Helper method to safely get array value with default
     */
    private function getValue($array, $key, $default = null)
    {
        return $array[$key] ?? $default;
    }

    private function createRoles()
    {
        $this->command->info('Creating roles...');
        Role::firstOrCreate(['name' => 'admin', 'guard_name' => 'web']);
        Role::firstOrCreate(['name' => 'school_admin', 'guard_name' => 'web']);
        Role::firstOrCreate(['name' => 'mentor', 'guard_name' => 'web']);
        $this->command->info('✓ Roles created');
    }

    private function importSchools()
    {
        $this->command->info('Importing schools...');
        $file = $this->dataPath . 'schools.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ schools.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            DB::table('schools')->insert([
                'id' => $row['id'],
                'school_code' => $row['school_code'],
                'school_name' => $row['school_name'],
                'university' => $this->getValue($row, 'university', 'Strathmore University'),
                'status' => $this->getValue($row, 'status', 'active'),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
        $this->command->info('✓ Schools: ' . count($data));
    }

    private function importPrograms()
    {
        $this->command->info('Importing programs...');
        $file = $this->dataPath . 'programs.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ programs.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            DB::table('programs')->insert([
                'id' => $row['id'],
                'program_code' => $row['program_code'],
                'program_name' => $row['program_name'],
                'school_id' => $row['school_id'],
                'degree_type' => $row['degree_type'],
                'duration_years' => $row['duration_years'],
                'status' => $this->getValue($row, 'status', 'active'),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
        $this->command->info('✓ Programs: ' . count($data));
    }

    private function importUsers()
    {
        $this->command->info('Importing users with Spatie roles...');
        $file = $this->dataPath . 'users.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ users.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Check if role exists
            if (!isset($row['role']) || !Role::where('name', $row['role'])->exists()) {
                $this->command->warn("⚠ Skipping user {$row['email']} - invalid or missing role");
                continue;
            }
            
            // Insert user
            DB::table('users')->insert([
                'name' => $row['name'],
                'email' => $row['email'],
                'password' => Hash::make('password123'),
                'status' => $this->getValue($row, 'status', 'active'),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            // Get the created user and assign role
            $user = User::where('email', $row['email'])->first();
            if ($user) {
                $user->assignRole($row['role']);
            }
        }
        $this->command->info('✓ Users: ' . count($data));
    }

    private function importSchoolAdmins()
    {
        $this->command->info('Importing school admins...');
        $file = $this->dataPath . 'school_admins.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ school_admins.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate foreign keys
            if (!$this->foreignKeyExists('users', $row['user_id'])) {
                $this->command->warn("⚠ Skipping school admin - User ID {$row['user_id']} not found");
                $skipped++;
                continue;
            }
            
            if (!$this->foreignKeyExists('schools', $row['school_id'])) {
                $this->command->warn("⚠ Skipping school admin - School ID {$row['school_id']} not found");
                $skipped++;
                continue;
            }
            
            DB::table('school_admins')->insert([
                'id' => $row['id'],
                'user_id' => $row['user_id'],
                'school_id' => $row['school_id'],
                'assigned_date' => $row['assigned_date'],
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ School admins: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }

    private function importStudents()
    {
        $this->command->info('Importing students...');
        $file = $this->dataPath . 'students.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ students.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate foreign keys
            if (!$this->foreignKeyExists('programs', $row['program_id'])) {
                $this->command->warn("⚠ Skipping student - Program ID {$row['program_id']} not found");
                $skipped++;
                continue;
            }
            
            if (!$this->foreignKeyExists('schools', $row['school_id'])) {
                $this->command->warn("⚠ Skipping student - School ID {$row['school_id']} not found");
                $skipped++;
                continue;
            }
            
            DB::table('students')->insert([
                'id' => $row['id'],
                'student_code' => $row['student_code'],
                'program_id' => $row['program_id'],
                'school_id' => $row['school_id'],
                'enrollment_date' => $row['enrollment_date'],
                'year_of_study' => $row['year_of_study'],
                'status' => $row['status'],
                'gpa' => $row['gpa'] === '' ? null : $row['gpa'],
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ Students: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }

    private function importCourses()
    {
        $this->command->info('Importing courses...');
        $file = $this->dataPath . 'courses.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ courses.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate school exists
            if (!$this->foreignKeyExists('schools', $row['school_id'])) {
                $this->command->warn("⚠ Skipping course - School ID {$row['school_id']} not found");
                $skipped++;
                continue;
            }
            
            // Extract year level from course code (e.g., MAT101 -> 1, MAT201 -> 2)
            $yearLevel = isset($row['course_code']) ? (int)substr($row['course_code'], -2, 1) : 1;
            
            DB::table('courses')->insert([
                'id' => $row['id'],
                'course_code' => $row['course_code'],
                'course_name' => $row['course_name'],
                'program_id' => null, // Not in CSV
                'school_id' => $row['school_id'],
                'credits' => $row['credits'],
                'year_level' => $yearLevel,
                'semester' => 1, // Default semester
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ Courses: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }

    private function importSisEnrollments()
    {
        $this->command->info('Importing SIS enrollments...');
        $file = $this->dataPath . 'sis_enrollments.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ sis_enrollments.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate foreign keys
            if (!$this->foreignKeyExists('students', $row['student_id'])) {
                $skipped++;
                continue;
            }
            
            if (!$this->foreignKeyExists('courses', $row['course_id'])) {
                $skipped++;
                continue;
            }
            
            $isRepeating = $this->getValue($row, 'is_repeating', '0');
            
            DB::table('sis_enrollments')->insert([
                'id' => $row['id'],
                'student_id' => $row['student_id'],
                'course_id' => $row['course_id'],
                'semester' => $row['semester'],
                'enrollment_date' => $row['enrollment_date'],
                'status' => $row['status'],
                'grade_points' => $row['grade_points'] === '' ? null : $row['grade_points'],
                'is_repeating' => $isRepeating === 'True' || $isRepeating === '1' || $isRepeating === 'true',
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ SIS enrollments: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }

    private function importLmsActivities()
    {
        $this->command->info('Importing LMS activities...');
        $file = $this->dataPath . 'lms_activities.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ lms_activities.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate student exists
            if (!$this->foreignKeyExists('students', $row['student_id'])) {
                $skipped++;
                continue;
            }
            
            DB::table('lms_activities')->insert([
                'id' => $row['id'],
                'student_id' => $row['student_id'],
                'week_number' => $this->getValue($row, 'week_number', 1),
                'academic_year' => $this->getValue($row, 'academic_year', date('Y')),
                'login_count' => $this->getValue($row, 'login_count', 0),
                'time_spent_minutes' => $this->getValue($row, 'time_spent_minutes', 0),
                'assignments_submitted' => $this->getValue($row, 'assignments_submitted', 0),
                'assignments_total' => $this->getValue($row, 'assignments_total', 0),
                'avg_assignment_score' => ($this->getValue($row, 'avg_assignment_score', '') === '') ? null : $row['avg_assignment_score'],
                'quizzes_attempted' => $this->getValue($row, 'quizzes_attempted', 0),
                'resources_accessed' => $this->getValue($row, 'resources_accessed', 0),
                'discussion_posts' => $this->getValue($row, 'discussion_posts', 0),
                'engagement_score' => $this->getValue($row, 'engagement_score', 0),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ LMS activities: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }

    private function importAttendanceRecords()
    {
        $this->command->info('Importing attendance...');
        $file = $this->dataPath . 'attendance_records.csv';
        if (!file_exists($file)) {
            $this->command->warn('⚠ attendance_records.csv not found');
            return;
        }

        $data = array_map('str_getcsv', file($file));
        $headers = array_shift($data);
        
        $imported = 0;
        $skipped = 0;
        
        foreach ($data as $row) {
            $row = array_combine($headers, $row);
            
            // Validate student exists
            if (!$this->foreignKeyExists('students', $row['student_id'])) {
                $skipped++;
                continue;
            }
            
            DB::table('attendance_records')->insert([
                'id' => $row['id'],
                'student_id' => $row['student_id'],
                'date' => $row['date'],
                'status' => $this->getValue($row, 'status', 'present'),
                'consecutive_absences' => $this->getValue($row, 'consecutive_absences', 0),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            
            $imported++;
        }
        
        $this->command->info("✓ Attendance: {$imported} imported" . ($skipped > 0 ? ", {$skipped} skipped" : ""));
    }
}