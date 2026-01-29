<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('courses', function (Blueprint $table) {
            $table->id();
            $table->string('course_code');
            $table->string('course_name');
            $table->foreignId('program_id')->nullable()->constrained()->onDelete('cascade'); // Add ->nullable()
            $table->foreignId('school_id')->constrained()->onDelete('cascade');
            $table->integer('credits');
            $table->integer('year_level');
            $table->integer('semester');
            $table->timestamps();
        });
    }
    public function down(): void
    {
        Schema::dropIfExists('courses');
    }
};
