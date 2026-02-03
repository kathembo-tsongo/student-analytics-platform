<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'role' => \Spatie\Permission\Middleware\RoleMiddleware::class,              // ← Changed
            'permission' => \Spatie\Permission\Middleware\PermissionMiddleware::class,  // ← Changed
            'role_or_permission' => \Spatie\Permission\Middleware\RoleOrPermissionMiddleware::class,  // ← Changed
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();