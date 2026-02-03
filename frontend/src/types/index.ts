export interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'school_admin' | 'mentor'
  status: string
}

export interface LoginResponse {
  user: User
  token: string
}

export interface School {
  id: number
  school_code: string
  school_name: string
  university: string
  students_count?: number
}

export interface Program {
  id: number
  program_code: string
  program_name: string
  school_id: number
  degree_type: string
}

export interface Student {
  id: number
  student_code: string
  program_id: number
  school_id: number
  enrollment_date: string
  year_of_study: number
  status: string
  gpa: number | null
  program?: Program
  school?: School
}

export interface DashboardStats {
  total_schools?: number
  total_students?: number
  total_users?: number
  total_programs?: number
  active_students?: number
  avg_gpa?: number
  assigned_students_count?: number
}

export interface AdminDashboard {
  stats: DashboardStats
  schools: School[]
  users_by_role: {
    admins: number
    school_admins: number
    mentors: number
  }
}
