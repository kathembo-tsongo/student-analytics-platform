<?php

namespace App\Http\Controllers\API\SchoolAdmin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * School Admin Dashboard
     */
    public function index(Request $request)
    {
        $user = $request->user();
        $schoolAdmin = $user->schoolAdmin()->with('school')->first();

        if (!$schoolAdmin) {
            return response()->json(['message' => 'Not assigned to any school'], 403);
        }

        $school = $schoolAdmin->school;

        // School statistics
        $stats = [
            'total_students' => $school->students()->count(),
            'active_students' => $school->students()->where('status', 'active')->count(),
            'total_programs' => $school->programs()->count(),
            'avg_gpa' => round($school->students()->avg('gpa'), 2),
        ];

        // Students by program
        $studentsByProgram = $school->programs()
            ->withCount('students')
            ->get()
            ->map(function($program) {
                return [
                    'program_code' => $program->program_code,
                    'program_name' => $program->program_name,
                    'student_count' => $program->students_count,
                ];
            });

        // Recent students (last 30 days)
        $recentStudents = $school->students()
            ->where('enrollment_date', '>=', now()->subDays(30))
            ->with('program')
            ->latest('enrollment_date')
            ->take(10)
            ->get();

        return response()->json([
            'school' => [
                'id' => $school->id,
                'name' => $school->school_name,
                'code' => $school->school_code,
            ],
            'stats' => $stats,
            'students_by_program' => $studentsByProgram,
            'recent_students' => $recentStudents,
        ]);
    }
}