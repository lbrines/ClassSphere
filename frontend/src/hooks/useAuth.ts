"use client";

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { contextLogger } from '@/utils/context-logger';
import api from '@/utils/api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface User {
  user_id: string;
  username: string;
  email: string;
  role: string;
}

interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export function useAuth() {
  const queryClient = useQueryClient();
  const router = useRouter();

  // Get current user
  const { data: user, isLoading } = useQuery({
    queryKey: ['user'],
    queryFn: async (): Promise<User | null> => {
      const token = localStorage.getItem('access_token');
      if (!token) return null;

      try {
        const response = await api.get('/auth/me');
        return response.data;
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return null;
      }
    },
    retry: false,
  });

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: async (credentials: LoginCredentials): Promise<AuthTokens> => {
      const response = await api.post('/auth/login', credentials);
      const tokens = response.data;
      
      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);
      
      return tokens;
    },
    onSuccess: (tokens) => {
      // User data will be fetched separately
      router.push('/dashboard');
    },
    onError: (error) => {
      contextLogger.logContextStatus(
        'auth-login-error',
        'HIGH',
        'error',
        'middle',
        'Login failed: ' + (error as Error).message,
        'frontend',
        'login_error'
      );
    },
  });

  // Google login mutation
  const googleLoginMutation = useMutation({
    mutationFn: async (): Promise<void> => {
      const response = await api.get('/auth/google/authorize');
      window.location.href = response.data.authorization_url;
    },
    onError: (error) => {
      contextLogger.logContextStatus(
        'google-login-error',
        'HIGH',
        'error',
        'middle',
        'Google login failed: ' + (error as Error).message,
        'frontend',
        'google_login_error'
      );
    },
  });

  // Logout function
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    queryClient.clear();
    router.push('/login');
    
    contextLogger.logContextStatus(
      'auth-logout',
      'HIGH',
      'completed',
      'middle',
      'User logged out',
      'frontend',
      'logout'
    );
  };

  return {
    user,
    isLoading,
    login: loginMutation.mutate,
    loginWithGoogle: googleLoginMutation.mutate,
    logout,
    isLoginLoading: loginMutation.isLoading,
    isGoogleLoginLoading: googleLoginMutation.isLoading,
  };
}