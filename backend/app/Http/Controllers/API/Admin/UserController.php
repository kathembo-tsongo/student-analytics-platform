<?php

namespace App\Http\Controllers\API\Admin;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * List all users
     */
    public function index(Request $request)
    {
        $query = User::with('roles');

        // Filter by role
        if ($request->has('role')) {
            $query->role($request->role);
        }

        // Filter by status
        if ($request->has('status')) {
            $query->where('status', $request->status);
        }

        $users = $query->paginate(20);

        return response()->json($users);
    }

    /**
     * Get specific user
     */
    public function show($id)
    {
        $user = User::with(['roles', 'schoolAdmin.school', 'mentorAssignments.student'])
            ->findOrFail($id);

        return response()->json($user);
    }
}