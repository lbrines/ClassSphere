import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService, RegisterRequest } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            ClassSphere
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Crea tu cuenta
          </p>
        </div>
        <form class="mt-8 space-y-6" (ngSubmit)="onSubmit()" #registerForm="ngForm">
          <div class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Nombre completo</label>
              <input
                id="name"
                name="name"
                type="text"
                autocomplete="name"
                required
                [(ngModel)]="registerData.name"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Tu nombre completo"
              />
            </div>
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                [(ngModel)]="registerData.email"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="tu@email.com"
              />
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                [(ngModel)]="registerData.password"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Mínimo 8 caracteres"
              />
              <p class="mt-1 text-xs text-gray-500">
                La contraseña debe tener al menos 8 caracteres y contener letras y números.
              </p>
            </div>
          </div>

          @if (errorMessage()) {
            <div class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-700">
                {{ errorMessage() }}
              </div>
            </div>
          }

          @if (successMessage()) {
            <div class="rounded-md bg-green-50 p-4">
              <div class="text-sm text-green-700">
                {{ successMessage() }}
              </div>
            </div>
          }

          <div>
            <button
              type="submit"
              [disabled]="isLoading()"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              @if (isLoading()) {
                <span>Creando cuenta...</span>
              } @else {
                <span>Crear cuenta</span>
              }
            </button>
          </div>

          <div class="text-center">
            <p class="text-sm text-gray-600">
              ¿Ya tienes una cuenta?
              <a routerLink="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
                Inicia sesión aquí
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  `,
  styles: []
})
export class RegisterComponent {
  registerData: RegisterRequest = {
    name: '',
    email: '',
    password: ''
  };

  isLoading = signal(false);
  errorMessage = signal('');
  successMessage = signal('');

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    if (!this.registerData.name || !this.registerData.email || !this.registerData.password) {
      this.errorMessage.set('Por favor, completa todos los campos');
      return;
    }

    if (this.registerData.password.length < 8) {
      this.errorMessage.set('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    this.authService.register(this.registerData).subscribe({
      next: (response) => {
        this.isLoading.set(false);
        this.successMessage.set('¡Cuenta creada exitosamente! Redirigiendo...');
        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 1500);
      },
      error: (error) => {
        this.isLoading.set(false);
        this.errorMessage.set(error.error?.error || 'Error al crear la cuenta');
      }
    });
  }
}
