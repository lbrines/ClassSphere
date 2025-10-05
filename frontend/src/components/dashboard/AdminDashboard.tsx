'use client'

import { useQuery } from '@tanstack/react-query'
import { dashboardAPI } from '@/lib/api'

export function AdminDashboard() {
  const { data: dashboardData, isLoading, error } = useQuery({
    queryKey: ['admin-dashboard'],
    queryFn: dashboardAPI.getAdminDashboard,
  })

  if (isLoading) {
    return <div className="text-center py-8">Loading admin dashboard...</div>
  }

  if (error) {
    return (
      <div className="text-center py-8 text-destructive">
        Error loading dashboard: {error.message}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-foreground">Admin Dashboard</h2>
        <p className="text-muted-foreground">Manage users, courses, and system settings</p>
      </div>

      {dashboardData && (
        <div className="bg-card rounded-lg border p-6">
          <h3 className="text-lg font-semibold mb-4">{dashboardData.message}</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Total Users</h4>
              <p className="text-2xl font-bold">{dashboardData.stats?.total_users || 0}</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Active Courses</h4>
              <p className="text-2xl font-bold">{dashboardData.stats?.active_courses || 0}</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-medium">Pending Requests</h4>
              <p className="text-2xl font-bold">{dashboardData.stats?.pending_requests || 0}</p>
            </div>
          </div>

          <div>
            <h4 className="font-medium mb-2">Admin Permissions:</h4>
            <div className="flex flex-wrap gap-2">
              {dashboardData.permissions?.map((permission: string) => (
                <span
                  key={permission}
                  className="px-2 py-1 text-xs bg-primary text-primary-foreground rounded"
                >
                  {permission}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}