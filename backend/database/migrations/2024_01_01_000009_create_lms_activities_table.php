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
