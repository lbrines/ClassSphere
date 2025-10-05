'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/providers/AuthProvider'
import { LoginForm } from '@/components/auth/LoginForm'
import { GoogleOAuthButton } from '@/components/auth/GoogleOAuthButton'

export default function LoginPage() {
  const { isAuthenticated } = useAuth()
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)

  // Redirect if already authenticated - usando useEffect para evitar setState durante render
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/')
    }
  }, [isAuthenticated, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md p-8 space-y-6 bg-card rounded-lg shadow-lg border">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-foreground">ClassSphere</h1>
          <p className="mt-2 text-muted-foreground">Sign in to your account</p>
        </div>

        {error && (
          <div className="p-4 text-sm text-destructive-foreground bg-destructive/10 border border-destructive/20 rounded-md">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <LoginForm onError={setError} />

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or continue with</span>
            </div>
          </div>

          <GoogleOAuthButton onError={setError} />
        </div>

        <div className="text-center text-sm text-muted-foreground">
          <p>Demo accounts for testing:</p>
          <div className="mt-2 space-y-1 text-xs">
            <p><strong>Admin:</strong> admin@classsphere.com / admin123</p>
            <p><strong>Coordinator:</strong> coordinator@classsphere.com / coord123</p>
            <p><strong>Teacher:</strong> teacher@classsphere.com / teacher123</p>
            <p><strong>Student:</strong> student@classsphere.com / student123</p>
          </div>
        </div>
      </div>
    </div>
  )
}