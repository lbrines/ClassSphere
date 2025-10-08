package app

import (
	"sync"

	"github.com/google/uuid"
	"github.com/lbrines/classsphere/internal/domain"
)

// NotificationHub manages WebSocket connections and message broadcasting.
type NotificationHub struct {
	mu      sync.RWMutex
	clients map[string]*client // clientID → client
	users   map[string][]string // userID → []clientID
}

type client struct {
	id       string
	userID   string
	messages chan domain.Notification
}

// NewNotificationHub creates a new notification hub.
func NewNotificationHub() *NotificationHub {
	return &NotificationHub{
		clients: make(map[string]*client),
		users:   make(map[string][]string),
	}
}

// RegisterClient registers a new client connection for a user.
func (h *NotificationHub) RegisterClient(userID string) string {
	h.mu.Lock()
	defer h.mu.Unlock()

	clientID := uuid.New().String()
	
	c := &client{
		id:       clientID,
		userID:   userID,
		messages: make(chan domain.Notification, 100),
	}

	h.clients[clientID] = c
	h.users[userID] = append(h.users[userID], clientID)

	return clientID
}

// UnregisterClient removes a client connection.
func (h *NotificationHub) UnregisterClient(clientID string) {
	h.mu.Lock()
	defer h.mu.Unlock()

	c, exists := h.clients[clientID]
	if !exists {
		return
	}

	// Remove from clients map
	delete(h.clients, clientID)

	// Remove from users map
	userClients := h.users[c.userID]
	for i, id := range userClients {
		if id == clientID {
			h.users[c.userID] = append(userClients[:i], userClients[i+1:]...)
			break
		}
	}

	// Clean up empty user entries
	if len(h.users[c.userID]) == 0 {
		delete(h.users, c.userID)
	}

	// Close channel if it exists and wasn't replaced by Subscribe
	if c.messages != nil {
		close(c.messages)
	}
}

// Subscribe provides the message channel for a client.
func (h *NotificationHub) Subscribe(clientID string, messages chan domain.Notification) {
	h.mu.Lock()
	defer h.mu.Unlock()

	if c, exists := h.clients[clientID]; exists {
		c.messages = messages
	}
}

// Unsubscribe stops sending messages to a client.
func (h *NotificationHub) Unsubscribe(clientID string) {
	h.mu.Lock()
	defer h.mu.Unlock()

	if c, exists := h.clients[clientID]; exists {
		// Don't close channel, just nil it to stop sending
		c.messages = nil
	}
}

// Broadcast sends a notification to all connected clients.
func (h *NotificationHub) Broadcast(notification domain.Notification) {
	h.mu.RLock()
	defer h.mu.RUnlock()

	for _, c := range h.clients {
		if c.messages != nil {
			select {
			case c.messages <- notification:
				// Sent successfully
			default:
				// Channel full, skip (prevents blocking)
			}
		}
	}
}

// SendToUser sends a notification to all clients of a specific user.
func (h *NotificationHub) SendToUser(userID string, notification domain.Notification) {
	h.mu.RLock()
	defer h.mu.RUnlock()

	clientIDs, exists := h.users[userID]
	if !exists {
		return // User not connected
	}

	for _, clientID := range clientIDs {
		c, exists := h.clients[clientID]
		if exists && c.messages != nil {
			select {
			case c.messages <- notification:
				// Sent successfully
			default:
				// Channel full, skip
			}
		}
	}
}

// ClientCount returns the number of connected clients.
func (h *NotificationHub) ClientCount() int {
	h.mu.RLock()
	defer h.mu.RUnlock()
	return len(h.clients)
}

// UserCount returns the number of unique users connected.
func (h *NotificationHub) UserCount() int {
	h.mu.RLock()
	defer h.mu.RUnlock()
	return len(h.users)
}

