'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/providers/AuthProvider'
import type { LoginRequest } from '@/types/auth'

interface LoginFormProps {
  onError: (error: string | null) => void
}

export function LoginForm({ onError }: LoginFormProps) {
  const [formData, setFormData] = useState<LoginRequest>({
    email: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.email || !formData.password) {
      onError('Please fill in all fields')
      return
    }

    setIsLoading(true)
    onError(null)

    try {
      await login(formData)
      router.push('/')
    } catch (error: any) {
      const message = error.response?.data?.detail || error.message || 'Login failed'
      onError(message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    onError(null)
  }

  const fillDemoCredentials = (role: string) => {
    const credentials = {
      admin: { email: 'admin@classsphere.com', password: 'admin123' },
      coordinator: { email: 'coordinator@classsphere.com', password: 'coord123' },
      teacher: { email: 'teacher@classsphere.com', password: 'teacher123' },
      student: { email: 'student@classsphere.com', password: 'student123' }
    }

    const creds = credentials[role as keyof typeof credentials]
    if (creds) {
      setFormData(creds)
      onError(null)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-foreground mb-1">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          value={formData.email}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-input bg-background text-foreground rounded-md focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
          placeholder="Enter your email"
          disabled={isLoading}
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-foreground mb-1">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          value={formData.password}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-input bg-background text-foreground rounded-md focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
          placeholder="Enter your password"
          disabled={isLoading}
        />
      </div>

      {/* Quick demo buttons */}
      <div className="flex flex-wrap gap-1 justify-center">
        {(['admin', 'coordinator', 'teacher', 'student'] as const).map((role) => (
          <button
            key={role}
            type="button"
            onClick={() => fillDemoCredentials(role)}
            className="px-2 py-1 text-xs bg-secondary text-secondary-foreground rounded hover:bg-secondary/80 transition-colors"
            disabled={isLoading}
          >
            {role}
          </button>
        ))}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  )
}