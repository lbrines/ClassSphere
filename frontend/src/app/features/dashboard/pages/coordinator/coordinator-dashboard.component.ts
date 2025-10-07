import { Component } from '@angular/core';

@Component({
  selector: 'app-coordinator-dashboard',
  standalone: true,
  template: `
    <section class="space-y-4">
      <h2 class="text-2xl font-semibold">Coordinator Console</h2>
      <p class="text-slate-400">Manage course allocations and educator support workflows.</p>
    </section>
  `,
})
export class CoordinatorDashboardComponent {}
