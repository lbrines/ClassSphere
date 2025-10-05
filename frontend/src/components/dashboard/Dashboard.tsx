'use client'

import { useAuth } from '@/providers/AuthProvider'
import { UserRole } from '@/types/auth'
import { AdminDashboard } from './AdminDashboard'
import { CoordinatorDashboard } from './CoordinatorDashboard'
import { TeacherDashboard } from './TeacherDashboard'
import { StudentDashboard } from './StudentDashboard'
import { DashboardLayout } from './DashboardLayout'

export function Dashboard() {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Please log in to access the dashboard.</p>
        </div>
      </div>
    )
  }

  const renderDashboard = () => {
    switch (user.role) {
      case UserRole.ADMIN:
        return <AdminDashboard />
      case UserRole.COORDINATOR:
        return <CoordinatorDashboard />
      case UserRole.TEACHER:
        return <TeacherDashboard />
      case UserRole.STUDENT:
        return <StudentDashboard />
      default:
        return (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Unknown user role: {user.role}</p>
          </div>
        )
    }
  }

  return (
    <DashboardLayout>
      {renderDashboard()}
    </DashboardLayout>
  )
}