<?php

namespace App\Http\Controllers\API\Mentor;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * Mentor Dashboard
     */
    public function index(Request $request)
    {
        $user = $request->user();

        // Get assigned students
        $assignedStudents = $user->assignedStudents()
            ->with(['program', 'school'])
            ->get();

        $stats = [
            'total_assigned' => $assignedStudents->count(),
            'active_students' => $assignedStudents->where('status', 'active')->count(),
            'avg_gpa' => round($assignedStudents->avg('gpa'), 2),
        ];

        // Students grouped by year
        $studentsByYear = $assignedStudents->groupBy('year_of_study')
            ->map(function($students, $year) {
                return [
                    'year' => $year,
                    'count' => $students->count(),
                ];
            })->values();

        return response()->json([
            'stats' => $stats,
            'students_by_year' => $studentsByYear,
            'recent_students' => $assignedStudents->take(10),
        ]);
    }
}