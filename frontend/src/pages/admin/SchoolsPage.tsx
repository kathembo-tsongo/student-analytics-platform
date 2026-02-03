import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function SchoolsPage() {
  return (
    <DashboardLayout title="Schools">
      <Card>
        <CardHeader>
          <CardTitle>Schools Management</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Schools management page coming soon...</p>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
