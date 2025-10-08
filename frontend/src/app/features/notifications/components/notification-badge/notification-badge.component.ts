import { Component, EventEmitter, inject, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-notification-badge',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div
      class="notification-badge relative inline-block cursor-pointer"
      role="button"
      tabindex="0"
      [attr.aria-label]="'Notifications: ' + (unreadCount$ | async) + ' unread'"
      (click)="onClick()"
      (keydown.enter)="onClick()"
    >
      <svg class="w-6 h-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      
      <span
        *ngIf="(unreadCount$ | async)! > 0"
        class="badge-count absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-600 rounded-full"
      >
        {{ (unreadCount$ | async)! > 9 ? '9+' : (unreadCount$ | async) }}
      </span>
    </div>
  `,
})
export class NotificationBadgeComponent {
  private readonly notificationService = inject(NotificationService);

  readonly unreadCount$ = this.notificationService.unreadCount$;

  @Output() badgeClicked = new EventEmitter<void>();

  onClick(): void {
    this.badgeClicked.emit();
  }
}

