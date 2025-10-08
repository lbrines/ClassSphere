/**
 * Notification Models for Phase 3 - Real-time Notifications
 * WebSocket-based notification system with priority levels
 */

export type NotificationType = 'info' | 'success' | 'warning' | 'error';
export type NotificationPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface AppNotification {
  id: string;
  type: NotificationType;
  priority: NotificationPriority;
  title: string;
  message: string;
  timestamp: string; // ISO 8601 format
  read: boolean;
  actionUrl?: string;
  actionLabel?: string;
  metadata?: Record<string, any>;
}

export interface NotificationState {
  notifications: AppNotification[];
  unreadCount: number;
  loading: boolean;
  error: string | null;
  connected: boolean; // WebSocket connection status
}

export interface WebSocketMessage {
  type: 'notification' | 'ping' | 'pong' | 'connection' | 'error';
  data?: any;
  timestamp?: string;
}

export interface NotificationPreferences {
  enabled: boolean;
  sound: boolean;
  desktop: boolean;
  email: boolean;
  priorityFilter: NotificationPriority[];
}

