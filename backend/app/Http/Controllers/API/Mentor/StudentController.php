<?php

namespace App\Http\Controllers\API\Mentor;

use App\Http\Controllers\Controller;
use App\Models\Student;
use Illuminate\Http\Request;

class StudentController extends Controller
{
    /**
     * List mentor's assigned students
     */
    public function index(Request $request)
    {
        $user = $request->user();

        $students = $user->assignedStudents()
            ->with(['program', 'school'])
            ->paginate(20);

        return response()->json($students);
    }

    /**
     * Get specific student details (only if assigned to mentor)
     */
    public function show(Request $request, $id)
    {
        $user = $request->user();

        $student = $user->assignedStudents()
            ->with([
                'program',
                'school',
                'sisEnrollments.course',
                'lmsActivities' => function($query) {
                    $query->latest()->take(12);
                },
                'attendanceRecords' => function($query) {
                    $query->latest()->take(60);
                }
            ])
            ->findOrFail($id);

        // Calculate additional metrics
        $metrics = [
            'current_courses' => $student->sisEnrollments()
                ->where('status', 'enrolled')
                ->count(),
            'completed_courses' => $student->sisEnrollments()
                ->where('status', 'completed')
                ->count(),
            'recent_attendance_rate' => $this->calculateAttendanceRate($student, 30),
            'avg_lms_engagement' => $student->lmsActivities()
                ->where('academic_year', 2024)
                ->avg('engagement_score'),
        ];

        return response()->json([
            'student' => $student,
            'metrics' => $metrics,
        ]);
    }

    /**
     * Helper: Calculate attendance rate
     */
    private function calculateAttendanceRate($student, $days)
    {
        $records = $student->attendanceRecords()
            ->where('date', '>=', now()->subDays($days))
            ->get();

        if ($records->isEmpty()) {
            return null;
        }

        $present = $records->where('status', 'present')->count();
        return round(($present / $records->count()) * 100, 2);
    }
}