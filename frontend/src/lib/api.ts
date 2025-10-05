import axios from 'axios'
import Cookies from 'js-cookie'
import type {
  AuthResponse,
  LoginRequest,
  GoogleOAuthRequest,
  GoogleAuthUrlResponse,
  User
} from '@/types/auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = Cookies.get('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh or redirect to login on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Clear tokens and redirect to login
      Cookies.remove('access_token')
      Cookies.remove('refresh_token')
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', credentials)
    return response.data
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout')
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me')
    return response.data
  },

  getGoogleAuthUrl: async (): Promise<GoogleAuthUrlResponse> => {
    const response = await api.get<GoogleAuthUrlResponse>('/oauth/google/url')
    return response.data
  },

  googleCallback: async (request: GoogleOAuthRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/oauth/google/callback', request)
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<{ access_token: string }> => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  }
}

export const dashboardAPI = {
  getAdminDashboard: async () => {
    const response = await api.get('/admin/dashboard')
    return response.data
  },

  getCoordinatorDashboard: async () => {
    const response = await api.get('/coordinator/dashboard')
    return response.data
  },

  getTeacherDashboard: async () => {
    const response = await api.get('/teacher/dashboard')
    return response.data
  },

  getStudentDashboard: async () => {
    const response = await api.get('/student/dashboard')
    return response.data
  }
}

export default api