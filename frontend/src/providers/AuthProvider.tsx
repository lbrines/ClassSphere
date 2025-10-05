'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { authAPI } from '@/lib/api'
import type { User, LoginRequest, AuthResponse } from '@/types/auth'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  getGoogleAuthUrl: () => Promise<string>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const queryClient = useQueryClient()

  // Check if user is authenticated
  const {
    data: userData,
    isLoading,
    error
  } = useQuery({
    queryKey: ['user'],
    queryFn: authAPI.getCurrentUser,
    enabled: !!Cookies.get('access_token'),
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: authAPI.login,
    onSuccess: (data: AuthResponse) => {
      setUser(data.user)
      Cookies.set('access_token', data.token.access_token, { expires: 1 })
      Cookies.set('refresh_token', data.token.refresh_token, { expires: 7 })
      queryClient.setQueryData(['user'], data.user)
    },
    onError: (error) => {
      console.error('Login failed:', error)
      throw error
    }
  })

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: authAPI.logout,
    onSuccess: () => {
      setUser(null)
      Cookies.remove('access_token')
      Cookies.remove('refresh_token')
      queryClient.clear()
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
  })

  useEffect(() => {
    if (userData) {
      setUser(userData)
    } else if (error) {
      setUser(null)
      Cookies.remove('access_token')
      Cookies.remove('refresh_token')
    }
  }, [userData, error])

  const login = async (credentials: LoginRequest) => {
    await loginMutation.mutateAsync(credentials)
  }

  const logout = async () => {
    await logoutMutation.mutateAsync()
  }

  const checkAuth = async () => {
    if (Cookies.get('access_token')) {
      queryClient.invalidateQueries({ queryKey: ['user'] })
    }
  }

  const getGoogleAuthUrl = async (): Promise<string> => {
    const response = await authAPI.getGoogleAuthUrl()
    // Store code_verifier for later use in callback
    sessionStorage.setItem('google_code_verifier', response.code_verifier)
    sessionStorage.setItem('google_state', response.state)
    return response.authorization_url
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading: isLoading || loginMutation.isPending || logoutMutation.isPending,
    login,
    logout,
    checkAuth,
    getGoogleAuthUrl
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}