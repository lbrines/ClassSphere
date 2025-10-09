import { Injectable } from '@angular/core';

/**
 * Global window interface extension for runtime environment configuration.
 * 
 * The _env object is injected at runtime by Docker using envsubst,
 * allowing the same Docker image to work in multiple environments:
 * - Mock: http://localhost:8080/api/v1
 * - Test: http://backend:8080/api/v1
 * - Development: http://localhost:8080/api/v1
 * - Production: https://api.classsphere.example/api/v1
 * 
 * This follows the 12-Factor App methodology (Config via environment).
 */
declare global {
  interface Window {
    _env?: {
      API_URL?: string;
    };
  }
}

/**
 * EnvironmentService provides runtime configuration for the Angular application.
 * 
 * This service reads configuration from window._env, which is injected at
 * container startup time via a script (generate-env.sh) that runs before
 * the Angular app loads. This allows a single Docker image to be deployed
 * to multiple environments without rebuilding.
 * 
 * **TDD Implementation:**
 * - Tests: environment.service.spec.ts
 * - Coverage: All branches tested
 * - Integration: Used by AuthService, ClassroomService, NotificationService
 * 
 * **Usage:**
 * ```typescript
 * constructor(private env: EnvironmentService) {}
 * 
 * makeApiCall() {
 *   const url = `${this.env.apiUrl}/endpoint`;
 *   // ...
 * }
 * ```
 * 
 * **Environment Detection:**
 * - Development: URL contains 'localhost'
 * - Test: URL contains 'test' or 'backend'
 * - Mock: URL contains 'mock'
 * - Production: Everything else (typically https)
 * 
 * @Injectable providedIn: 'root'
 */
@Injectable({
  providedIn: 'root'
})
export class EnvironmentService {
  /**
   * Default API URL used when window._env is not available.
   * This provides a sensible fallback for local development.
   */
  private readonly DEFAULT_API_URL = 'http://localhost:8080/api/v1';

  /**
   * Gets the API URL from runtime configuration or default.
   * 
   * Priority:
   * 1. window._env.API_URL (if set and not empty)
   * 2. DEFAULT_API_URL fallback
   * 
   * This is a getter so it's reactive to changes in window._env,
   * which can be useful during testing.
   */
  get apiUrl(): string {
    return window._env?.API_URL || this.DEFAULT_API_URL;
  }

  /**
   * Detects the current environment based on the API URL.
   * 
   * Detection rules:
   * - 'development': URL contains 'localhost'
   * - 'test': URL contains 'test' or 'backend' (container names)
   * - 'mock': URL contains 'mock'
   * - 'production': All other cases
   * 
   * @returns The detected environment type
   */
  get environment(): 'mock' | 'test' | 'development' | 'production' {
    const url = this.apiUrl.toLowerCase();
    
    if (url.includes('localhost')) {
      return 'development';
    }
    
    if (url.includes('test') || url.includes('backend')) {
      return 'test';
    }
    
    if (url.includes('mock')) {
      return 'mock';
    }
    
    return 'production';
  }

  /**
   * Checks if the app is running in production mode.
   * Useful for conditional logic (e.g., enabling analytics only in production).
   * 
   * @returns true if in production, false otherwise
   */
  get isProduction(): boolean {
    return this.environment === 'production';
  }

  /**
   * Checks if the app is running in development mode.
   * Useful for development-specific features (e.g., debug logging).
   * 
   * @returns true if in development, false otherwise
   */
  get isDevelopment(): boolean {
    return this.environment === 'development';
  }

  /**
   * Checks if the app is running in test mode.
   * Useful for test-specific behavior.
   * 
   * @returns true if in test mode, false otherwise
   */
  get isTest(): boolean {
    return this.environment === 'test';
  }

  /**
   * Checks if the app is running in mock mode.
   * Useful for mock-specific behavior.
   * 
   * @returns true if in mock mode, false otherwise
   */
  get isMock(): boolean {
    return this.environment === 'mock';
  }
}

