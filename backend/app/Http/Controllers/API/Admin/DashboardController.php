<?php

namespace App\Http\Controllers\API\Admin;

use App\Http\Controllers\Controller;
use App\Models\School;
use App\Models\Student;
use App\Models\User;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * Admin Dashboard Overview
     */
    public function index()
    {
        $stats = [
            'total_schools' => School::count(),
            'total_students' => Student::where('status', 'active')->count(),
            'total_users' => User::where('status', 'active')->count(),
            'total_programs' => \App\Models\Program::count(),
        ];

        // School breakdown
        $schools = School::withCount([
            'students' => function($query) {
                $query->where('status', 'active');
            }
        ])->get();

        // User role breakdown
        $usersByRole = [
            'admins' => User::role('admin')->count(),
            'school_admins' => User::role('school_admin')->count(),
            'mentors' => User::role('mentor')->count(),
        ];

        return response()->json([
            'stats' => $stats,
            'schools' => $schools,
            'users_by_role' => $usersByRole,
        ]);
    }

    /**
     * System-wide analytics
     */
    public function analytics()
    {
        // Overall student status distribution
        $studentsByStatus = Student::select('status')
            ->groupBy('status')
            ->selectRaw('status, count(*) as count')
            ->get();

        // Average GPA by school
        $gpaBySchool = School::with('students')
            ->get()
            ->map(function($school) {
                return [
                    'school_name' => $school->school_name,
                    'school_code' => $school->school_code,
                    'avg_gpa' => $school->students()->avg('gpa'),
                    'student_count' => $school->students()->count(),
                ];
            });

        return response()->json([
            'students_by_status' => $studentsByStatus,
            'gpa_by_school' => $gpaBySchool,
        ]);
    }
}