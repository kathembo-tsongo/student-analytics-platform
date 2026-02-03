import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function SchoolAdminDashboard() {
  return (
    <DashboardLayout title="School Admin Dashboard">
      <Card>
        <CardHeader>
          <CardTitle>Welcome, School Administrator</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            School dashboard coming soon...
          </p>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
