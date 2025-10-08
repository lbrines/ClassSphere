package domain

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestNotificationType_IsValid(t *testing.T) {
	tests := []struct {
		name     string
		notifType NotificationType
		expected  bool
	}{
		{"info is valid", NotificationTypeInfo, true},
		{"success is valid", NotificationTypeSuccess, true},
		{"warning is valid", NotificationTypeWarning, true},
		{"error is valid", NotificationTypeError, true},
		{"empty is invalid", NotificationType(""), false},
		{"unknown is invalid", NotificationType("unknown"), false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.expected, tt.notifType.IsValid())
		})
	}
}

func TestNotification_MarkAsRead(t *testing.T) {
	// Setup
	notification := &Notification{
		ID:      "notif-1",
		UserID:  "user-1",
		Type:    NotificationTypeInfo,
		Title:   "Test",
		Message: "Test message",
		Read:    false,
		ReadAt:  nil,
	}

	// Before marking as read
	assert.False(t, notification.Read)
	assert.Nil(t, notification.ReadAt)

	// Mark as read
	beforeMark := time.Now()
	notification.MarkAsRead()
	afterMark := time.Now()

	// After marking as read
	assert.True(t, notification.Read)
	assert.NotNil(t, notification.ReadAt)
	assert.True(t, notification.ReadAt.After(beforeMark) || notification.ReadAt.Equal(beforeMark))
	assert.True(t, notification.ReadAt.Before(afterMark) || notification.ReadAt.Equal(afterMark))
}

func TestNotification_MarkAsRead_Idempotent(t *testing.T) {
	// Setup
	notification := &Notification{
		ID:     "notif-1",
		UserID: "user-1",
		Type:   NotificationTypeInfo,
		Read:   false,
	}

	// Mark as read twice
	notification.MarkAsRead()
	firstReadAt := notification.ReadAt

	time.Sleep(10 * time.Millisecond)
	notification.MarkAsRead()
	secondReadAt := notification.ReadAt

	// Should update ReadAt on second call
	assert.NotEqual(t, firstReadAt, secondReadAt)
	assert.True(t, secondReadAt.After(*firstReadAt))
}

