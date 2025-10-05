export enum UserRole {
  ADMIN = 'admin',
  COORDINATOR = 'coordinator',
  TEACHER = 'teacher',
  STUDENT = 'student'
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
  google_id?: string
  avatar_url?: string
  created_at: string
  last_login?: string
}

export interface Token {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface AuthResponse {
  user: User
  token: Token
}

export interface LoginRequest {
  email: string
  password: string
}

export interface GoogleOAuthRequest {
  authorization_code: string
  code_verifier: string
}

export interface GoogleAuthUrlResponse {
  authorization_url: string
  code_verifier: string
  state: string
}