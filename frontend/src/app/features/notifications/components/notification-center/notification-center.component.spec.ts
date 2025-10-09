import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BehaviorSubject } from 'rxjs';

import { NotificationCenterComponent } from './notification-center.component';
import { NotificationService } from '../../../../core/services/notification.service';
import { AppNotification } from '../../../../core/models/notification.model';

describe('NotificationCenterComponent', () => {
  let component: NotificationCenterComponent;
  let fixture: ComponentFixture<NotificationCenterComponent>;
  let notificationService: jasmine.SpyObj<NotificationService>;
  let notificationsSubject: BehaviorSubject<AppNotification[]>;
  let unreadCountSubject: BehaviorSubject<number>;
  let connectionStatusSubject: BehaviorSubject<boolean>;

  const mockNotifications: AppNotification[] = [
    {
      id: '1',
      type: 'info',
      priority: 'medium',
      title: 'New Assignment',
      message: 'You have a new assignment in Mathematics',
      timestamp: '2025-10-07T12:00:00Z',
      read: false,
    },
    {
      id: '2',
      type: 'success',
      priority: 'low',
      title: 'Grade Posted',
      message: 'Your grade for Quiz 1 has been posted',
      timestamp: '2025-10-07T11:00:00Z',
      read: true,
    },
  ];

  beforeEach(async () => {
    notificationsSubject = new BehaviorSubject<AppNotification[]>(
      mockNotifications.map((notification) => ({ ...notification }))
    );
    unreadCountSubject = new BehaviorSubject<number>(1);
    connectionStatusSubject = new BehaviorSubject<boolean>(true);

    const notificationServiceSpy = jasmine.createSpyObj(
      'NotificationService',
      ['markAsRead', 'markAllAsRead', 'deleteNotification', 'clearAll'],
      {
        notifications$: notificationsSubject.asObservable(),
        unreadCount$: unreadCountSubject.asObservable(),
        connectionStatus$: connectionStatusSubject.asObservable(),
      }
    );
    (notificationServiceSpy as any).notificationsSubject = notificationsSubject;

    await TestBed.configureTestingModule({
      imports: [NotificationCenterComponent],
      providers: [{ provide: NotificationService, useValue: notificationServiceSpy }],
    }).compileComponents();

    fixture = TestBed.createComponent(NotificationCenterComponent);
    component = fixture.componentInstance;
    notificationService = TestBed.inject(
      NotificationService
    ) as jasmine.SpyObj<NotificationService>;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Display', () => {
    it('should display all notifications', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const notificationItems = compiled.querySelectorAll('.notification-item');

      expect(notificationItems.length).toBe(2);
    });

    it('should display notification title and message', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const firstNotification = compiled.querySelector('.notification-item');

      expect(firstNotification?.textContent).toContain('New Assignment');
      expect(firstNotification?.textContent).toContain(
        'You have a new assignment in Mathematics'
      );
    });

    it('should display notification timestamp', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const timestamp = compiled.querySelector('.notification-timestamp');

      expect(timestamp).toBeTruthy();
    });

    it('should show unread indicator for unread notifications', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const unreadIndicators = compiled.querySelectorAll('.unread-indicator');

      expect(unreadIndicators.length).toBe(1);
    });

    it('should display empty state when no notifications', () => {
      notificationsSubject.next([]);
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const emptyState = compiled.querySelector('.empty-state');

      expect(emptyState).toBeTruthy();
      expect(emptyState?.textContent).toContain('No notifications');
    });

    it('should show connection status indicator', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const connectionStatus = compiled.querySelector('.connection-status');

      expect(connectionStatus).toBeTruthy();
    });

    it('should show disconnected status when offline', () => {
      connectionStatusSubject.next(false);
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const disconnectedIndicator = compiled.querySelector('.disconnected-indicator');

      expect(disconnectedIndicator).toBeTruthy();
    });
  });

  describe('Interactions', () => {
    it('should mark notification as read when clicked', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const firstNotification = compiled.querySelector('.notification-item') as HTMLElement;

      firstNotification.click();

      expect(notificationService.markAsRead).toHaveBeenCalledWith('1');
    });

    it('should call markAllAsRead when "Mark all as read" button clicked', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const markAllButton = compiled.querySelector(
        '.mark-all-read-button'
      ) as HTMLButtonElement;

      markAllButton?.click();

      expect(notificationService.markAllAsRead).toHaveBeenCalled();
    });

    it('should delete notification when delete button clicked', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const deleteButton = compiled.querySelector('.delete-button') as HTMLButtonElement;

      deleteButton?.click();

      expect(notificationService.deleteNotification).toHaveBeenCalled();
    });

    it('should clear all notifications when "Clear all" button clicked', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const clearAllButton = compiled.querySelector(
        '.clear-all-button'
      ) as HTMLButtonElement;

      clearAllButton?.click();

      expect(notificationService.clearAll).toHaveBeenCalled();
    });
  });

  describe('Filtering', () => {
    it('should filter by notification type', () => {
      fixture.detectChanges();
      component.filterByType('info');
      fixture.detectChanges();

      expect(component.filteredNotifications.length).toBeLessThan(
        mockNotifications.length
      );
    });

    it('should show only unread notifications when filter applied', () => {
      fixture.detectChanges();
      component.toggleUnreadFilter();

      expect(
        component.filteredNotifications.every((n) => !n.read)
      ).toBe(true);
    });

    it('should display filter buttons', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const filterButtons = compiled.querySelectorAll('.filter-button');

      expect(filterButtons.length).toBeGreaterThan(0);
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const notificationList = compiled.querySelector('[role="list"]');

      expect(notificationList).toBeTruthy();
    });

    it('should have keyboard navigation support', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const firstNotification = compiled.querySelector('.notification-item');

      expect(firstNotification?.getAttribute('tabindex')).toBe('0');
    });

    it('should announce new notifications to screen readers', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const liveRegion = compiled.querySelector('[aria-live="polite"]');

      expect(liveRegion).toBeTruthy();
    });
  });

  describe('Styling', () => {
    it('should apply correct style for notification type', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const notifications = compiled.querySelectorAll('.notification-item');

      notifications.forEach((notif) => {
        expect(notif.classList.length).toBeGreaterThan(0);
      });
    });

    it('should highlight unread notifications', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const unreadNotification = compiled.querySelector(
        '.notification-item.unread'
      ) as HTMLElement;

      expect(unreadNotification).toBeTruthy();
    });
  });

  describe('Performance', () => {
    it('should handle large number of notifications efficiently', () => {
      const manyNotifications = Array.from({ length: 100 }, (_, i) => ({
        ...mockNotifications[0],
        id: `notif-${i}`,
      }));

      notificationsSubject.next(manyNotifications);

      expect(() => {
        fixture.detectChanges();
      }).not.toThrow();
    });
  });

  describe('Time formatting', () => {
    it('should format recent timestamps as "Just now"', () => {
      const recentNotif: AppNotification = {
        ...mockNotifications[0],
        timestamp: new Date().toISOString(),
      };

      notificationsSubject.next([recentNotif]);
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const timestamp = compiled.querySelector('.notification-timestamp');

      expect(timestamp?.textContent).toContain('now');
    });

    it('should format old timestamps as relative time', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const timestamps = compiled.querySelectorAll('.notification-timestamp');

      timestamps.forEach((ts) => {
        expect(ts.textContent).toBeTruthy();
      });
    });

    it('should format timestamps in hours', () => {
      const oneHourAgo = new Date(Date.now() - 3600000).toISOString();
      const timestamp = component.formatTimestamp(oneHourAgo);

      expect(timestamp).toContain('h ago');
    });

    it('should format timestamps in days', () => {
      const oneDayAgo = new Date(Date.now() - 86400000 * 2).toISOString();
      const timestamp = component.formatTimestamp(oneDayAgo);

      expect(timestamp).toContain('d ago');
    });
  });

  describe('additional coverage', () => {
    it('should get filter count text', () => {
      fixture.detectChanges();

      const countText = component.getFilterCountText();

      expect(countText).toContain('of');
    });

    it('should apply combined filters', () => {
      fixture.detectChanges();

      component.filterByType('info');
      component.toggleUnreadFilter();

      expect(component.filteredNotifications).toBeDefined();
    });

    it('should get correct icon classes for all notification types', () => {
      const infoClass = component.getIconClass('info');
      const successClass = component.getIconClass('success');
      const warningClass = component.getIconClass('warning');
      const errorClass = component.getIconClass('error');

      expect(infoClass).toContain('blue');
      expect(successClass).toContain('green');
      expect(warningClass).toContain('yellow');
      expect(errorClass).toContain('red');
    });

    it('should format 1 minute as singular', () => {
      const oneMinuteAgo = new Date(Date.now() - 60000).toISOString();
      const formatted = component.formatTimestamp(oneMinuteAgo);

      expect(formatted).toBe('1m ago');
    });

    it('should format 1 hour as singular', () => {
      const oneHourAgo = new Date(Date.now() - 3600000).toISOString();
      const formatted = component.formatTimestamp(oneHourAgo);

      expect(formatted).toBe('1h ago');
    });

    it('should format 1 day as singular', () => {
      const oneDayAgo = new Date(Date.now() - 86400000).toISOString();
      const formatted = component.formatTimestamp(oneDayAgo);

      expect(formatted).toBe('1d ago');
    });

    it('should clear selectedType when filtering by all', () => {
      fixture.detectChanges();

      component.filterByType('info');
      expect(component.selectedType).toBe('info');

      component.filterByType('all');
      expect(component.selectedType).toBe('all');
    });

    it('should apply filters when notifications update', () => {
      fixture.detectChanges();
      spyOn(component as any, 'applyFilters');

      // Trigger notification update
      notificationsSubject.next([...mockNotifications]);

      expect((component as any).applyFilters).toHaveBeenCalled();
    });

    it('should stop propagation on delete button click', () => {
      fixture.detectChanges();
      const event = new Event('click');
      spyOn(event, 'stopPropagation');

      component.onDelete(event, '1');

      expect(event.stopPropagation).toHaveBeenCalled();
    });

    it('should handle marking already read notification', () => {
      notificationsSubject.next([{ ...mockNotifications[1], read: true }]);
      fixture.detectChanges();

      component.onNotificationClick(mockNotifications[1]);

      expect(notificationService.markAsRead).not.toHaveBeenCalled();
    });

    it('should format minutes correctly between 1-59', () => {
      const thirtyMinsAgo = new Date(Date.now() - 1800000).toISOString();
      const formatted = component.formatTimestamp(thirtyMinsAgo);

      expect(formatted).toContain('m ago');
      expect(formatted).not.toBe('1m ago');
    });

    it('should format hours correctly between 2-23', () => {
      const fiveHoursAgo = new Date(Date.now() - 18000000).toISOString();
      const formatted = component.formatTimestamp(fiveHoursAgo);

      expect(formatted).toContain('h ago');
      expect(formatted).not.toBe('1h ago');
    });

    it('should format days correctly for multiple days', () => {
      const threeDaysAgo = new Date(Date.now() - 259200000).toISOString();
      const formatted = component.formatTimestamp(threeDaysAgo);

      expect(formatted).toContain('d ago');
      expect(formatted).not.toBe('1d ago');
    });
  });
});
