import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertTriangle, TrendingDown, Clock, Users } from 'lucide-react'
import axios from 'axios'

interface RiskPrediction {
  student_id: number
  overall_risk_score: number
  overall_risk_level: string
  priority: number
  all_risk_factors: string[]
  intervention_urgency: string
  recommended_actions: string[]
  dropout_risk: {
    risk_probability: number
    risk_level: string
    risk_factors: string[]
  }
  course_failure_risk: {
    failure_probability: number
    risk_level: string
  }
  program_delay_risk: {
    delay_probability: number
    estimated_delay_semesters: number
    risk_level: string
  }
}

interface DashboardStats {
  total_students: number
  critical_risk: number
  high_risk: number
  medium_risk: number
  low_risk: number
  avg_risk_score: number
  students_needing_intervention: number
}

export default function AtRiskStudentsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [students, setStudents] = useState<RiskPrediction[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('ALL')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // Get dashboard stats
      const statsRes = await axios.get('http://localhost:5000/api/stats/dashboard')
      setStats(statsRes.data)
      
      // Get all at-risk students (we'll fetch from all schools)
      const schoolIds = [1, 2, 3, 4, 5]
      const allStudents: RiskPrediction[] = []
      
      for (const schoolId of schoolIds) {
        try {
            const res = await axios.get(`http://localhost:5000/api/predict/school/${schoolId}`)
          allStudents.push(...res.data.students)
        } catch (err) {
            console.error(`Error fetching school ${schoolId}:`, err)
        }
      }
      
      // Sort by risk score
      allStudents.sort((a, b) => b.overall_risk_score - a.overall_risk_score)
      setStudents(allStudents)
      
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border-orange-300'
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      default:
        return 'bg-green-100 text-green-800 border-green-300'
    }
  }

  const filteredStudents = students.filter(student => {
    if (filter === 'ALL') return true
    return student.overall_risk_level === filter
  })

  if (loading) {
    return (
      <DashboardLayout title="At-Risk Students Analytics">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto"></div>
            <p className="mt-4 text-gray-600">Analyzing student data...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout title="At-Risk Students Analytics">
      <div className="space-y-6">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card className="border-red-200 bg-red-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-red-600">
                Critical Risk
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-900">
                {stats?.critical_risk || 0}
              </div>
              <p className="text-xs text-red-600 mt-1">Immediate action required</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 bg-orange-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-orange-600">
                High Risk
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-900">
                {stats?.high_risk || 0}
              </div>
              <p className="text-xs text-orange-600 mt-1">Close monitoring needed</p>
            </CardContent>
          </Card>

          <Card className="border-yellow-200 bg-yellow-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-yellow-600">
                Medium Risk
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-yellow-900">
                {stats?.medium_risk || 0}
              </div>
              <p className="text-xs text-yellow-600 mt-1">Regular monitoring</p>
            </CardContent>
          </Card>

          <Card className="border-blue-200 bg-blue-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-blue-600">
                Avg Risk Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-900">
                {stats?.avg_risk_score || 0}
              </div>
              <p className="text-xs text-blue-600 mt-1">Out of 100</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>At-Risk Students ({filteredStudents.length})</CardTitle>
              <div className="flex space-x-2">
                {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((level) => (
                  <button
                    key={level}
                    onClick={() => setFilter(level)}
                    className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                      filter === level
                        ? 'bg-primary text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {filteredStudents.map((student) => (
                <div
                  key={student.student_id}
                  className="rounded-lg border-2 p-4 transition-all hover:shadow-lg"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 text-white font-bold">
                          {student.priority}
                        </div>
                        <div>
                          <h3 className="font-semibold text-lg">
                            Student ID: {student.student_id}
                          </h3>
                          <div className="flex items-center space-x-2 mt-1">
                            <Badge className={getRiskColor(student.overall_risk_level)}>
                              {student.overall_risk_level} RISK
                            </Badge>
                            <span className="text-sm text-gray-600">
                              Risk Score: {student.overall_risk_score}/100
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Risk Breakdown */}
                      <div className="mt-4 grid grid-cols-3 gap-4">
                        <div className="rounded-lg bg-red-50 p-3">
                          <div className="flex items-center space-x-2">
                            <AlertTriangle className="h-4 w-4 text-red-600" />
                            <span className="text-xs font-medium text-red-600">
                              Dropout Risk
                            </span>
                          </div>
                          <p className="mt-1 text-lg font-bold text-red-900">
                            {(student.dropout_risk.risk_probability * 100).toFixed(1)}%
                          </p>
                        </div>

                        <div className="rounded-lg bg-orange-50 p-3">
                          <div className="flex items-center space-x-2">
                            <TrendingDown className="h-4 w-4 text-orange-600" />
                            <span className="text-xs font-medium text-orange-600">
                              Course Failure
                            </span>
                          </div>
                          <p className="mt-1 text-lg font-bold text-orange-900">
                            {(student.course_failure_risk.failure_probability * 100).toFixed(1)}%
                          </p>
                        </div>

                        <div className="rounded-lg bg-yellow-50 p-3">
                          <div className="flex items-center space-x-2">
                            <Clock className="h-4 w-4 text-yellow-600" />
                            <span className="text-xs font-medium text-yellow-600">
                              Program Delay
                            </span>
                          </div>
                          <p className="mt-1 text-lg font-bold text-yellow-900">
                            {student.program_delay_risk.estimated_delay_semesters} sem
                          </p>
                        </div>
                      </div>

                      {/* Risk Factors */}
                      {student.all_risk_factors.length > 0 && (
                        <div className="mt-4">
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            Risk Factors:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {student.all_risk_factors.map((factor, idx) => (
                              <span
                                key={idx}
                                className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700"
                              >
                                {factor}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Recommendations */}
                      {student.recommended_actions.length > 0 && (
                        <div className="mt-4 rounded-lg bg-blue-50 p-3">
                          <p className="text-sm font-medium text-blue-900 mb-2">
                            📋 Recommended Actions:
                          </p>
                          <ul className="space-y-1">
                            {student.recommended_actions.map((action, idx) => (
                              <li key={idx} className="text-sm text-blue-800">
                                • {action}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
