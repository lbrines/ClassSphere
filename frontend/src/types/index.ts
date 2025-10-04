/**
 * TypeScript Types for Dashboard Educativo
 * Context-Aware Implementation
 */

export interface ContextAwareComponentProps {
  children: React.ReactNode;
  contextId?: string;
  componentName?: string;
}

export interface User {
  user_id: string;
  username: string;
  email: string;
  role: string;
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
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => void;
  loginWithGoogle: () => void;
  logout: () => void;
  isLoginLoading: boolean;
  isGoogleLoginLoading: boolean;
}

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status: string;
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
  dependencies?: string[];
  next_action?: string;
  coherence_check: {
    context_continuity: boolean;
    priority_consistency: boolean;
  };
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  app_name: string;
  version: string;
  context_management: {
    context_log_path: string;
    context_health: {
      healthy: boolean;
      last_log: string | null;
    };
  };
}