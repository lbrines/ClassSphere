/**
 * Dashboard Educativo - Login Form Component
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ContextAwareComponent } from './ContextAwareComponent';
import { useAuth } from '@/hooks/useAuth';
import { logComponentContext } from '@/utils/context-logger';

// Validation schema
const loginSchema = z.object({
  username: z.string().min(1, 'Username is required'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginForm: React.FC = () => {
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const { login, loginWithGoogle, isLoading } = useAuth();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      logComponentContext('login-form-submit-001', 'CRITICAL', 'started', 'Login form submitted', 'frontend', 'login_form_submit');
      
      await login(data);
      
      logComponentContext('login-form-submit-001', 'CRITICAL', 'completed', 'Login form submitted successfully', 'frontend', 'login_form_submit');
    } catch (error: any) {
      logComponentContext('login-form-submit-001', 'CRITICAL', 'failed', `Login form submission failed: ${error.message}`, 'frontend', 'login_form_submit');
      
      setError('root', {
        type: 'manual',
        message: error.message || 'Login failed. Please try again.'
      });
    }
  };

  const handleGoogleLogin = async () => {
    try {
      setIsGoogleLoading(true);
      logComponentContext('google-login-button-002', 'CRITICAL', 'started', 'Google login button clicked', 'frontend', 'google_login_button');
      
      await loginWithGoogle();
      
      logComponentContext('google-login-button-002', 'CRITICAL', 'completed', 'Google login initiated', 'frontend', 'google_login_button');
    } catch (error: any) {
      logComponentContext('google-login-button-002', 'CRITICAL', 'failed', `Google login failed: ${error.message}`, 'frontend', 'google_login_button');
      
      setError('root', {
        type: 'manual',
        message: 'Google login failed. Please try again.'
      });
    } finally {
      setIsGoogleLoading(false);
    }
  };

  return (
    <ContextAwareComponent contextId="login-form-001" priority="CRITICAL">
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Dashboard Educativo
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Inicia sesión en tu cuenta
            </p>
          </div>
          
          <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="username" className="sr-only">
                  Username
                </label>
                <input
                  {...register('username')}
                  type="text"
                  autoComplete="username"
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Username"
                />
                {errors.username && (
                  <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
                )}
              </div>
              
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  {...register('password')}
                  type="password"
                  autoComplete="current-password"
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                />
                {errors.password && (
                  <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
                )}
              </div>
            </div>

            {errors.root && (
              <div className="rounded-md bg-red-50 p-4">
                <p className="text-sm text-red-800">{errors.root.message}</p>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Iniciando sesión...' : 'Iniciar sesión'}
              </button>
            </div>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-gray-50 text-gray-500">O continúa con</span>
                </div>
              </div>

              <div className="mt-6">
                <button
                  type="button"
                  onClick={handleGoogleLogin}
                  disabled={isGoogleLoading || isLoading}
                  className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGoogleLoading ? 'Conectando con Google...' : 'Google'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </ContextAwareComponent>
  );
};