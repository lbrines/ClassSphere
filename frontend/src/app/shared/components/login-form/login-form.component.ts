import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form (ngSubmit)="onSubmit()" [formGroup]="form" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium" for="email">Email</label>
        <input
          id="email"
          type="email"
          formControlName="email"
          autocomplete="email"
          class="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-slate-100 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
        />
        <p *ngIf="form.controls.email.invalid && form.controls.email.touched" class="text-sm text-red-400">
          Please enter a valid email address.
        </p>
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium" for="password">Password</label>
        <input
          id="password"
          type="password"
          autocomplete="current-password"
          formControlName="password"
          class="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-slate-100 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
        />
        <p *ngIf="form.controls.password.invalid && form.controls.password.touched" class="text-sm text-red-400">
          Password must be at least 6 characters.
        </p>
      </div>

      <button
        type="submit"
        class="w-full rounded-md bg-sky-500 px-4 py-2 font-semibold text-white shadow hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
        [disabled]="form.invalid || pending"
      >
        {{ pending ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
  `,
})
export class LoginFormComponent {
  private readonly fb = inject(FormBuilder);

  @Input() pending = false;
  @Output() readonly submitted = new EventEmitter<{ email: string; password: string }>();

  readonly form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  onSubmit(): void {
    if (this.form.invalid || this.pending) {
      this.form.markAllAsTouched();
      return;
    }
    this.submitted.emit(this.form.getRawValue());
  }
}
