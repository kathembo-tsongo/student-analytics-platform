import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/auth/LoginPage'
import AdminDashboard from './pages/admin/AdminDashboard'
import SchoolsPage from './pages/admin/SchoolsPage'
import UsersPage from './pages/admin/UsersPage'
import AtRiskStudentsPage from './pages/admin/AtRiskStudentsPage'
import SchoolAdminDashboard from './pages/school-admin/SchoolAdminDashboard'
import StudentsPage from './pages/school-admin/StudentsPage'
import SchoolAdminAtRiskPage from './pages/school-admin/AtRiskStudentsPage'
import MentorDashboard from './pages/mentor/MentorDashboard'
import MyStudentsPage from './pages/mentor/MyStudentsPage'
import MentorAtRiskPage from './pages/mentor/AtRiskStudentsPage'
import ProtectedRoute from './components/auth/ProtectedRoute'

function App() {
  const { isAuthenticated, user } = useAuthStore()

  const getDefaultRoute = () => {
    if (!isAuthenticated || !user) return '/login'
    
    switch (user.role) {
      case 'admin':
        return '/admin'
      case 'school_admin':
        return '/school-admin'
      case 'mentor':
        return '/mentor'
      default:
        return '/login'
    }
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        {/* Admin Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/schools"
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <SchoolsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <UsersPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/analytics"
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <AtRiskStudentsPage />
            </ProtectedRoute>
          }
        />
        
        {/* School Admin Routes */}
        <Route
          path="/school-admin"
          element={
            <ProtectedRoute allowedRoles={['school_admin']}>
              <SchoolAdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/school-admin/students"
          element={
            <ProtectedRoute allowedRoles={['school_admin']}>
              <StudentsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/school-admin/at-risk"
          element={
            <ProtectedRoute allowedRoles={['school_admin']}>
              <SchoolAdminAtRiskPage />
            </ProtectedRoute>
          }
        />
        
        {/* Mentor Routes */}
        <Route
          path="/mentor"
          element={
            <ProtectedRoute allowedRoles={['mentor']}>
              <MentorDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/mentor/students"
          element={
            <ProtectedRoute allowedRoles={['mentor']}>
              <MyStudentsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/mentor/at-risk"
          element={
            <ProtectedRoute allowedRoles={['mentor']}>
              <MentorAtRiskPage />
            </ProtectedRoute>
          }
        />
        
        <Route path="/" element={<Navigate to={getDefaultRoute()} replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
