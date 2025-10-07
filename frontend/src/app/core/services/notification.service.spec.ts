import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';

import { NotificationService } from './notification.service';
import { WebSocketService } from './websocket.service';
import { AppNotification, WebSocketMessage } from '../models/notification.model';

describe('NotificationService', () => {
  let service: NotificationService;
  let webSocketService: jasmine.SpyObj<WebSocketService>;
  let mockMessages$: Subject<WebSocketMessage>;
  let mockConnectionStatus$: Subject<boolean>;

  const mockNotification: AppNotification = {
    id: 'notif-001',
    type: 'info',
    priority: 'medium',
    title: 'Test Notification',
    message: 'This is a test notification',
    timestamp: '2025-10-07T12:00:00Z',
    read: false,
  };

  beforeEach(() => {
    mockMessages$ = new Subject<WebSocketMessage>();
    mockConnectionStatus$ = new Subject<boolean>();

    const webSocketServiceSpy = jasmine.createSpyObj(
      'WebSocketService',
      ['connect', 'disconnect', 'send', 'isConnected'],
      {
        messages$: mockMessages$.asObservable(),
        connectionStatus$: mockConnectionStatus$.asObservable(),
      }
    );

    TestBed.configureTestingModule({
      providers: [
        NotificationService,
        { provide: WebSocketService, useValue: webSocketServiceSpy },
      ],
    });

    service = TestBed.inject(NotificationService);
    webSocketService = TestBed.inject(WebSocketService) as jasmine.SpyObj<WebSocketService>;
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('initialization', () => {
    it('should connect to WebSocket on init', () => {
      service.initialize();

      expect(webSocketService.connect).toHaveBeenCalled();
    });

    it('should start with empty notifications', (done) => {
      service.notifications$.subscribe((notifications) => {
        expect(notifications).toEqual([]);
        done();
      });
    });

    it('should have unread count of 0 initially', (done) => {
      service.unreadCount$.subscribe((count) => {
        expect(count).toBe(0);
        done();
      });
    });
  });

  describe('receiving notifications', () => {
    it('should add notification when received from WebSocket', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      mockMessages$.next({
        type: 'notification',
        data: mockNotification,
      });

      tick();

      expect(notifications.length).toBe(1);
      expect(notifications[0]).toEqual(mockNotification);
    }));

    it('should update unread count when new notification arrives', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();

      mockMessages$.next({
        type: 'notification',
        data: mockNotification,
      });

      tick();

      expect(unreadCount).toBe(1);
    }));

    it('should not add duplicate notifications', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      expect(notifications.length).toBe(1);
    }));

    it('should sort notifications by timestamp (newest first)', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      const oldNotif = { ...mockNotification, id: '1', timestamp: '2025-10-07T10:00:00Z' };
      const newNotif = { ...mockNotification, id: '2', timestamp: '2025-10-07T12:00:00Z' };

      mockMessages$.next({ type: 'notification', data: oldNotif });
      tick();
      mockMessages$.next({ type: 'notification', data: newNotif });
      tick();

      expect(notifications[0].id).toBe('2'); // Newest first
      expect(notifications[1].id).toBe('1');
    }));

    it('should play sound for high priority notifications', fakeAsync(() => {
      spyOn(service as any, 'playNotificationSound');

      service.initialize();

      const highPriorityNotif = { ...mockNotification, priority: 'high' as const };
      mockMessages$.next({ type: 'notification', data: highPriorityNotif });

      tick();

      expect((service as any).playNotificationSound).toHaveBeenCalled();
    }));
  });

  describe('markAsRead()', () => {
    it('should mark notification as read', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      service.markAsRead('notif-001');
      tick();

      expect(notifications[0].read).toBe(true);
    }));

    it('should decrease unread count when marking as read', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      expect(unreadCount).toBe(1);

      service.markAsRead('notif-001');
      tick();

      expect(unreadCount).toBe(0);
    }));

    it('should handle marking non-existent notification', fakeAsync(() => {
      service.initialize();

      expect(() => {
        service.markAsRead('non-existent-id');
        tick();
      }).not.toThrow();
    }));
  });

  describe('markAllAsRead()', () => {
    it('should mark all notifications as read', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '1' } });
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '2' } });
      tick();

      service.markAllAsRead();
      tick();

      expect(notifications.every((n) => n.read)).toBe(true);
    }));

    it('should set unread count to 0', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      service.markAllAsRead();
      tick();

      expect(unreadCount).toBe(0);
    }));
  });

  describe('deleteNotification()', () => {
    it('should remove notification from list', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      service.deleteNotification('notif-001');
      tick();

      expect(notifications.length).toBe(0);
    }));

    it('should update unread count if deleted notification was unread', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      expect(unreadCount).toBe(1);

      service.deleteNotification('notif-001');
      tick();

      expect(unreadCount).toBe(0);
    }));
  });

  describe('clearAll()', () => {
    it('should remove all notifications', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '1' } });
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '2' } });
      tick();

      service.clearAll();
      tick();

      expect(notifications.length).toBe(0);
    }));

    it('should reset unread count to 0', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      service.clearAll();
      tick();

      expect(unreadCount).toBe(0);
    }));
  });

  describe('connection status', () => {
    it('should reflect WebSocket connection status', fakeAsync(() => {
      let connected = false;
      service.connectionStatus$.subscribe((status) => (connected = status));

      service.initialize();
      mockConnectionStatus$.next(true);
      tick();

      expect(connected).toBe(true);

      mockConnectionStatus$.next(false);
      tick();

      expect(connected).toBe(false);
    }));
  });

  describe('desktop notifications', () => {
    it('should request permission for desktop notifications', () => {
      spyOn(Notification, 'requestPermission').and.returnValue(
        Promise.resolve('granted')
      );

      service.requestDesktopPermission();

      expect(Notification.requestPermission).toHaveBeenCalled();
    });

    it('should show desktop notification for high priority', fakeAsync(() => {
      spyOn(service as any, 'showDesktopNotification');

      // Mock permission granted
      Object.defineProperty(Notification, 'permission', {
        value: 'granted',
        configurable: true,
      });

      service.initialize();

      const urgentNotif = { ...mockNotification, priority: 'urgent' as const };
      mockMessages$.next({ type: 'notification', data: urgentNotif });

      tick();

      expect((service as any).showDesktopNotification).toHaveBeenCalled();
    }));
  });

  describe('filtering', () => {
    it('should filter notifications by type', fakeAsync(() => {
      service.initialize();

      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '1', type: 'info' as const },
      });
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '2', type: 'error' as const },
      });
      tick();

      const filtered = service.getNotificationsByType('error');

      expect(filtered.length).toBe(1);
      expect(filtered[0].type).toBe('error');
    }));

    it('should filter unread notifications', fakeAsync(() => {
      service.initialize();

      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '1' } });
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '2', read: true },
      });
      tick();

      const unread = service.getUnreadNotifications();

      expect(unread.length).toBe(1);
      expect(unread[0].read).toBe(false);
    }));
  });

  describe('edge cases', () => {
    it('should handle non-notification WebSocket messages', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      mockMessages$.next({ type: 'ping', data: {} });
      tick();

      expect(notifications.length).toBe(0);
    }));

    it('should handle WebSocket connection lost during operation', fakeAsync(() => {
      let connected = true;
      service.connectionStatus$.subscribe((status) => (connected = status));

      service.initialize();
      mockConnectionStatus$.next(true);
      tick();

      mockConnectionStatus$.next(false);
      tick();

      expect(connected).toBe(false);
    }));

    it('should handle rapid notification bursts', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      // Send 10 notifications rapidly
      for (let i = 0; i < 10; i++) {
        mockMessages$.next({
          type: 'notification',
          data: { ...mockNotification, id: `notif-${i}` },
        });
      }
      tick();

      expect(notifications.length).toBe(10);
    }));

    it('should maintain sort order after marking as read', fakeAsync(() => {
      let notifications: AppNotification[] = [];
      service.notifications$.subscribe((n) => (notifications = n));

      service.initialize();

      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '1', timestamp: '2025-10-07T10:00:00Z' },
      });
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '2', timestamp: '2025-10-07T11:00:00Z' },
      });
      tick();

      service.markAsRead('2');
      tick();

      // Should still be sorted by timestamp
      expect(notifications[0].id).toBe('2');
      expect(notifications[1].id).toBe('1');
    }));
  });

  describe('utility methods', () => {
    it('should get notifications count', fakeAsync(() => {
      service.initialize();

      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '1' } });
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, id: '2' } });
      tick();

      expect(service.getNotificationsCount()).toBe(2);
    }));

    it('should check if has unread notifications', fakeAsync(() => {
      service.initialize();

      expect(service.hasUnread()).toBe(false);

      mockMessages$.next({ type: 'notification', data: mockNotification });
      tick();

      expect(service.hasUnread()).toBe(true);
    }));

    it('should not play sound for low priority notifications', fakeAsync(() => {
      spyOn(service as any, 'playNotificationSound');

      service.initialize();

      const lowPriorityNotif = { ...mockNotification, priority: 'low' as const };
      mockMessages$.next({ type: 'notification', data: lowPriorityNotif });
      tick();

      expect((service as any).playNotificationSound).not.toHaveBeenCalled();
    }));

    it('should handle Notification API not available', async () => {
      const originalNotification = (window as any).Notification;
      delete (window as any).Notification;

      const permission = await service.requestDesktopPermission();

      expect(permission).toBe('denied');

      (window as any).Notification = originalNotification;
    });

    it('should update unread count after deleting unread notification', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, read: false } });
      tick();

      const initialCount = unreadCount;
      service.deleteNotification(mockNotification.id);
      tick();

      expect(unreadCount).toBeLessThan(initialCount);
    }));

    it('should handle Audio API not available', fakeAsync(() => {
      const originalAudio = (window as any).Audio;
      (window as any).Audio = undefined;
      spyOn(console, 'warn');

      service.initialize();
      const highPriorityNotif = { ...mockNotification, priority: 'high' as const };
      mockMessages$.next({ type: 'notification', data: highPriorityNotif });
      tick();

      expect(console.warn).toHaveBeenCalledWith('Audio API not available');

      (window as any).Audio = originalAudio;
    }));

    it('should not update unread count if marking already read notification', fakeAsync(() => {
      let unreadCount = 0;
      service.unreadCount$.subscribe((count) => (unreadCount = count));

      service.initialize();
      mockMessages$.next({ type: 'notification', data: { ...mockNotification, read: true } });
      tick();

      expect(unreadCount).toBe(0);

      service.markAsRead(mockNotification.id);
      tick();

      expect(unreadCount).toBe(0);
    }));

    it('should handle priority combinations correctly', fakeAsync(() => {
      spyOn(service as any, 'playNotificationSound');
      spyOn(service as any, 'showDesktopNotification');

      service.initialize();

      // Medium priority - no sound, no desktop
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '1', priority: 'medium' as const },
      });
      tick();
      expect((service as any).playNotificationSound).not.toHaveBeenCalled();

      // High priority - sound, no desktop
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '2', priority: 'high' as const },
      });
      tick();
      expect((service as any).playNotificationSound).toHaveBeenCalled();

      // Urgent priority - sound and desktop
      mockMessages$.next({
        type: 'notification',
        data: { ...mockNotification, id: '3', priority: 'urgent' as const },
      });
      tick();
      expect((service as any).showDesktopNotification).toHaveBeenCalled();
    }));

    it('should handle audio play promise rejection', fakeAsync(() => {
      spyOn(console, 'warn');
      const mockAudio = {
        volume: 0.5,
        play: jasmine.createSpy('play').and.returnValue(Promise.reject('Audio error')),
      };
      spyOn(window as any, 'Audio').and.returnValue(mockAudio);

      service.initialize();
      const highPriorityNotif = { ...mockNotification, priority: 'high' as const };
      mockMessages$.next({ type: 'notification', data: highPriorityNotif });
      tick();
      tick(100); // Wait for promise rejection

      expect(console.warn).toHaveBeenCalledWith('Failed to play notification sound:', 'Audio error');
    }));

    it('should handle audio creation error in catch block', fakeAsync(() => {
      spyOn(console, 'warn');
      spyOn(window as any, 'Audio').and.throwError('Audio constructor error');

      service.initialize();
      const highPriorityNotif = { ...mockNotification, priority: 'high' as const };
      mockMessages$.next({ type: 'notification', data: highPriorityNotif });
      tick();

      expect(console.warn).toHaveBeenCalledWith('Notification sound not available:', jasmine.any(Error));
    }));
  });
});

