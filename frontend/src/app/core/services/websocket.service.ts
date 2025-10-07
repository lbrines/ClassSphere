import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { WebSocketMessage } from '../models/notification.model';

/**
 * WebSocketService - Phase 3 Real-time Communication
 * 
 * Features:
 * - WebSocket connection management
 * - Automatic reconnection with exponential backoff
 * - Heartbeat/ping mechanism
 * - Message queue for offline messages
 * - Connection status monitoring
 */
@Injectable({ providedIn: 'root' })
export class WebSocketService implements OnDestroy {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private reconnectTimer: any;
  private heartbeatTimer: any;
  private messageQueue: any[] = [];

  maxReconnectAttempts = 5;
  reconnectInterval = 5000; // 5 seconds
  heartbeatInterval = 30000; // 30 seconds

  private readonly connectionStatusSubject = new BehaviorSubject<boolean>(false);
  private readonly messagesSubject = new Subject<WebSocketMessage>();

  readonly connectionStatus$ = this.connectionStatusSubject.asObservable();
  readonly messages$ = this.messagesSubject.asObservable();

  /**
   * Connect to WebSocket server
   * @param url WebSocket URL (e.g., ws://localhost:8080/ws/notifications)
   */
  connect(url: string): void {
    // Don't create multiple connections
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.connectionStatusSubject.next(true);
        this.reconnectAttempts = 0;
        this.startHeartbeat();
        this.flushMessageQueue();
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.messagesSubject.next(message);

          // Respond to ping with pong
          if (message.type === 'ping') {
            this.send({ type: 'pong', timestamp: new Date().toISOString() });
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.connectionStatusSubject.next(false);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.connectionStatusSubject.next(false);
        this.stopHeartbeat();
        this.attemptReconnect(url);
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      this.connectionStatusSubject.next(false);
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.stopHeartbeat();

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.connectionStatusSubject.next(false);
  }

  /**
   * Send message through WebSocket
   * @param message Message to send
   */
  send(message: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify(message));
      } catch (error) {
        console.error('Failed to send WebSocket message:', error);
        this.messageQueue.push(message);
      }
    } else {
      // Queue message for sending when connection is restored
      this.messageQueue.push(message);
    }
  }

  /**
   * Get current connection status (synchronous)
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * Get reconnect attempts count
   */
  getReconnectAttempts(): number {
    return this.reconnectAttempts;
  }

  /**
   * Reset reconnect attempts (for testing)
   */
  resetReconnectAttempts(): void {
    this.reconnectAttempts = 0;
  }

  ngOnDestroy(): void {
    this.disconnect();
  }

  /**
   * Attempt to reconnect with exponential backoff
   */
  private attemptReconnect(url: string): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.connectionStatusSubject.next(false);
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      this.connect(url);
    }, delay);
  }

  /**
   * Start heartbeat mechanism to keep connection alive
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();

    this.heartbeatTimer = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'ping', timestamp: new Date().toISOString() });
      }
    }, this.heartbeatInterval);
  }

  /**
   * Stop heartbeat mechanism
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /**
   * Send queued messages when connection is restored
   */
  private flushMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
  }
}

