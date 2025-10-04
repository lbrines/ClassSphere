/**
 * Dashboard Educativo - API Utility
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { logComponentContext } from './context-logger';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8003',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens
api.interceptors.request.use(
  (config) => {
    // Log API request
    logComponentContext(
      `api-request-${Date.now()}`,
      'MEDIUM',
      'started',
      `API Request: ${config.method?.toUpperCase()} ${config.url}`,
      'frontend',
      'api_request'
    );

    // Add auth token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    logComponentContext(
      `api-request-error-${Date.now()}`,
      'HIGH',
      'failed',
      `API Request Error: ${error.message}`,
      'frontend',
      'api_request_error'
    );
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log successful API response
    logComponentContext(
      `api-response-${Date.now()}`,
      'MEDIUM',
      'completed',
      `API Response: ${response.status} ${response.config.url}`,
      'frontend',
      'api_response'
    );

    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Log API response error
    logComponentContext(
      `api-response-error-${Date.now()}`,
      'HIGH',
      'failed',
      `API Response Error: ${error.response?.status} ${error.config?.url}`,
      'frontend',
      'api_response_error'
    );

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
          logComponentContext(
            'api-token-refresh-001',
            'HIGH',
            'started',
            'Attempting token refresh due to 401 error',
            'frontend',
            'token_refresh'
          );

          const response = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8003'}/api/v1/auth/refresh`,
            { refresh_token: refreshToken }
          );

          if (response.data.access_token) {
            const newToken = response.data.access_token;
            localStorage.setItem('access_token', newToken);
            
            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            
            logComponentContext(
              'api-token-refresh-001',
              'HIGH',
              'completed',
              'Token refreshed successfully, retrying request',
              'frontend',
              'token_refresh'
            );

            return api(originalRequest);
          }
        }
      } catch (refreshError) {
        logComponentContext(
          'api-token-refresh-001',
          'HIGH',
          'failed',
          `Token refresh failed: ${refreshError}`,
          'frontend',
          'token_refresh'
        );

        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Redirect to login page
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export { api };