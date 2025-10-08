package app

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/lbrines/classsphere/internal/domain"
)

func TestNotificationHub_NewHub(t *testing.T) {
	hub := NewNotificationHub()
	
	assert.NotNil(t, hub)
	assert.Equal(t, 0, hub.ClientCount())
}

func TestNotificationHub_RegisterClient(t *testing.T) {
	hub := NewNotificationHub()
	
	// Register client
	clientID := hub.RegisterClient("user-1")
	
	assert.NotEmpty(t, clientID)
	assert.Equal(t, 1, hub.ClientCount())
}

func TestNotificationHub_UnregisterClient(t *testing.T) {
	hub := NewNotificationHub()
	
	// Register and unregister
	clientID := hub.RegisterClient("user-1")
	assert.Equal(t, 1, hub.ClientCount())
	
	hub.UnregisterClient(clientID)
	assert.Equal(t, 0, hub.ClientCount())
}

func TestNotificationHub_Broadcast(t *testing.T) {
	hub := NewNotificationHub()
	
	// Register clients
	client1ID := hub.RegisterClient("user-1")
	client2ID := hub.RegisterClient("user-2")
	
	// Subscribe to messages
	messages1 := make(chan domain.Notification, 10)
	messages2 := make(chan domain.Notification, 10)
	
	hub.Subscribe(client1ID, messages1)
	hub.Subscribe(client2ID, messages2)
	
	// Broadcast
	notification := domain.Notification{
		ID:      "broadcast-1",
		Type:    domain.NotificationTypeInfo,
		Title:   "Test Broadcast",
		Message: "To all users",
	}
	
	hub.Broadcast(notification)
	
	// Both clients should receive
	select {
	case msg := <-messages1:
		assert.Equal(t, "broadcast-1", msg.ID)
	case <-time.After(1 * time.Second):
		t.Fatal("Client 1 did not receive broadcast")
	}
	
	select {
	case msg := <-messages2:
		assert.Equal(t, "broadcast-1", msg.ID)
	case <-time.After(1 * time.Second):
		t.Fatal("Client 2 did not receive broadcast")
	}
}

func TestNotificationHub_SendToUser(t *testing.T) {
	hub := NewNotificationHub()
	
	// Register 2 users
	client1ID := hub.RegisterClient("user-1")
	client2ID := hub.RegisterClient("user-2")
	
	messages1 := make(chan domain.Notification, 10)
	messages2 := make(chan domain.Notification, 10)
	
	hub.Subscribe(client1ID, messages1)
	hub.Subscribe(client2ID, messages2)
	
	// Send to user-1 only
	notification := domain.Notification{
		ID:      "user-specific-1",
		UserID:  "user-1",
		Type:    domain.NotificationTypeInfo,
		Title:   "For User 1",
		Message: "Private message",
	}
	
	hub.SendToUser("user-1", notification)
	
	// User-1 receives
	select {
	case msg := <-messages1:
		assert.Equal(t, "user-specific-1", msg.ID)
	case <-time.After(1 * time.Second):
		t.Fatal("User 1 did not receive notification")
	}
	
	// User-2 should NOT receive
	select {
	case <-messages2:
		t.Fatal("User 2 should not have received the notification")
	case <-time.After(200 * time.Millisecond):
		// Expected timeout
	}
}

func TestNotificationHub_MultipleClientsPerUser(t *testing.T) {
	hub := NewNotificationHub()
	
	// Same user with 2 clients (e.g., mobile + desktop)
	client1ID := hub.RegisterClient("user-1")
	client2ID := hub.RegisterClient("user-1")
	
	messages1 := make(chan domain.Notification, 10)
	messages2 := make(chan domain.Notification, 10)
	
	hub.Subscribe(client1ID, messages1)
	hub.Subscribe(client2ID, messages2)
	
	// Send to user-1
	notification := domain.Notification{
		ID:      "multi-client-1",
		UserID:  "user-1",
		Type:    domain.NotificationTypeInfo,
		Title:   "Test",
		Message: "Should reach both clients",
	}
	
	hub.SendToUser("user-1", notification)
	
	// Both clients of user-1 should receive
	receivedCount := 0
	for i := 0; i < 2; i++ {
		select {
		case <-messages1:
			receivedCount++
		case <-messages2:
			receivedCount++
		case <-time.After(1 * time.Second):
			t.Fatal("Not all clients received the notification")
		}
	}
	
	assert.Equal(t, 2, receivedCount)
}

func TestNotificationHub_UnsubscribeStopsMessages(t *testing.T) {
	hub := NewNotificationHub()
	
	// Register and subscribe
	clientID := hub.RegisterClient("user-1")
	messages := make(chan domain.Notification, 10)
	hub.Subscribe(clientID, messages)
	
	// Unsubscribe
	hub.Unsubscribe(clientID)
	
	// Send notification
	notification := domain.Notification{
		ID:     "test-1",
		UserID: "user-1",
	}
	
	hub.SendToUser("user-1", notification)
	
	// Should NOT receive (unsubscribed)
	select {
	case <-messages:
		t.Fatal("Should not receive after unsubscribe")
	case <-time.After(200 * time.Millisecond):
		// Expected
	}
}

