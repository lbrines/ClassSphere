import { TestBed, fakeAsync, flushMicrotasks, tick } from '@angular/core/testing';
import { BehaviorSubject, Subject } from 'rxjs';

import { NotificationService } from './notification.service';
import { SSEWithAuthService } from './sse-with-auth.service';
import { EnvironmentService } from './environment.service';
import { AppNotification, WebSocketMessage } from '../models/notification.model';

describe('NotificationService (SSE integration)', () => {
  let service: NotificationService;
  let sseService: {
    connect: jasmine.Spy<(url: string, token: string) => Promise<void>>;
    disconnect: jasmine.Spy<() => void>;
    messages$: Subject<WebSocketMessage>;
    connectionStatus$: BehaviorSubject<boolean>;
  };
  let runtimeNotification: any;
  let originalNotification: Notification | undefined;
  let originalAudio: typeof Audio | undefined;

  const runtimeApiUrl = 'http://localhost:8080/api/v1';
  const authToken = 'token-123';

  const baseNotification: AppNotification = {
    id: 'notif-001',
    type: 'info',
    priority: 'medium',
    title: 'Test notification',
    message: 'Notification body',
    timestamp: '2025-10-09T00:00:00Z',
    read: false,
  };

  beforeAll(() => {
    originalNotification = (window as any).Notification;
    originalAudio = (window as any).Audio;
  });

  afterAll(() => {
    (window as any).Notification = originalNotification;
    (window as any).Audio = originalAudio;
  });

  beforeEach(() => {
    sseService = {
      connect: jasmine.createSpy('connect').and.resolveTo(),
      disconnect: jasmine.createSpy('disconnect'),
      messages$: new Subject<WebSocketMessage>(),
      connectionStatus$: new BehaviorSubject<boolean>(false),
    };

    runtimeNotification = {
      requestPermission: jasmine.createSpy('requestPermission').and.resolveTo('granted'),
    };
    Object.defineProperty(runtimeNotification, 'permission', {
      configurable: true,
      get: () => 'default',
    });

    (window as any).Notification = runtimeNotification;
    (window as any).Audio = originalAudio ?? Audio;

    TestBed.configureTestingModule({
      providers: [
        NotificationService,
        { provide: SSEWithAuthService, useValue: sseService },
        { provide: EnvironmentService, useValue: { apiUrl: runtimeApiUrl } },
      ],
    });

    service = TestBed.inject(NotificationService);
  });

  afterEach(() => {
    sseService.messages$.complete();
    sseService.connectionStatus$.complete();
  });

  function initialize(): void {
    service.initialize(authToken);
    flushMicrotasks();
    tick();
  }

  it('connects to SSE endpoint with runtime API URL', fakeAsync(() => {
    initialize();

    expect(sseService.connect).toHaveBeenCalledWith(`${runtimeApiUrl}/notifications/stream`, authToken);
  }));

  it('ignores initialization when token is missing', fakeAsync(() => {
    service.initialize('');
    tick();

    expect(sseService.connect).not.toHaveBeenCalled();
  }));

  it('adds incoming notifications and updates unread count', fakeAsync(() => {
    let latestNotifications: AppNotification[] = [];
    let unread = 0;

    service.notifications$.subscribe((items) => (latestNotifications = items));
    service.unreadCount$.subscribe((count) => (unread = count));

    initialize();

    sseService.messages$.next({ type: 'notification', data: baseNotification });
    tick();

    expect(latestNotifications.length).toBe(1);
    expect(unread).toBe(1);
  }));

  it('marks notifications as read', fakeAsync(() => {
    initialize();

    sseService.messages$.next({ type: 'notification', data: baseNotification });
    tick();

    service.markAsRead(baseNotification.id);
    tick();

    const result = service.getUnreadNotifications();
    expect(result.length).toBe(0);
  }));

  it('clears notifications and unread count', fakeAsync(() => {
    initialize();

    sseService.messages$.next({ type: 'notification', data: baseNotification });
    tick();

    service.clearAll();
    tick();

    expect(service.getNotificationsCount()).toBe(0);
    expect(service.hasUnread()).toBe(false);
  }));

  it('reflects SSE connection status updates', fakeAsync(() => {
    let connected = false;
    service.connectionStatus$.subscribe((status) => (connected = status));

    initialize();

    sseService.connectionStatus$.next(true);
    tick();
    expect(connected).toBe(true);

    sseService.connectionStatus$.next(false);
    tick();
    expect(connected).toBe(false);
  }));

  it('requests desktop permission via Notification API', async () => {
    const permission = await service.requestDesktopPermission();

    expect(runtimeNotification.requestPermission).toHaveBeenCalled();
    expect(permission).toBe('granted');
  });

  it('falls back when Notification API is unavailable', async () => {
    (window as any).Notification = undefined;

    const permission = await service.requestDesktopPermission();

    expect(permission).toBe('denied');
  });

  it('plays sound for high priority notifications when Audio is available', fakeAsync(() => {
    const playSpy = jasmine.createSpy('play').and.returnValue(Promise.resolve());
    (window as any).Audio = jasmine.createSpy('Audio').and.returnValue({
      volume: 0,
      play: playSpy,
    });

    initialize();

    const urgentNotification = { ...baseNotification, priority: 'high' as const };
    sseService.messages$.next({ type: 'notification', data: urgentNotification });
    tick();

    expect(playSpy).toHaveBeenCalled();
  }));

  it('disconnects SSE stream on destroy', fakeAsync(() => {
    initialize();

    service.ngOnDestroy();
    tick();

    expect(sseService.disconnect).toHaveBeenCalled();
  }));
});
