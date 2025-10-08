import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-oauth-button',
  standalone: true,
  template: `
    <button
      type="button"
      (click)="clicked.emit()"
      class="flex w-full items-center justify-center gap-2 rounded-md bg-sky-500 px-4 py-2 font-semibold text-white shadow hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
      [disabled]="disabled"
      aria-label="Sign in with Google"
    >
      <span class="font-semibold">G</span>
      <span>{{ label }}</span>
    </button>
  `,
})
export class OAuthButtonComponent {
  @Input() label = 'Continue with Google';
  @Input() disabled = false;

  @Output() readonly clicked = new EventEmitter<void>();
}
