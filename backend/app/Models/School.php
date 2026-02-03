<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class School extends Model
{
    use HasFactory;

    protected $fillable = [
        'school_code',
        'school_name',
        'university',
        'status',
    ];

    // Relationships
    public function programs()
    {
        return $this->hasMany(Program::class);
    }

    public function students()
    {
        return $this->hasMany(Student::class);
    }

    public function courses()
    {
        return $this->hasMany(Course::class);
    }

    public function schoolAdmins()
    {
        return $this->hasMany(SchoolAdmin::class);
    }

    public function mentorAssignments()
    {
        return $this->hasMany(MentorAssignment::class);
    }
}