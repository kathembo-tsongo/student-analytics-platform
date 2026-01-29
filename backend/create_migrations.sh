#!/bin/bash

echo "Creating Laravel migration files..."

# Check if we're in Laravel directory
if [ ! -f "artisan" ]; then
    echo "❌ Error: Not in Laravel backend directory"
    exit 1
fi

mkdir -p database/migrations

# 1. Users
cat > database/migrations/2024_01_01_000001_create_users_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->string('password');
            $table->enum('role', ['admin', 'school_admin', 'mentor'])->default('mentor');
            $table->enum('status', ['active', 'inactive'])->default('active');
            $table->rememberToken();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('users'); }
};
EOFILE
echo "✓ users"

# 2. Schools
cat > database/migrations/2024_01_01_000002_create_schools_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('schools', function (Blueprint $table) {
            $table->id();
            $table->string('school_code', 50)->unique();
            $table->string('school_name');
            $table->string('university')->default('Strathmore University');
            $table->enum('status', ['active', 'inactive'])->default('active');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('schools'); }
};
EOFILE
echo "✓ schools"

# 3. Programs
cat > database/migrations/2024_01_01_000003_create_programs_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('programs', function (Blueprint $table) {
            $table->id();
            $table->string('program_code', 50)->unique();
            $table->string('program_name');
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->string('degree_type', 100);
            $table->integer('duration_years')->default(4);
            $table->enum('status', ['active', 'inactive'])->default('active');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('programs'); }
};
EOFILE
echo "✓ programs"

# 4. School Admins
cat > database/migrations/2024_01_01_000004_create_school_admins_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('school_admins', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->date('assigned_date');
            $table->timestamps();
            $table->unique(['user_id', 'school_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('school_admins'); }
};
EOFILE
echo "✓ school_admins"

# 5. Students
cat > database/migrations/2024_01_01_000005_create_students_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('students', function (Blueprint $table) {
            $table->id();
            $table->string('student_code', 50)->unique();
            $table->foreignId('program_id')->constrained()->onDelete('cascade');
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->date('enrollment_date');
            $table->integer('year_of_study')->default(1);
            $table->enum('status', ['active', 'inactive', 'graduated', 'transferred'])->default('active');
            $table->decimal('gpa', 3, 2)->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('students'); }
};
EOFILE
echo "✓ students"

# 6. Courses
cat > database/migrations/2024_01_01_000006_create_courses_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('courses', function (Blueprint $table) {
            $table->id();
            $table->string('course_code', 50)->unique();
            $table->string('course_name');
            $table->foreignId('program_id')->constrained()->onDelete('cascade');
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->integer('credits')->default(3);
            $table->integer('year_level')->default(1);
            $table->integer('semester')->default(1);
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('courses'); }
};
EOFILE
echo "✓ courses"

# 7. Mentor Assignments
cat > database/migrations/2024_01_01_000007_create_mentor_assignments_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('mentor_assignments', function (Blueprint $table) {
            $table->id();
            $table->foreignId('mentor_id')->constrained('users')->onDelete('cascade');
            $table->foreignId('student_id')->constrained()->onDelete('cascade');
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->date('assignment_date');
            $table->date('end_date')->nullable();
            $table->enum('status', ['active', 'completed'])->default('active');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('mentor_assignments'); }
};
EOFILE
echo "✓ mentor_assignments"

# 8. SIS Enrollments
cat > database/migrations/2024_01_01_000008_create_sis_enrollments_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('sis_enrollments', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->onDelete('cascade');
            $table->foreignId('course_id')->constrained()->onDelete('cascade');
            $table->string('semester', 50);
            $table->date('enrollment_date');
            $table->enum('status', ['enrolled', 'completed', 'dropped', 'failed'])->default('enrolled');
            $table->decimal('grade_points', 3, 2)->nullable();
            $table->boolean('is_repeating')->default(false);
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('sis_enrollments'); }
};
EOFILE
echo "✓ sis_enrollments"

# 9. LMS Activities
cat > database/migrations/2024_01_01_000009_create_lms_activities_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('lms_activities', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->onDelete('cascade');
            $table->integer('week_number');
            $table->integer('academic_year');
            $table->integer('login_count')->default(0);
            $table->integer('time_spent_minutes')->default(0);
            $table->integer('assignments_submitted')->default(0);
            $table->integer('assignments_total')->default(0);
            $table->decimal('avg_assignment_score', 5, 2)->nullable();
            $table->integer('quizzes_attempted')->default(0);
            $table->integer('resources_accessed')->default(0);
            $table->integer('discussion_posts')->default(0);
            $table->decimal('engagement_score', 5, 2)->default(0);
            $table->timestamps();
            $table->unique(['student_id', 'week_number', 'academic_year']);
        });
    }
    public function down(): void { Schema::dropIfExists('lms_activities'); }
};
EOFILE
echo "✓ lms_activities"

# 10. Attendance Records
cat > database/migrations/2024_01_01_000010_create_attendance_records_table.php << 'EOFILE'
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('attendance_records', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->onDelete('cascade');
            $table->date('date');
            $table->enum('status', ['present', 'absent', 'late', 'excused']);
            $table->integer('consecutive_absences')->default(0);
            $table->timestamps();
            $table->unique(['student_id', 'date']);
        });
    }
    public function down(): void { Schema::dropIfExists('attendance_records'); }
};
EOFILE
echo "✓ attendance_records"

echo ""
echo "✅ All 10 migration files created!"
echo ""
ls -lh database/migrations/2024_01_01_*.php
