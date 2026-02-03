import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { StatCard } from '@/components/ui/stat-card'
import { getAdminDashboard } from '@/services/api'
import type { AdminDashboard as AdminDashboardType } from '@/types'
import { Users, School, GraduationCap, TrendingUp, BookOpen } from 'lucide-react'

export default function AdminDashboard() {
  const [data, setData] = useState<AdminDashboardType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getAdminDashboard()
        setData(response)
      } catch (error) {
        console.error('Error fetching dashboard:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <DashboardLayout title="Admin Dashboard">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading dashboard...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout title="Admin Dashboard">
      <div className="space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total Schools"
            value={data?.stats.total_schools || 0}
            icon={School}
            color="blue"
            trend={{ value: 5, isPositive: true }}
          />
          <StatCard
            title="Total Students"
            value={data?.stats.total_students || 0}
            icon={Users}
            color="green"
            trend={{ value: 12, isPositive: true }}
          />
          <StatCard
            title="Total Programs"
            value={data?.stats.total_programs || 0}
            icon={BookOpen}
            color="purple"
            trend={{ value: 3, isPositive: true }}
          />
          <StatCard
            title="System Users"
            value={data?.stats.total_users || 0}
            icon={TrendingUp}
            color="orange"
            trend={{ value: 8, isPositive: true }}
          />
        </div>

        {/* Schools Overview */}
        <Card className="shadow-soft">
          <CardHeader className="border-b bg-gradient-to-r from-blue-50 to-purple-50">
            <CardTitle className="flex items-center space-x-2">
              <School className="h-5 w-5 text-blue-600" />
              <span>Schools Overview</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {data?.schools.map((school, index) => (
                <div
                  key={school.id}
                  className="group relative overflow-hidden rounded-lg border border-gray-200 bg-white p-5 transition-all hover:border-blue-300 hover:shadow-lg"
                >
                  <div className="absolute right-0 top-0 h-full w-2 bg-gradient-to-b from-blue-500 to-purple-600 opacity-0 transition-opacity group-hover:opacity-100"></div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-lg">
                        <span className="text-lg font-bold">{index + 1}</span>
                      </div>
                      <div>
                        <p className="text-lg font-semibold text-gray-900">
                          {school.school_name}
                        </p>
                        <p className="text-sm text-gray-500">
                          Code: <span className="font-medium">{school.school_code}</span>
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-3xl font-bold text-blue-600">
                        {school.students_count || 0}
                      </p>
                      <p className="text-sm text-gray-500">Students</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* User Breakdown */}
        <Card className="shadow-soft">
          <CardHeader className="border-b bg-gradient-to-r from-purple-50 to-pink-50">
            <CardTitle className="flex items-center space-x-2">
              <GraduationCap className="h-5 w-5 text-purple-600" />
              <span>Users by Role</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div className="rounded-lg border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-blue-100 p-6 text-center transition-all hover:border-blue-300 hover:shadow-lg">
                <div className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 shadow-lg">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <p className="text-4xl font-bold text-blue-900">
                  {data?.users_by_role.admins || 0}
                </p>
                <p className="mt-2 text-sm font-medium text-blue-700">Administrators</p>
              </div>
              <div className="rounded-lg border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-purple-100 p-6 text-center transition-all hover:border-purple-300 hover:shadow-lg">
                <div className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full bg-purple-600 shadow-lg">
                  <School className="h-8 w-8 text-white" />
                </div>
                <p className="text-4xl font-bold text-purple-900">
                  {data?.users_by_role.school_admins || 0}
                </p>
                <p className="mt-2 text-sm font-medium text-purple-700">School Admins</p>
              </div>
              <div className="rounded-lg border-2 border-green-200 bg-gradient-to-br from-green-50 to-green-100 p-6 text-center transition-all hover:border-green-300 hover:shadow-lg">
                <div className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full bg-green-600 shadow-lg">
                  <GraduationCap className="h-8 w-8 text-white" />
                </div>
                <p className="text-4xl font-bold text-green-900">
                  {data?.users_by_role.mentors || 0}
                </p>
                <p className="mt-2 text-sm font-medium text-green-700">Mentors</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
