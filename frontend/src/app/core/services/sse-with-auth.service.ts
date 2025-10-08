import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { WebSocketMessage } from '../models/notification.model';

/**
 * SSEWithAuthService - Enhanced SSE with Custom Headers Support
 * 
 * Uses fetch API + ReadableStream to implement EventSource with Authorization headers.
 * This is necessary because native EventSource doesn't support custom headers.
 * 
 * Features:
 * - JWT authentication via Authorization header
 * - Manual reconnection with exponential backoff
 * - Connection status monitoring
 * - Event parsing (event: type, data: json)
 * - Keep-alive handling
 * 
 * Based on: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
 */
@Injectable({ providedIn: 'root' })
export class SSEWithAuthService implements OnDestroy {
  private abortController: AbortController | null = null;
  private reconnectTimer: any;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectBaseDelay = 1000; // 1 second

  private readonly connectionStatusSubject = new BehaviorSubject<boolean>(false);
  private readonly messagesSubject = new Subject<WebSocketMessage>();

  readonly connectionStatus$ = this.connectionStatusSubject.asObservable();
  readonly messages$ = this.messagesSubject.asObservable();

  /**
   * Connect to SSE endpoint with Authorization header
   * @param url SSE URL
   * @param token JWT token
   */
  async connect(url: string, token: string): Promise<void> {
    // Don't create multiple connections
    if (this.abortController && !this.abortController.signal.aborted) {
      console.warn('SSE already connected');
      return;
    }

    this.abortController = new AbortController();

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        signal: this.abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`SSE connection failed: ${response.status} ${response.statusText}`);
      }

      if (!response.body) {
        throw new Error('SSE response body is null');
      }

      console.log('SSE connected via fetch');
      this.connectionStatusSubject.next(true);
      this.reconnectAttempts = 0;

      // Read the stream
      await this.readStream(response.body);
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('SSE connection aborted');
        return;
      }

      console.error('SSE connection error:', error);
      this.connectionStatusSubject.next(false);

      // Attempt reconnection
      this.attemptReconnect(url, token);
    }
  }

  /**
   * Disconnect from SSE
   */
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }

    this.connectionStatusSubject.next(false);
  }

  /**
   * Get current connection status
   */
  isConnected(): boolean {
    return this.connectionStatusSubject.value;
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
   * Read and parse SSE stream
   */
  private async readStream(body: ReadableStream<Uint8Array>): Promise<void> {
    const reader = body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          console.log('SSE stream ended');
          this.connectionStatusSubject.next(false);
          break;
        }

        // Decode chunk and add to buffer
        buffer += decoder.decode(value, { stream: true });

        // Process complete messages (separated by \n\n)
        const messages = buffer.split('\n\n');
        buffer = messages.pop() || ''; // Keep incomplete message in buffer

        for (const message of messages) {
          if (message.trim()) {
            this.parseSSEMessage(message);
          }
        }
      }
    } catch (error) {
      console.error('SSE stream read error:', error);
      this.connectionStatusSubject.next(false);
    } finally {
      reader.releaseLock();
    }
  }

  /**
   * Parse SSE message format:
   * event: type
   * data: json
   */
  private parseSSEMessage(message: string): void {
    const lines = message.split('\n');
    let eventType = 'message'; // default
    let data = '';

    for (const line of lines) {
      if (line.startsWith(':')) {
        // Comment (keep-alive), ignore
        continue;
      }

      if (line.startsWith('event:')) {
        eventType = line.substring(6).trim();
      } else if (line.startsWith('data:')) {
        data += line.substring(5).trim();
      }
    }

    if (data) {
      try {
        const parsedData = JSON.parse(data);
        this.messagesSubject.next({
          type: eventType,
          data: parsedData,
        });
      } catch (error) {
        console.error('Failed to parse SSE data:', error, data);
      }
    }
  }

  /**
   * Attempt reconnection with exponential backoff
   */
  private attemptReconnect(url: string, token: string): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max SSE reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectBaseDelay * Math.pow(2, this.reconnectAttempts - 1);
    const maxDelay = 30000; // Max 30 seconds
    const actualDelay = Math.min(delay, maxDelay);

    console.log(`Reconnecting SSE in ${actualDelay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      this.connect(url, token);
    }, actualDelay);
  }
}

