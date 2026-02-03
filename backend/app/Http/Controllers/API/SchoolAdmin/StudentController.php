<?php

namespace App\Http\Controllers\API\SchoolAdmin;

use App\Http\Controllers\Controller;
use App\Models\Student;
use Illuminate\Http\Request;

class StudentController extends Controller
{
    /**
     * List students in school admin's school
     */
    public function index(Request $request)
    {
        $user = $request->user();
        $schoolAdmin = $user->schoolAdmin;

        if (!$schoolAdmin) {
            return response()->json(['message' => 'Not assigned to any school'], 403);
        }

        $query = Student::where('school_id', $schoolAdmin->school_id)
            ->with(['program', 'currentMentor.mentor']);

        // Filter by program
        if ($request->has('program_id')) {
            $query->where('program_id', $request->program_id);
        }

        // Filter by year
        if ($request->has('year_of_study')) {
            $query->where('year_of_study', $request->year_of_study);
        }

        // Filter by status
        if ($request->has('status')) {
            $query->where('status', $request->status);
        }

        $students = $query->paginate(20);

        return response()->json($students);
    }

    /**
     * Get specific student details
     */
    public function show(Request $request, $id)
    {
        $user = $request->user();
        $schoolAdmin = $user->schoolAdmin;

        $student = Student::where('school_id', $schoolAdmin->school_id)
            ->with([
                'program',
                'school',
                'sisEnrollments.course',
                'lmsActivities' => function($query) {
                    $query->latest()->take(12);
                },
                'attendanceRecords' => function($query) {
                    $query->latest()->take(30);
                },
                'currentMentor.mentor'
            ])
            ->findOrFail($id);

        return response()->json($student);
    }
}