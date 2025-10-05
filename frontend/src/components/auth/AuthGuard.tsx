'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/providers/AuthProvider'
import { UserRole } from '@/types/auth'

interface AuthGuardProps {
  children: React.ReactNode
  requiredRole?: UserRole
  fallback?: React.ReactNode
}

export function AuthGuard({ children, requiredRole, fallback }: AuthGuardProps) {
  const { user, isAuthenticated, isLoading } = useAuth()
  const router = useRouter()
  const [hasMounted, setHasMounted] = useState(false)

  useEffect(() => {
    setHasMounted(true)
  }, [])

  useEffect(() => {
    if (hasMounted && !isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [hasMounted, isAuthenticated, isLoading, router])

  // Durante SSR o antes del mount, mostrar loading para evitar hidration mismatch
  if (!hasMounted || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  // Not authenticated
  if (!isAuthenticated || !user) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Redirecting to login...</p>
        </div>
      </div>
    )
  }

  // Check role permissions if required
  if (requiredRole) {
    const roleHierarchy = {
      [UserRole.STUDENT]: 1,
      [UserRole.TEACHER]: 2,
      [UserRole.COORDINATOR]: 3,
      [UserRole.ADMIN]: 4,
    }

    const userLevel = roleHierarchy[user.role]
    const requiredLevel = roleHierarchy[requiredRole]

    if (userLevel < requiredLevel) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-destructive">Access Denied</h1>
            <p className="mt-2 text-muted-foreground">
              You don't have permission to access this resource.
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              Required role: {requiredRole} or higher
            </p>
          </div>
        </div>
      )
    }
  }

  return <>{children}</>
}