import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function MyStudentsPage() {
  return (
    <DashboardLayout title="My Students">
      <Card>
        <CardHeader>
          <CardTitle>My Assigned Students</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Student list coming soon...</p>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
