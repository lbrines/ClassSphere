import { inject, Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable, Subject, takeUntil } from 'rxjs';

import { SSEWithAuthService } from './sse-with-auth.service';
import { AppNotification, NotificationState, WebSocketMessage } from '../models/notification.model';
import { environment } from '../../../environments/environment';

/**
 * NotificationService - Phase 3 Real-time Notifications
 * 
 * Features:
 * - Real-time notification reception via Server-Sent Events (SSE)
 * - Notification state management
 * - Read/unread tracking
 * - Desktop notifications for high priority
 * - Sound alerts
 * - Filtering and search
 * 
 * Updated to use SSE with Authorization header support for secure authentication.
 */
@Injectable({ providedIn: 'root' })
export class NotificationService implements OnDestroy {
  private readonly sseService = inject(SSEWithAuthService);
  private readonly destroy$ = new Subject<void>();

  private readonly notificationsSubject = new BehaviorSubject<AppNotification[]>([]);
  private readonly unreadCountSubject = new BehaviorSubject<number>(0);
  private readonly connectionStatusSubject = new BehaviorSubject<boolean>(false);

  readonly notifications$ = this.notificationsSubject.asObservable();
  readonly unreadCount$ = this.unreadCountSubject.asObservable();
  readonly connectionStatus$ = this.connectionStatusSubject.asObservable();

  /**
   * Initialize notification service and SSE connection
   * @param token JWT token for authentication (required)
   */
  async initialize(token: string): Promise<void> {
    if (!token) {
      console.error('SSE requires authentication token');
      return;
    }

    // Use SSE endpoint for notifications
    const sseUrl = environment.apiUrl + '/notifications/stream';
    
    // Connect with Authorization header
    await this.sseService.connect(sseUrl, token);

    // Subscribe to SSE messages
    this.sseService.messages$
      .pipe(takeUntil(this.destroy$))
      .subscribe((message: WebSocketMessage) => {
        this.handleSSEMessage(message);
      });

    // Subscribe to connection status
    this.sseService.connectionStatus$
      .pipe(takeUntil(this.destroy$))
      .subscribe((connected) => {
        this.connectionStatusSubject.next(connected);
      });
  }

  /**
   * Mark notification as read
   */
  markAsRead(notificationId: string): void {
    const notifications = this.notificationsSubject.value;
    const notification = notifications.find((n) => n.id === notificationId);

    if (notification && !notification.read) {
      notification.read = true;
      this.notificationsSubject.next([...notifications]);
      this.updateUnreadCount();
    }
  }

  /**
   * Mark all notifications as read
   */
  markAllAsRead(): void {
    const notifications = this.notificationsSubject.value.map((n) => ({
      ...n,
      read: true,
    }));

    this.notificationsSubject.next(notifications);
    this.unreadCountSubject.next(0);
  }

  /**
   * Delete notification
   */
  deleteNotification(notificationId: string): void {
    const notifications = this.notificationsSubject.value.filter(
      (n) => n.id !== notificationId
    );

    this.notificationsSubject.next(notifications);
    this.updateUnreadCount();
  }

  /**
   * Clear all notifications
   */
  clearAll(): void {
    this.notificationsSubject.next([]);
    this.unreadCountSubject.next(0);
  }

  /**
   * Get notifications by type
   */
  getNotificationsByType(type: string): AppNotification[] {
    return this.notificationsSubject.value.filter((n) => n.type === type);
  }

  /**
   * Get unread notifications
   */
  getUnreadNotifications(): AppNotification[] {
    return this.notificationsSubject.value.filter((n) => !n.read);
  }

  /**
   * Get notifications count
   */
  getNotificationsCount(): number {
    return this.notificationsSubject.value.length;
  }

  /**
   * Check if has unread notifications
   */
  hasUnread(): boolean {
    return this.unreadCountSubject.value > 0;
  }

  /**
   * Request desktop notification permission
   */
  async requestDesktopPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      console.warn('Desktop notifications not supported');
      return 'denied';
    }

    return await Notification.requestPermission();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.sseService.disconnect();
  }

  /**
   * Handle incoming SSE messages
   */
  private handleSSEMessage(message: WebSocketMessage): void {
    if (message.type === 'notification' && message.data) {
      this.addNotification(message.data);
    } else if (message.type === 'connected') {
      console.log('SSE connection established:', message.data);
    }
  }

  /**
   * Add new notification to the list
   */
  private addNotification(notification: AppNotification): void {
    const notifications = this.notificationsSubject.value;

    // Avoid duplicates
    if (notifications.some((n) => n.id === notification.id)) {
      return;
    }

    // Add and sort by timestamp (newest first)
    const updated = [notification, ...notifications].sort((a, b) => {
      return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    });

    this.notificationsSubject.next(updated);
    this.updateUnreadCount();

    // Handle high priority notifications
    if (notification.priority === 'high' || notification.priority === 'urgent') {
      this.playNotificationSound();

      if (notification.priority === 'urgent') {
        this.showDesktopNotification(notification);
      }
    }
  }

  /**
   * Update unread count
   */
  private updateUnreadCount(): void {
    const unreadCount = this.notificationsSubject.value.filter((n) => !n.read).length;
    this.unreadCountSubject.next(unreadCount);
  }

  /**
   * Play notification sound
   */
  private playNotificationSound(): void {
    if (typeof Audio === 'undefined') {
      console.warn('Audio API not available');
      return;
    }
    
    try {
      const audio = new Audio('/assets/sounds/notification.mp3');
      audio.volume = 0.5;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch((error) => {
          console.warn('Failed to play notification sound:', error);
        });
      }
    } catch (error) {
      console.warn('Notification sound not available:', error);
    }
  }

  /**
   * Show desktop notification (Browser API)
   */
  private showDesktopNotification(notification: AppNotification): void {
    if (Notification.permission === 'granted') {
      try {
        const desktopNotif = new Notification(notification.title, {
          body: notification.message,
          icon: '/assets/icons/notification-icon.png',
          tag: notification.id,
          requireInteraction: notification.priority === 'urgent',
        });

        desktopNotif.onclick = () => {
          window.focus();
          desktopNotif.close();
          this.markAsRead(notification.id);
        };
      } catch (error) {
        console.warn('Failed to show desktop notification:', error);
      }
    }
  }
}

