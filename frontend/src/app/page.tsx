import { AuthGuard } from '@/components/auth/AuthGuard'
import { Dashboard } from '@/components/dashboard/Dashboard'

export default function HomePage() {
  return (
    <AuthGuard>
      <Dashboard />
    </AuthGuard>
  )
}