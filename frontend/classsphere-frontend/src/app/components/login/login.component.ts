import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService, LoginRequest } from '../../services/auth.service';

interface DemoUser {
  name: string;
  email: string;
  password: string;
  role: string;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            ClassSphere
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Sign in to your account
          </p>
        </div>
        
        <!-- Google OAuth Button -->
        <div class="mt-6">
          <button
            type="button"
            (click)="loginWithGoogle()"
            [disabled]="isLoading()"
            class="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            @if (isLoading()) {
              <span>Signing in...</span>
            } @else {
              <span>Sign in with Google</span>
            }
          </button>
        </div>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">Or continue with email</span>
          </div>
        </div>

        <!-- Email/Password Form -->
        <form class="mt-6 space-y-6" [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
              <input
                id="email"
                type="email"
                formControlName="email"
                autocomplete="email"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Enter your email"
                [class.border-red-300]="loginForm.get('email')?.invalid && loginForm.get('email')?.touched"
              />
              @if (loginForm.get('email')?.invalid && loginForm.get('email')?.touched) {
                <p class="mt-1 text-sm text-red-600">
                  @if (loginForm.get('email')?.errors?.['required']) {
                    Email is required
                  } @else if (loginForm.get('email')?.errors?.['email']) {
                    Please enter a valid email address
                  }
                </p>
              }
            </div>
            
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input
                id="password"
                type="password"
                formControlName="password"
                autocomplete="current-password"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Enter your password"
                [class.border-red-300]="loginForm.get('password')?.invalid && loginForm.get('password')?.touched"
              />
              @if (loginForm.get('password')?.invalid && loginForm.get('password')?.touched) {
                <p class="mt-1 text-sm text-red-600">
                  @if (loginForm.get('password')?.errors?.['required']) {
                    Password is required
                  }
                </p>
              }
            </div>
          </div>

          @if (errorMessage()) {
            <div class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-700">
                {{ errorMessage() }}
              </div>
            </div>
          }

          <div>
            <button
              type="submit"
              [disabled]="isLoading() || loginForm.invalid"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              @if (isLoading()) {
                <span>Signing in...</span>
              } @else {
                <span>Sign in</span>
              }
            </button>
          </div>

          <div class="text-center">
            <p class="text-sm text-gray-600">
              Don't have an account?
              <a routerLink="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
                Sign up here
              </a>
            </p>
          </div>
        </form>

        <!-- Demo Users Section -->
        <div class="mt-8 border-t border-gray-200 pt-6">
          <div class="text-center">
            <button
              type="button"
              (click)="showDemoUsers.set(!showDemoUsers())"
              class="text-sm font-medium text-indigo-600 hover:text-indigo-500 mb-4 flex items-center justify-center mx-auto"
            >
              <svg class="w-4 h-4 mr-1" [class.rotate-180]="showDemoUsers()" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
              Demo Users (Testing Only)
            </button>
            
            @if (showDemoUsers()) {
              <div class="grid grid-cols-1 gap-3 mb-4">
                @for (user of demoUsers; track user.email) {
                  <button
                    type="button"
                    (click)="fillDemoUser(user)"
                    class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-indigo-50 hover:border-indigo-300 transition-colors"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
                        <span class="text-sm font-medium text-indigo-600">{{ user.name.charAt(0) }}</span>
                      </div>
                      <div class="text-left">
                        <p class="text-sm font-medium text-gray-900">{{ user.name }}</p>
                        <p class="text-xs text-gray-500">{{ user.role }}</p>
                      </div>
                    </div>
                    <div class="text-right">
                      <p class="text-xs text-gray-500">{{ user.email }}</p>
                      <p class="text-xs text-indigo-500 font-medium">Click to fill</p>
                    </div>
                  </button>
                }
              </div>
              <p class="text-xs text-gray-400">
                These are demo accounts for testing purposes only
              </p>
            }
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class LoginComponent {
  loginForm: FormGroup;
  isLoading = signal(false);
  errorMessage = signal('');
  showDemoUsers = signal(false);

  demoUsers: DemoUser[] = [
    {
      name: 'Admin User',
      email: 'admin@classsphere.com',
      password: 'admin123',
      role: 'Administrator'
    },
    {
      name: 'Teacher Demo',
      email: 'teacher@classsphere.com',
      password: 'teacher123',
      role: 'Teacher'
    },
    {
      name: 'Student Demo',
      email: 'student@classsphere.com',
      password: 'student123',
      role: 'Student'
    },
    {
      name: 'Parent Demo',
      email: 'parent@classsphere.com',
      password: 'parent123',
      role: 'Parent'
    }
  ];

  constructor(
    private authService: AuthService,
    private router: Router,
    private fb: FormBuilder
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set('');

    const loginData: LoginRequest = {
      email: this.loginForm.get('email')?.value,
      password: this.loginForm.get('password')?.value
    };

    this.authService.login(loginData).subscribe({
      next: (response) => {
        this.isLoading.set(false);
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        this.isLoading.set(false);
        this.errorMessage.set(error.error?.error || 'Error signing in');
      }
    });
  }

  loginWithGoogle(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    // For now, redirect to Google OAuth URL
    // In a real implementation, this would use Google's OAuth library
    const googleAuthUrl = 'http://localhost:8080/auth/google';
    window.location.href = googleAuthUrl;
  }

  fillDemoUser(user: DemoUser): void {
    this.loginForm.patchValue({
      email: user.email,
      password: user.password
    });
    this.errorMessage.set('');
    
    // Show a brief success message
    console.log(`Demo user filled: ${user.name} (${user.role})`);
    
    // Optional: Add visual feedback by marking the form as touched
    this.loginForm.markAsTouched();
  }
}
