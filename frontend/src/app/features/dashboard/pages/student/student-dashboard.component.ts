import { Component } from '@angular/core';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  template: `
    <section class="space-y-4">
      <h2 class="text-2xl font-semibold">Student Dashboard</h2>
      <p class="text-slate-400">Review assignments, grades, and classroom announcements.</p>
    </section>
  `,
})
export class StudentDashboardComponent {}
