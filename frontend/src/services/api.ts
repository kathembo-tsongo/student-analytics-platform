import axios from 'axios'
import type { LoginResponse, AdminDashboard, Student } from '@/types'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const login = async (email: string, password: string): Promise<LoginResponse> => {
  const { data } = await api.post('/auth/login', { email, password })
  return data
}

export const logout = async (): Promise<void> => {
  await api.post('/auth/logout')
}

export const getProfile = async () => {
  const { data } = await api.get('/auth/profile')
  return data
}

// Admin
export const getAdminDashboard = async (): Promise<AdminDashboard> => {
  const { data } = await api.get('/admin/dashboard')
  return data
}

export const getAdminAnalytics = async () => {
  const { data } = await api.get('/admin/analytics')
  return data
}

export const getSchools = async () => {
  const { data } = await api.get('/admin/schools')
  return data
}

export const getSchool = async (id: number) => {
  const { data } = await api.get(`/admin/schools/${id}`)
  return data
}

export const getUsers = async () => {
  const { data } = await api.get('/admin/users')
  return data
}

// School Admin
export const getSchoolAdminDashboard = async () => {
  const { data } = await api.get('/school-admin/dashboard')
  return data
}

export const getSchoolAdminStudents = async (): Promise<{ data: Student[] }> => {
  const { data } = await api.get('/school-admin/students')
  return data
}

export const getSchoolAdminStudent = async (id: number) => {
  const { data } = await api.get(`/school-admin/students/${id}`)
  return data
}

// Mentor
export const getMentorDashboard = async () => {
  const { data } = await api.get('/mentor/dashboard')
  return data
}

export const getMentorStudents = async (): Promise<{ data: Student[] }> => {
  const { data } = await api.get('/mentor/students')
  return data
}

export const getMentorStudent = async (id: number) => {
  const { data } = await api.get(`/mentor/students/${id}`)
  return data
}

export default api
