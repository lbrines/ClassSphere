/**
 * Dashboard Educativo - Login Page
 * Context-Aware Implementation - Day 5-7 High Priority
 */

'use client';

import React from 'react';
import { LoginForm } from '@/components/LoginForm';
import { AuthGuard } from '@/components/AuthGuard';

export default function LoginPage() {
  return (
    <AuthGuard requireAuth={false}>
      <LoginForm />
    </AuthGuard>
  );
}