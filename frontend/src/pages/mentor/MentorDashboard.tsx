import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function MentorDashboard() {
  return (
    <DashboardLayout title="Mentor Dashboard">
      <Card>
        <CardHeader>
          <CardTitle>Welcome, Mentor</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Mentor dashboard coming soon...
          </p>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
