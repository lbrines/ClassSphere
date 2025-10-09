import { TestBed } from '@angular/core/testing';
import { EnvironmentService } from './environment.service';

describe('EnvironmentService - TDD Implementation', () => {
  let service: EnvironmentService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [EnvironmentService]
    });
    service = TestBed.inject(EnvironmentService);
    
    // Clean up window._env before each test
    delete (window as any)._env;
  });

  describe('RED Phase - Runtime Configuration', () => {
    it('should be created', () => {
      expect(service).toBeTruthy();
    });

    it('should load API URL from window._env when available', () => {
      // Setup: Mock window._env
      (window as any)._env = {
        API_URL: 'http://test-backend:8080/api/v1'
      };

      // Execute & Assert
      expect(service.apiUrl).toBe('http://test-backend:8080/api/v1');
    });

    it('should fallback to default API URL when window._env is not set', () => {
      // Setup: No window._env
      delete (window as any)._env;

      // Execute & Assert
      expect(service.apiUrl).toBe('http://localhost:8080/api/v1');
    });

    it('should fallback to default when window._env.API_URL is empty', () => {
      // Setup: Empty API_URL
      (window as any)._env = {
        API_URL: ''
      };

      // Execute & Assert
      expect(service.apiUrl).toBe('http://localhost:8080/api/v1');
    });

    it('should detect development environment from localhost URL', () => {
      // Setup
      (window as any)._env = {
        API_URL: 'http://localhost:8080/api/v1'
      };

      // Execute & Assert
      expect(service.environment).toBe('development');
    });

    it('should detect test environment from test URL', () => {
      // Setup
      (window as any)._env = {
        API_URL: 'http://test-backend:8080/api/v1'
      };

      // Execute & Assert
      expect(service.environment).toBe('test');
    });

    it('should detect mock environment from mock URL', () => {
      // Setup
      (window as any)._env = {
        API_URL: 'http://mock-api:8080/api/v1'
      };

      // Execute & Assert
      expect(service.environment).toBe('mock');
    });

    it('should detect production environment from production URL', () => {
      // Setup
      (window as any)._env = {
        API_URL: 'https://api.classsphere.example/api/v1'
      };

      // Execute & Assert
      expect(service.environment).toBe('production');
    });

    it('should handle window._env with undefined API_URL', () => {
      // Setup
      (window as any)._env = {};

      // Execute & Assert
      expect(service.apiUrl).toBe('http://localhost:8080/api/v1');
    });

    it('should be reactive to changes in window._env', () => {
      // Setup: Initial state
      (window as any)._env = {
        API_URL: 'http://localhost:8080/api/v1'
      };

      const firstUrl = service.apiUrl;
      expect(firstUrl).toBe('http://localhost:8080/api/v1');

      // Change window._env
      (window as any)._env = {
        API_URL: 'https://production.example.com/api/v1'
      };

      // Should reflect new value
      const secondUrl = service.apiUrl;
      expect(secondUrl).toBe('https://production.example.com/api/v1');
    });

    it('should handle special characters in API URL', () => {
      // Setup
      (window as any)._env = {
        API_URL: 'http://localhost:8080/api/v1?key=value&test=true'
      };

      // Execute & Assert
      expect(service.apiUrl).toContain('key=value');
    });

    it('should provide boolean flag for production mode', () => {
      // Test development
      (window as any)._env = { API_URL: 'http://localhost:8080/api/v1' };
      expect(service.isProduction).toBe(false);

      // Test production
      (window as any)._env = { API_URL: 'https://api.classsphere.example/api/v1' };
      expect(service.isProduction).toBe(true);
    });

    it('should provide boolean flag for development mode', () => {
      // Test development
      (window as any)._env = { API_URL: 'http://localhost:8080/api/v1' };
      expect(service.isDevelopment).toBe(true);

      // Test production
      (window as any)._env = { API_URL: 'https://api.classsphere.example/api/v1' };
      expect(service.isDevelopment).toBe(false);
    });
  });

  describe('Integration with Multiple Environments', () => {
    it('should work in mock mode (localhost:8080)', () => {
      (window as any)._env = { API_URL: 'http://localhost:8080/api/v1' };
      
      expect(service.apiUrl).toBe('http://localhost:8080/api/v1');
      expect(service.environment).toBe('development');
      expect(service.isDevelopment).toBe(true);
    });

    it('should work in test mode (backend container)', () => {
      (window as any)._env = { API_URL: 'http://backend:8080/api/v1' };
      
      expect(service.apiUrl).toBe('http://backend:8080/api/v1');
      expect(service.environment).toBe('test');
    });

    it('should work in production mode', () => {
      (window as any)._env = { API_URL: 'https://api.classsphere.example/api/v1' };
      
      expect(service.apiUrl).toBe('https://api.classsphere.example/api/v1');
      expect(service.environment).toBe('production');
      expect(service.isProduction).toBe(true);
    });
  });

  describe('Type Safety', () => {
    it('should have correct return types', () => {
      (window as any)._env = { API_URL: 'http://localhost:8080/api/v1' };

      // Type checks (TypeScript compilation ensures these)
      const url: string = service.apiUrl;
      const env: 'mock' | 'test' | 'development' | 'production' = service.environment;
      const isProd: boolean = service.isProduction;
      const isDev: boolean = service.isDevelopment;

      expect(typeof url).toBe('string');
      expect(['mock', 'test', 'development', 'production']).toContain(env);
      expect(typeof isProd).toBe('boolean');
      expect(typeof isDev).toBe('boolean');
    });
  });
});

