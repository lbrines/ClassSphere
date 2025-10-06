import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-auth-callback',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
      <div class="max-w-md w-full space-y-8 text-center">
        <div>
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
            ClassSphere
          </h2>
          <p class="mt-2 text-sm text-gray-600">
            {{ statusMessage }}
          </p>
        </div>
        
        @if (isLoading) {
          <div class="flex justify-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          </div>
        }
        
        @if (errorMessage) {
          <div class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">
              {{ errorMessage }}
            </div>
            <div class="mt-4">
              <button
                (click)="goToLogin()"
                class="text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Return to Login
              </button>
            </div>
          </div>
        }
      </div>
    </div>
  `,
  styles: []
})
export class AuthCallbackComponent implements OnInit {
  isLoading = true;
  statusMessage = 'Completing authentication...';
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const token = params['token'];
      const error = params['error'];

      if (error) {
        this.handleError(error);
      } else if (token) {
        this.handleSuccess(token);
      } else {
        this.handleError('No authentication token received');
      }
    });
  }

  private handleSuccess(token: string): void {
    try {
      // Store the token
      localStorage.setItem('token', token);
      
      // Update auth service state
      this.authService.isAuthenticated.set(true);
      
      // Get user profile
      this.authService.getProfile().subscribe({
        next: (user) => {
          this.authService.currentUser.set(user);
          this.statusMessage = 'Authentication successful! Redirecting...';
          
          // Redirect to dashboard after a short delay
          setTimeout(() => {
            this.router.navigate(['/dashboard']);
          }, 1500);
        },
        error: (error) => {
          console.error('Failed to get user profile:', error);
          this.handleError('Failed to load user profile');
        }
      });
    } catch (error) {
      console.error('Error processing authentication:', error);
      this.handleError('Failed to process authentication');
    }
  }

  private handleError(error: string): void {
    this.isLoading = false;
    this.errorMessage = error;
    this.statusMessage = 'Authentication failed';
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }
}
