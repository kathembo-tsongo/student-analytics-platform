<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Course extends Model
{
    use HasFactory;

    protected $fillable = [
        'course_code',
        'course_name',
        'program_id',
        'school_id',
        'credits',
        'year_level',
        'semester',
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
}