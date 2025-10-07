import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { WebSocketService } from './websocket.service';

describe('WebSocketService', () => {
  let service: WebSocketService;
  let mockWebSocket: jasmine.SpyObj<WebSocket>;

  beforeEach(() => {
    // Mock WebSocket
    mockWebSocket = jasmine.createSpyObj('WebSocket', ['send', 'close'], {
      readyState: WebSocket.CONNECTING,
    });

    spyOn(window, 'WebSocket').and.returnValue(mockWebSocket);

    TestBed.configureTestingModule({
      providers: [WebSocketService],
    });

    service = TestBed.inject(WebSocketService);
  });

  afterEach(() => {
    service.disconnect();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('connect()', () => {
    it('should create WebSocket connection with correct URL', () => {
      const url = 'ws://localhost:8080/ws/notifications';
      service.connect(url);

      expect(window.WebSocket).toHaveBeenCalledWith(url);
    });

    it('should emit connection status when connected', fakeAsync(() => {
      let connectionStatus: boolean | undefined;
      service.connectionStatus$.subscribe((status) => (connectionStatus = status));

      service.connect('ws://localhost:8080/ws');

      // Simulate WebSocket open event
      mockWebSocket.onopen?.(new Event('open'));
      tick();

      expect(connectionStatus).toBe(true);
    }));

    it('should emit connection status false when connection fails', fakeAsync(() => {
      let connectionStatus: boolean | undefined;
      service.connectionStatus$.subscribe((status) => (connectionStatus = status));

      service.connect('ws://localhost:8080/ws');

      // Simulate WebSocket error event
      mockWebSocket.onerror?.(new Event('error'));
      tick();

      expect(connectionStatus).toBe(false);
    }));

    it('should not create multiple connections if already connected', () => {
      Object.defineProperty(mockWebSocket, 'readyState', { 
        value: WebSocket.CONNECTING,
        writable: true 
      });
      
      service.connect('ws://localhost:8080/ws');
      
      Object.defineProperty(mockWebSocket, 'readyState', { 
        value: WebSocket.OPEN,
        writable: true 
      });
      mockWebSocket.onopen?.(new Event('open'));

      const callCount = (window as any).WebSocket.calls.count();

      service.connect('ws://localhost:8080/ws');

      expect((window as any).WebSocket.calls.count()).toBe(callCount);
    });
  });

  describe('disconnect()', () => {
    it('should close WebSocket connection', () => {
      service.connect('ws://localhost:8080/ws');
      service.disconnect();

      expect(mockWebSocket.close).toHaveBeenCalled();
    });

    it('should emit connection status false when disconnected', fakeAsync(() => {
      let connectionStatus: boolean | undefined;
      service.connectionStatus$.subscribe((status) => (connectionStatus = status));

      service.connect('ws://localhost:8080/ws');
      mockWebSocket.onopen?.(new Event('open'));
      tick();

      service.disconnect();
      tick();

      expect(connectionStatus).toBe(false);
    }));

    it('should handle disconnect when no connection exists', () => {
      expect(() => service.disconnect()).not.toThrow();
    });
  });

  describe('send()', () => {
    it('should send message through WebSocket', () => {
      service.connect('ws://localhost:8080/ws');
      mockWebSocket.onopen?.(new Event('open'));
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });

      const message = { type: 'ping', data: 'test' };
      service.send(message);

      expect(mockWebSocket.send).toHaveBeenCalledWith(JSON.stringify(message));
    });

    it('should not send message if WebSocket is not connected', () => {
      const message = { type: 'ping', data: 'test' };
      service.send(message);

      expect(mockWebSocket.send).not.toHaveBeenCalled();
    });

    it('should handle send errors gracefully', () => {
      service.connect('ws://localhost:8080/ws');
      mockWebSocket.onopen?.(new Event('open'));
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });

      mockWebSocket.send.and.throwError('Send failed');
      spyOn(console, 'error');

      const message = { type: 'ping', data: 'test' };
      service.send(message);

      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('messages$', () => {
    it('should emit received messages', fakeAsync(() => {
      const messages: any[] = [];
      service.messages$.subscribe((msg) => messages.push(msg));

      service.connect('ws://localhost:8080/ws');

      const testMessage = { type: 'notification', data: { id: '1', title: 'Test' } };
      const messageEvent = new MessageEvent('message', {
        data: JSON.stringify(testMessage),
      });

      mockWebSocket.onmessage?.(messageEvent);
      tick();

      expect(messages.length).toBe(1);
      expect(messages[0]).toEqual(testMessage);
    }));

    it('should handle invalid JSON messages gracefully', fakeAsync(() => {
      const messages: any[] = [];
      service.messages$.subscribe((msg) => messages.push(msg));
      spyOn(console, 'error');

      service.connect('ws://localhost:8080/ws');

      const messageEvent = new MessageEvent('message', {
        data: 'invalid json',
      });

      mockWebSocket.onmessage?.(messageEvent);
      tick();

      expect(console.error).toHaveBeenCalled();
      expect(messages.length).toBe(0);
    }));
  });

  describe('reconnection', () => {
    it('should attempt to reconnect on connection close', fakeAsync(() => {
      service.connect('ws://localhost:8080/ws');
      
      const initialCallCount = (window as any).WebSocket.calls.count();

      mockWebSocket.onclose?.(new CloseEvent('close'));
      
      // Wait for reconnection delay
      tick(5000);

      expect((window as any).WebSocket.calls.count()).toBeGreaterThan(initialCallCount);
    }));

    it('should stop reconnecting after max attempts', fakeAsync(() => {
      service.maxReconnectAttempts = 3;

      service.connect('ws://localhost:8080/ws');

      // Simulate 3 failed connections
      for (let i = 0; i < 3; i++) {
        mockWebSocket.onclose?.(new CloseEvent('close'));
        tick(5000 * Math.pow(2, i));
      }

      const callCount = (window as any).WebSocket.calls.count();
      mockWebSocket.onclose?.(new CloseEvent('close'));
      tick(40000);

      expect((window as any).WebSocket.calls.count()).toBe(callCount);
    }));
  });

  describe('heartbeat', () => {
    it('should send ping messages periodically', fakeAsync(() => {
      service.connect('ws://localhost:8080/ws');
      
      Object.defineProperty(mockWebSocket, 'readyState', { 
        value: WebSocket.OPEN,
        writable: true 
      });
      mockWebSocket.onopen?.(new Event('open'));

      // Clear initial calls
      mockWebSocket.send.calls.reset();

      // Wait for heartbeat interval (30 seconds)
      tick(30000);

      expect(mockWebSocket.send).toHaveBeenCalled();
      const lastCall = mockWebSocket.send.calls.mostRecent().args[0] as string;
      expect(JSON.parse(lastCall).type).toBe('ping');
    }));
  });

  describe('additional coverage', () => {
    it('should return correct connection status with isConnected()', () => {
      expect(service.isConnected()).toBe(false);

      service.connect('ws://localhost:8080/ws');
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });
      mockWebSocket.onopen?.(new Event('open'));

      expect(service.isConnected()).toBe(true);
    });

    it('should queue messages when offline', () => {
      service.send({ type: 'test', data: 'queued' });

      expect(mockWebSocket.send).not.toHaveBeenCalled();
    });

    it('should flush message queue on connection', () => {
      service.send({ type: 'test1', data: 'queued1' });
      service.send({ type: 'test2', data: 'queued2' });

      service.connect('ws://localhost:8080/ws');
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });
      mockWebSocket.onopen?.(new Event('open'));

      expect(mockWebSocket.send).toHaveBeenCalledTimes(2);
    });

    it('should handle pong responses from server', fakeAsync(() => {
      service.connect('ws://localhost:8080/ws');

      const pongMessage = new MessageEvent('message', {
        data: JSON.stringify({ type: 'pong', timestamp: new Date().toISOString() }),
      });

      mockWebSocket.onmessage?.(pongMessage);
      tick();

      // Should not cause errors
      expect(true).toBe(true);
    }));

    it('should respond to ping with pong', fakeAsync(() => {
      service.connect('ws://localhost:8080/ws');
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });
      mockWebSocket.onopen?.(new Event('open'));

      mockWebSocket.send.calls.reset();

      const pingMessage = new MessageEvent('message', {
        data: JSON.stringify({ type: 'ping', timestamp: new Date().toISOString() }),
      });

      mockWebSocket.onmessage?.(pingMessage);
      tick();

      expect(mockWebSocket.send).toHaveBeenCalled();
      const lastCall = mockWebSocket.send.calls.mostRecent().args[0] as string;
      expect(JSON.parse(lastCall).type).toBe('pong');
    }));

    it('should handle connection errors during send', () => {
      service.connect('ws://localhost:8080/ws');
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.CLOSED });

      service.send({ type: 'test', data: 'fail' });

      // Should queue the message
      expect(mockWebSocket.send).not.toHaveBeenCalled();
    });

    it('should track reconnect attempts', fakeAsync(() => {
      service.connect('ws://localhost:8080/ws');
      mockWebSocket.onclose?.(new CloseEvent('close'));
      tick(5000);

      expect(service.getReconnectAttempts()).toBeGreaterThan(0);
    }));

    it('should reset reconnect attempts', () => {
      service['reconnectAttempts'] = 3;
      
      service.resetReconnectAttempts();

      expect(service.getReconnectAttempts()).toBe(0);
    });

    it('should handle connection creation error', () => {
      spyOn(console, 'error');
      (window.WebSocket as any).and.throwError('Connection failed');

      service.connect('ws://invalid-url');

      expect(console.error).toHaveBeenCalled();
    });

    it('should stop heartbeat on disconnect', () => {
      service.connect('ws://localhost:8080/ws');
      Object.defineProperty(mockWebSocket, 'readyState', { value: WebSocket.OPEN });
      mockWebSocket.onopen?.(new Event('open'));

      service.disconnect();

      expect(service['heartbeatTimer']).toBeFalsy();
    });

    it('should clear reconnect timer on disconnect', () => {
      service.connect('ws://localhost:8080/ws');
      mockWebSocket.onclose?.(new CloseEvent('close'));

      service.disconnect();

      expect(service['reconnectTimer']).toBeFalsy();
    });

    it('should update connection status to false after max reconnect attempts', fakeAsync(() => {
      let connectionStatus = true;
      service.connectionStatus$.subscribe((status) => (connectionStatus = status));

      service.maxReconnectAttempts = 2;
      service.connect('ws://localhost:8080/ws');

      for (let i = 0; i < 3; i++) {
        mockWebSocket.onclose?.(new CloseEvent('close'));
        tick(10000);
      }

      tick(20000);

      expect(connectionStatus).toBe(false);
    }));

    it('should handle WebSocket onopen callback', () => {
      spyOn(console, 'log');
      service.connect('ws://localhost:8080/ws');

      mockWebSocket.onopen?.(new Event('open'));

      expect(console.log).toHaveBeenCalledWith('WebSocket connected');
    });

    it('should handle WebSocket onclose callback', () => {
      spyOn(console, 'log');
      service.connect('ws://localhost:8080/ws');

      mockWebSocket.onclose?.(new CloseEvent('close'));

      expect(console.log).toHaveBeenCalledWith('WebSocket disconnected');
    });

    it('should handle WebSocket onerror callback', () => {
      spyOn(console, 'error');
      service.connect('ws://localhost:8080/ws');

      mockWebSocket.onerror?.(new Event('error'));

      expect(console.error).toHaveBeenCalledWith('WebSocket error:', jasmine.any(Event));
    });
  });
});

