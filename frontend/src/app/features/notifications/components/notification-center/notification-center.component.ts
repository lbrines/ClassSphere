import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NotificationService } from '../../../../core/services/notification.service';
import { AppNotification, NotificationType } from '../../../../core/models/notification.model';

@Component({
  selector: 'app-notification-center',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="notification-center max-w-md mx-auto bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <div class="p-4 border-b border-gray-200 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <h2 class="text-lg font-semibold text-gray-900">Notifications</h2>
          <span
            class="connection-status inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
            [ngClass]="(connectionStatus$ | async) ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
          >
            <span class="w-2 h-2 rounded-full mr-1"
                  [ngClass]="(connectionStatus$ | async) ? 'bg-green-500' : 'bg-red-500 disconnected-indicator'">
            </span>
            {{ (connectionStatus$ | async) ? 'Connected' : 'Offline' }}
          </span>
        </div>
        <button
          *ngIf="(unreadCount$ | async)! > 0"
          (click)="onMarkAllAsRead()"
          class="mark-all-read-button text-sm text-blue-600 hover:text-blue-800"
        >
          Mark all as read
        </button>
      </div>

      <!-- Filters -->
      <div class="p-3 border-b border-gray-200 flex gap-2">
        <button
          *ngFor="let type of notificationTypes"
          (click)="filterByType(type)"
          class="filter-button px-3 py-1 text-sm rounded-full"
          [ngClass]="selectedType === type ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          {{ type | titlecase }}
        </button>
        <button
          (click)="toggleUnreadFilter()"
          class="filter-button px-3 py-1 text-sm rounded-full"
          [ngClass]="showOnlyUnread ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          Unread
        </button>
      </div>

      <!-- Notifications List -->
      <div
        role="list"
        aria-label="Notifications list"
        aria-live="polite"
        class="max-h-96 overflow-y-auto"
      >
        <div
          *ngFor="let notification of filteredNotifications"
          role="listitem"
          tabindex="0"
          (click)="onNotificationClick(notification)"
          (keydown.enter)="onNotificationClick(notification)"
          class="notification-item p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
          [ngClass]="{ 'unread bg-blue-50': !notification.read }"
        >
          <div class="flex items-start gap-3">
            <!-- Icon -->
            <div class="notification-icon flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center"
                 [ngClass]="getIconClass(notification.type)">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <p class="notification-title text-sm font-medium text-gray-900">
                  {{ notification.title }}
                </p>
                <button
                  (click)="onDelete($event, notification.id)"
                  class="delete-button flex-shrink-0 text-gray-400 hover:text-red-600"
                  aria-label="Delete notification"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
              <p class="notification-message text-sm text-gray-600 mt-1">
                {{ notification.message }}
              </p>
              <p class="notification-timestamp text-xs text-gray-500 mt-1">
                {{ formatTimestamp(notification.timestamp) }}
              </p>
            </div>

            <!-- Unread Indicator -->
            <div *ngIf="!notification.read" class="unread-indicator flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div *ngIf="filteredNotifications.length === 0" class="empty-state p-8 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <p class="mt-2 text-sm text-gray-600">No notifications</p>
        </div>
      </div>

      <!-- Footer -->
      <div *ngIf="(notifications$ | async)!.length > 0" class="p-3 border-t border-gray-200 text-center">
        <button
          (click)="onClearAll()"
          class="clear-all-button text-sm text-red-600 hover:text-red-800"
        >
          Clear all notifications
        </button>
      </div>
    </div>
  `,
})
export class NotificationCenterComponent implements OnInit {
  private readonly notificationService = inject(NotificationService);

  readonly notifications$ = this.notificationService.notifications$;
  readonly unreadCount$ = this.notificationService.unreadCount$;
  readonly connectionStatus$ = this.notificationService.connectionStatus$;

  notificationTypes: NotificationType[] = ['info', 'success', 'warning', 'error'];
  filteredNotifications: AppNotification[] = [];
  selectedType: NotificationType | 'all' = 'all';
  showOnlyUnread = false;

  ngOnInit(): void {
    this.notifications$.subscribe((notifications) => {
      this.applyFilters(notifications);
    });
  }

  onNotificationClick(notification: AppNotification): void {
    if (!notification.read) {
      this.notificationService.markAsRead(notification.id);
    }
  }

  onMarkAllAsRead(): void {
    this.notificationService.markAllAsRead();
  }

  onDelete(event: Event, notificationId: string): void {
    event.stopPropagation();
    this.notificationService.deleteNotification(notificationId);
  }

  onClearAll(): void {
    this.notificationService.clearAll();
  }

  filterByType(type: NotificationType | 'all'): void {
    this.selectedType = type;
    this.applyFilters(this.notificationService['notificationsSubject'].value);
  }

  toggleUnreadFilter(): void {
    this.showOnlyUnread = !this.showOnlyUnread;
    this.applyFilters(this.notificationService['notificationsSubject'].value);
  }

  getIconClass(type: NotificationType): string {
    const classes = {
      info: 'bg-blue-100 text-blue-600',
      success: 'bg-green-100 text-green-600',
      warning: 'bg-yellow-100 text-yellow-600',
      error: 'bg-red-100 text-red-600',
    };
    return classes[type];
  }

  formatTimestamp(timestamp: string): string {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins === 1) return '1m ago';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 120) return '1h ago';
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    if (diffMins < 2880) return '1d ago';
    return `${Math.floor(diffMins / 1440)}d ago`;
  }

  private applyFilters(notifications: AppNotification[]): void {
    let filtered = notifications;

    if (this.selectedType !== 'all') {
      filtered = filtered.filter((n) => n.type === this.selectedType);
    }

    if (this.showOnlyUnread) {
      filtered = filtered.filter((n) => !n.read);
    }

    this.filteredNotifications = filtered;
  }

  /**
   * Get filter count text
   */
  getFilterCountText(): string {
    return `${this.filteredNotifications.length} of ${this.notificationService['notificationsSubject'].value.length}`;
  }
}

