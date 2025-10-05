import { useQuery } from '@tanstack/react-query'
import { dashboardAPI } from '@/lib/api'

export function CoordinatorDashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['coordinator-dashboard'],
    queryFn: dashboardAPI.getCoordinatorDashboard,
  })

  if (isLoading) return <div className="text-center py-8">Loading coordinator dashboard...</div>
  if (error) return <div className="text-center py-8 text-destructive">Error: {error.message}</div>

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Coordinator Dashboard</h2>
      {data && (
        <div className="bg-card rounded-lg border p-6">
          <h3 className="text-lg font-semibold mb-4">{data.message}</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Assigned Teachers</h4>
              <p className="text-2xl font-bold">{data.stats?.assigned_teachers || 0}</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Managed Courses</h4>
              <p className="text-2xl font-bold">{data.stats?.managed_courses || 0}</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Pending Approvals</h4>
              <p className="text-2xl font-bold">{data.stats?.pending_approvals || 0}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}