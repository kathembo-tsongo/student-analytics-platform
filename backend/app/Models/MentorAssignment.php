<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class MentorAssignment extends Model
{
    use HasFactory;

    protected $fillable = [
        'mentor_id',
        'student_id',
        'school_id',
        'assignment_date',
        'end_date',
        'status',
    ];

    protected $casts = [
        'assignment_date' => 'date',
        'end_date' => 'date',
    ];

    // Relationships
    public function mentor()
    {
        return $this->belongsTo(User::class, 'mentor_id');
    }

    public function student()
    {
        return $this->belongsTo(Student::class);
    }

    public function school()
    {
        return $this->belongsTo(School::class);
    }
}