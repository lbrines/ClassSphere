package http

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/gorilla/websocket"
	echo "github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
)

// TestWebSocketHandler_Upgrade tests WebSocket connection upgrade
func TestWebSocketHandler_Upgrade(t *testing.T) {
	// Setup
	e := echo.New()
	hub := app.NewNotificationHub()
	handler := &Handler{
		notificationHub: hub,
	}
	
	e.GET("/ws", handler.handleWebSocket)
	
	// Start server
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect via WebSocket
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws"
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, nil)
	
	// Assert
	require.NoError(t, err)
	assert.Equal(t, http.StatusSwitchingProtocols, resp.StatusCode)
	assert.NotNil(t, ws)
	
	// Cleanup
	ws.Close()
}

// TestWebSocketHandler_BroadcastMessage tests broadcasting to connected clients
func TestWebSocketHandler_BroadcastMessage(t *testing.T) {
	// Setup
	hub := app.NewNotificationHub()
	e := echo.New()
	handler := &Handler{
		notificationHub: hub,
	}
	
	e.GET("/ws", handler.handleWebSocket)
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect client
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws"
	ws, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
	require.NoError(t, err)
	defer ws.Close()
	
	// Wait for connection to be registered
	time.Sleep(100 * time.Millisecond)
	
	// Broadcast notification
	notification := domain.Notification{
		ID:      "notif-1",
		UserID:  "user-1",
		Type:    "info",
		Title:   "Test Notification",
		Message: "This is a test",
	}
	
	hub.Broadcast(notification)
	
	// Read message from WebSocket
	ws.SetReadDeadline(time.Now().Add(2 * time.Second))
	var received domain.Notification
	err = ws.ReadJSON(&received)
	
	// Assert
	require.NoError(t, err)
	assert.Equal(t, "notif-1", received.ID)
	assert.Equal(t, "Test Notification", received.Title)
}

// TestWebSocketHandler_DisconnectCleanup tests connection cleanup on disconnect
func TestWebSocketHandler_DisconnectCleanup(t *testing.T) {
	// Setup
	hub := app.NewNotificationHub()
	e := echo.New()
	handler := &Handler{
		notificationHub: hub,
	}
	
	e.GET("/ws", handler.handleWebSocket)
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect and disconnect
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws"
	ws, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
	require.NoError(t, err)
	
	// Wait for registration
	time.Sleep(100 * time.Millisecond)
	initialClients := hub.ClientCount()
	
	// Disconnect
	ws.Close()
	time.Sleep(100 * time.Millisecond)
	
	// Assert cleanup
	assert.Equal(t, initialClients-1, hub.ClientCount())
}

// TestWebSocketHandler_MultipleClients tests multiple concurrent connections
func TestWebSocketHandler_MultipleClients(t *testing.T) {
	// Setup
	hub := app.NewNotificationHub()
	e := echo.New()
	handler := &Handler{
		notificationHub: hub,
	}
	
	e.GET("/ws", handler.handleWebSocket)
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect 3 clients
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws"
	clients := make([]*websocket.Conn, 3)
	
	for i := 0; i < 3; i++ {
		ws, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
		require.NoError(t, err)
		clients[i] = ws
		defer ws.Close()
	}
	
	time.Sleep(100 * time.Millisecond)
	
	// Broadcast to all
	notification := domain.Notification{
		ID:      "broadcast-1",
		Title:   "Broadcast Test",
		Message: "To all clients",
	}
	
	hub.Broadcast(notification)
	
	// All clients should receive
	for i, client := range clients {
		client.SetReadDeadline(time.Now().Add(2 * time.Second))
		var received domain.Notification
		err := client.ReadJSON(&received)
		
		require.NoError(t, err, "Client %d should receive message", i)
		assert.Equal(t, "broadcast-1", received.ID)
	}
}

// TestWebSocketHandler_UserSpecificNotification tests user-specific message delivery
func TestWebSocketHandler_UserSpecificNotification(t *testing.T) {
	// Setup
	hub := app.NewNotificationHub()
	e := echo.New()
	handler := &Handler{
		notificationHub: hub,
	}
	
	e.GET("/ws", handler.handleWebSocket)
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect 2 users
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws?userId=user-1"
	ws1, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
	require.NoError(t, err)
	defer ws1.Close()
	
	wsURL2 := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws?userId=user-2"
	ws2, _, err := websocket.DefaultDialer.Dial(wsURL2, nil)
	require.NoError(t, err)
	defer ws2.Close()
	
	time.Sleep(100 * time.Millisecond)
	
	// Send to user-1 only
	notification := domain.Notification{
		ID:      "user-specific-1",
		UserID:  "user-1",
		Title:   "For User 1",
		Message: "Private message",
	}
	
	hub.SendToUser("user-1", notification)
	
	// User-1 receives
	ws1.SetReadDeadline(time.Now().Add(2 * time.Second))
	var received domain.Notification
	err = ws1.ReadJSON(&received)
	require.NoError(t, err)
	assert.Equal(t, "user-specific-1", received.ID)
	
	// User-2 should NOT receive (timeout expected)
	ws2.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
	var shouldTimeout domain.Notification
	err = ws2.ReadJSON(&shouldTimeout)
	assert.Error(t, err) // Timeout error expected
}

