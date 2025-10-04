/**
 * Dashboard Educativo - useAuth Hook
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { User, AuthTokens, LoginCredentials, GoogleOAuthData } from '@/types';
import { api } from '@/utils/api';
import { logComponentContext } from '@/utils/context-logger';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const queryClient = useQueryClient();

  // Log auth hook initialization
  useEffect(() => {
    logComponentContext('auth-hook-001', 'CRITICAL', 'started', 'Auth hook initialized', 'frontend', 'useAuth_init');
  }, []);

  // Check if user is authenticated
  const isAuthenticated = !!user && !!tokens;

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      logComponentContext('auth-login-002', 'CRITICAL', 'started', 'Login attempt initiated', 'frontend', 'login');
      
      const response = await api.post('/auth/login', credentials);
      
      if (response.data) {
        const { access_token, refresh_token, token_type, expires_in, user: userData } = response.data;
        
        setTokens({ access_token, refresh_token, token_type, expires_in });
        setUser(userData);
        
        // Store tokens in localStorage
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        
        logComponentContext('auth-login-002', 'CRITICAL', 'completed', 'Login successful', 'frontend', 'login');
        
        return response.data;
      }
      
      throw new Error('Login failed');
    },
    onError: (error) => {
      logComponentContext('auth-login-002', 'CRITICAL', 'failed', `Login failed: ${error}`, 'frontend', 'login');
    }
  });

  // Google OAuth login mutation
  const googleLoginMutation = useMutation({
    mutationFn: async () => {
      logComponentContext('auth-google-login-003', 'CRITICAL', 'started', 'Google OAuth login initiated', 'frontend', 'google_login');
      
      const response = await api.get('/auth/google/authorize');
      
      if (response.data) {
        const { authorization_url } = response.data;
        
        // Redirect to Google OAuth
        window.location.href = authorization_url;
        
        logComponentContext('auth-google-login-003', 'CRITICAL', 'completed', 'Redirected to Google OAuth', 'frontend', 'google_login');
        
        return response.data;
      }
      
      throw new Error('Google OAuth failed');
    },
    onError: (error) => {
      logComponentContext('auth-google-login-003', 'CRITICAL', 'failed', `Google OAuth failed: ${error}`, 'frontend', 'google_login');
    }
  });

  // Refresh token mutation
  const refreshTokenMutation = useMutation({
    mutationFn: async () => {
      logComponentContext('auth-refresh-004', 'HIGH', 'started', 'Token refresh initiated', 'frontend', 'refresh_token');
      
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await api.post('/auth/refresh', { refresh_token: refreshToken });
      
      if (response.data) {
        const { access_token, expires_in } = response.data;
        
        setTokens(prev => prev ? { ...prev, access_token, expires_in } : null);
        localStorage.setItem('access_token', access_token);
        
        logComponentContext('auth-refresh-004', 'HIGH', 'completed', 'Token refreshed successfully', 'frontend', 'refresh_token');
        
        return response.data;
      }
      
      throw new Error('Token refresh failed');
    },
    onError: (error) => {
      logComponentContext('auth-refresh-004', 'HIGH', 'failed', `Token refresh failed: ${error}`, 'frontend', 'refresh_token');
      
      // If refresh fails, logout user
      logout();
    }
  });

  // Logout function
  const logout = useCallback(() => {
    logComponentContext('auth-logout-005', 'HIGH', 'started', 'Logout initiated', 'frontend', 'logout');
    
    setUser(null);
    setTokens(null);
    
    // Clear tokens from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Clear all queries
    queryClient.clear();
    
    logComponentContext('auth-logout-005', 'HIGH', 'completed', 'Logout completed', 'frontend', 'logout');
  }, [queryClient]);

  // Check authentication status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      const accessToken = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (accessToken && refreshToken) {
        try {
          logComponentContext('auth-check-006', 'MEDIUM', 'started', 'Checking auth status', 'frontend', 'check_auth');
          
          const response = await api.get('/auth/me', {
            headers: { Authorization: `Bearer ${accessToken}` }
          });
          
          if (response.data) {
            setUser(response.data);
            setTokens({
              access_token: accessToken,
              refresh_token: refreshToken,
              token_type: 'bearer',
              expires_in: 1800
            });
            
            logComponentContext('auth-check-006', 'MEDIUM', 'completed', 'Auth status verified', 'frontend', 'check_auth');
          }
        } catch (error) {
          logComponentContext('auth-check-006', 'MEDIUM', 'failed', `Auth check failed: ${error}`, 'frontend', 'check_auth');
          
          // Try to refresh token
          try {
            await refreshTokenMutation.mutateAsync();
          } catch (refreshError) {
            // If refresh also fails, logout
            logout();
          }
        }
      }
    };
    
    checkAuthStatus();
  }, [refreshTokenMutation, logout]);

  return {
    user,
    tokens,
    isLoading: loginMutation.isLoading || googleLoginMutation.isLoading || refreshTokenMutation.isLoading,
    isAuthenticated,
    login: loginMutation.mutateAsync,
    loginWithGoogle: googleLoginMutation.mutateAsync,
    logout,
    refreshToken: refreshTokenMutation.mutateAsync
  };
};