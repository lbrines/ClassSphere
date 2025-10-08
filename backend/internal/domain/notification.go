package domain

import "time"

// Notification represents a system notification for a user.
type Notification struct {
	ID        string
	UserID    string
	Type      NotificationType
	Title     string
	Message   string
	Data      map[string]interface{} // Optional structured data
	Read      bool
	CreatedAt time.Time
	ReadAt    *time.Time
}

// NotificationType categorizes notifications for UI rendering.
type NotificationType string

const (
	NotificationTypeInfo    NotificationType = "info"
	NotificationTypeSuccess NotificationType = "success"
	NotificationTypeWarning NotificationType = "warning"
	NotificationTypeError   NotificationType = "error"
)

// IsValid checks if the notification type is valid.
func (nt NotificationType) IsValid() bool {
	switch nt {
	case NotificationTypeInfo, NotificationTypeSuccess, NotificationTypeWarning, NotificationTypeError:
		return true
	default:
		return false
	}
}

// MarkAsRead marks the notification as read with timestamp.
func (n *Notification) MarkAsRead() {
	now := time.Now()
	n.Read = true
	n.ReadAt = &now
}

