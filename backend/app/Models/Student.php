<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    use HasFactory;

    protected $fillable = [
        'student_code',
        'program_id',
        'school_id',
        'enrollment_date',
        'year_of_study',
        'status',
        'gpa',
    ];

    protected $casts = [
        'enrollment_date' => 'date',
        'gpa' => 'decimal:2',
    ];

    // Relationships
    public function program()
    {
        return $this->belongsTo(Program::class);
    }

    public function school()
    {
        return $this->belongsTo(School::class);
    }

    public function sisEnrollments()
    {
        return $this->hasMany(SisEnrollment::class);
    }

    public function lmsActivities()
    {
        return $this->hasMany(LmsActivity::class);
    }

    public function attendanceRecords()
    {
        return $this->hasMany(AttendanceRecord::class);
    }

    public function mentorAssignments()
    {
        return $this->hasMany(MentorAssignment::class);
    }

    public function currentMentor()
    {
        return $this->hasOne(MentorAssignment::class)
            ->where('status', 'active')
            ->latest();
    }

    // Helper: Calculate current GPA from enrollments
    public function calculateGpa()
    {
        return $this->sisEnrollments()
            ->where('status', 'completed')
            ->avg('grade_points');
    }

    // Helper: Get latest risk score (you'll implement this later)
    public function latestRiskScore()
    {
        // Will connect to risk_scores table later
        return null;
    }
}