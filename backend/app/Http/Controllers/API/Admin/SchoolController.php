<?php

namespace App\Http\Controllers\API\Admin;

use App\Http\Controllers\Controller;
use App\Models\School;
use Illuminate\Http\Request;

class SchoolController extends Controller
{
    /**
     * List all schools
     */
    public function index()
    {
        $schools = School::with(['programs', 'schoolAdmins.user'])
            ->withCount(['students', 'programs'])
            ->get();

        return response()->json($schools);
    }

    /**
     * Get specific school details
     */
    public function show($id)
    {
        $school = School::with([
            'programs.students',
            'schoolAdmins.user',
            'students.program'
        ])
        ->withCount(['students', 'programs', 'courses'])
        ->findOrFail($id);

        // Calculate school-level stats
        $stats = [
            'total_students' => $school->students()->count(),
            'active_students' => $school->students()->where('status', 'active')->count(),
            'avg_gpa' => round($school->students()->avg('gpa'), 2),
            'programs_offered' => $school->programs()->count(),
        ];

        return response()->json([
            'school' => $school,
            'stats' => $stats,
        ]);
    }
}