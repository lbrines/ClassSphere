import { Component } from '@angular/core';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  template: `
    <section class="space-y-4">
      <h2 class="text-2xl font-semibold">Administrator Overview</h2>
      <p class="text-slate-400">Monitor organization-wide metrics and user activity.</p>
    </section>
  `,
})
export class AdminDashboardComponent {}
