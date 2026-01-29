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
