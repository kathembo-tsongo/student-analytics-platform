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
