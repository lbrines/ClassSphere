import { User } from './user.model';

export interface AuthResponse {
  accessToken: string;
  expiresAt: string;
  user: User;
}

export interface OAuthInitResponse {
  state: string;
  url: string;
}

export interface Credentials {
  email: string;
  password: string;
}
