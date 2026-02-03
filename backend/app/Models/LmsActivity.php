<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class LmsActivity extends Model
{
    use HasFactory;

    protected $fillable = [
        'student_id',
        'week_number',
        'academic_year',
        'login_count',
        'time_spent_minutes',
        'assignments_submitted',
        'assignments_total',
        'avg_assignment_score',
        'quizzes_attempted',
        'resources_accessed',
        'discussion_posts',
        'engagement_score',
    ];

    protected $casts = [
        'avg_assignment_score' => 'decimal:2',
        'engagement_score' => 'decimal:2',
    ];

    // Relationships
    public function student()
    {
        return $this->belongsTo(Student::class);
    }
}