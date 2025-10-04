/**
 * Dashboard Educativo - Types
 * Context-Aware Implementation - Day 5-7 High Priority
 */

export interface ContextAwareComponentProps {
  contextId: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  children?: React.ReactNode;
}

export interface User {
  user_id: string;
  username: string;
  email: string;
  name?: string;
  picture?: string;
  role: 'admin' | 'coordinator' | 'teacher' | 'student';
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface GoogleOAuthData {
  authorization_url: string;
  state: string;
  scopes: string[];
}

export interface GoogleTokens {
  access_token: string;
  refresh_token?: string;
  expires_in: number;
}

export interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
  context_id?: string;
}

export interface ContextLog {
  timestamp: string;
  context_id: string;
  token_count: number;
  context_priority: string;
  status: string;
  memory_management: {
    chunk_position: string;
    lost_in_middle_risk: string;
  };
  phase?: string;
  task?: string;
  message?: string;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  app_name: string;
  app_version: string;
  context_management: {
    context_log_path: string;
    context_health: {
      status: string;
      healthy: boolean;
      coherence_score?: string;
      total_entries?: number;
    };
  };
  server: {
    host: string;
    port: number;
  };
}