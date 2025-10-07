import { Component } from '@angular/core';

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  template: `
    <section class="space-y-4">
      <h2 class="text-2xl font-semibold">Teacher Workspace</h2>
      <p class="text-slate-400">Track classroom progress and upcoming sessions.</p>
    </section>
  `,
})
export class TeacherDashboardComponent {}
