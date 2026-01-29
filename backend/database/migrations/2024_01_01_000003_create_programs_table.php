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
