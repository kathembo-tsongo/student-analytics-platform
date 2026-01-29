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
