import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function StudentsPage() {
  return (
    <DashboardLayout title="Students">
      <Card>
        <CardHeader>
          <CardTitle>Students List</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Students list coming soon...</p>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
