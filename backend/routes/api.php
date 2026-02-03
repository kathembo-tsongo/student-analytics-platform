<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;
use App\Http\Controllers\API\Admin\DashboardController as AdminDashboardController;
use App\Http\Controllers\API\Admin\SchoolController as AdminSchoolController;
use App\Http\Controllers\API\Admin\UserController as AdminUserController;
use App\Http\Controllers\API\SchoolAdmin\DashboardController as SchoolAdminDashboardController;
use App\Http\Controllers\API\SchoolAdmin\StudentController as SchoolAdminStudentController;
use App\Http\Controllers\API\Mentor\DashboardController as MentorDashboardController;
use App\Http\Controllers\API\Mentor\StudentController as MentorStudentController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
| All routes automatically prefixed with /api
*/

// Public routes (no authentication required)
Route::post('auth/login', [AuthController::class, 'login']);

// Protected routes (require authentication)
Route::middleware('auth:sanctum')->group(function () {
    
    // Auth routes
    Route::post('auth/logout', [AuthController::class, 'logout']);
    Route::get('auth/profile', [AuthController::class, 'profile']);
    
    // Admin routes
    Route::middleware('role:admin')->prefix('admin')->group(function () {
        Route::get('dashboard', [AdminDashboardController::class, 'index']);
        Route::get('analytics', [AdminDashboardController::class, 'analytics']);
        
        // Schools management
        Route::get('schools', [AdminSchoolController::class, 'index']);
        Route::get('schools/{id}', [AdminSchoolController::class, 'show']);
        
        // Users management
        Route::get('users', [AdminUserController::class, 'index']);
        Route::get('users/{id}', [AdminUserController::class, 'show']);
    });
    
    // School Admin routes
    Route::middleware('role:school_admin')->prefix('school-admin')->group(function () {
        Route::get('dashboard', [SchoolAdminDashboardController::class, 'index']);
        
        // Students in their school
        Route::get('students', [SchoolAdminStudentController::class, 'index']);
        Route::get('students/{id}', [SchoolAdminStudentController::class, 'show']);
    });
    
    // Mentor routes
    Route::middleware('role:mentor')->prefix('mentor')->group(function () {
        Route::get('dashboard', [MentorDashboardController::class, 'index']);
        
        // Assigned students only
        Route::get('students', [MentorStudentController::class, 'index']);
        Route::get('students/{id}', [MentorStudentController::class, 'show']);
    });
});
