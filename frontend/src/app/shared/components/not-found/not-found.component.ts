import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="flex min-h-screen flex-col items-center justify-center bg-slate-950 text-center text-slate-100">
      <h2 class="text-4xl font-bold">404</h2>
      <p class="mt-2 text-slate-400">We could not find the page you were looking for.</p>
      <a routerLink="/auth/login" class="mt-6 rounded-md bg-sky-500 px-4 py-2 font-semibold text-white hover:bg-sky-600">Return to login</a>
    </section>
  `,
})
export class NotFoundComponent {}
