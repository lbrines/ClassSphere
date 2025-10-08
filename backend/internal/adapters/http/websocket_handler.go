package http

import (
	"log/slog"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/domain"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		// In production, check origin properly
		return true
	},
}

const (
	writeWait      = 10 * time.Second
	pongWait       = 60 * time.Second
	pingPeriod     = (pongWait * 9) / 10
	maxMessageSize = 512
)

// handleWebSocket upgrades HTTP connection to WebSocket and handles messages.
// Requires JWT authentication via AuthMiddleware to extract authenticated user.
func (h *Handler) handleWebSocket(c echo.Context) error {
	// Extract authenticated user from context (set by AuthMiddleware)
	user := CurrentUser(c)
	if user.ID == "" {
		slog.Warn("WebSocket connection attempt without authenticated user")
		return echo.NewHTTPError(http.StatusUnauthorized, "unauthorized: missing user context")
	}

	// Upgrade connection
	ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
	if err != nil {
		slog.Error("WebSocket upgrade failed", 
			"error", err,
			"userID", user.ID,
			"role", user.Role)
		return err
	}
	defer ws.Close()

	slog.Info("WebSocket client connecting",
		"userID", user.ID,
		"role", user.Role,
		"email", user.Email)

	// Register client with authenticated user ID
	clientID := h.notificationHub.RegisterClient(user.ID)
	defer h.notificationHub.UnregisterClient(clientID)

	// Create message channel
	messages := make(chan domain.Notification, 100)
	h.notificationHub.Subscribe(clientID, messages)
	defer h.notificationHub.Unsubscribe(clientID)

	// Configure WebSocket
	ws.SetReadLimit(maxMessageSize)
	ws.SetReadDeadline(time.Now().Add(pongWait))
	ws.SetPongHandler(func(string) error {
		ws.SetReadDeadline(time.Now().Add(pongWait))
		return nil
	})

	// Start goroutines for read/write
	done := make(chan struct{})
	go h.writePump(ws, messages, done)
	go h.readPump(ws, done)

	// Wait for connection to close
	<-done

	slog.Info("WebSocket client disconnected",
		"userID", user.ID,
		"clientID", clientID)

	return nil
}

// readPump pumps messages from the WebSocket connection.
func (h *Handler) readPump(ws *websocket.Conn, done chan struct{}) {
	defer close(done)

	for {
		_, _, err := ws.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				slog.Error("WebSocket read error", "error", err)
			}
			break
		}
		// For now, we only send from server to client
		// Future: handle client messages here
	}
}

// writePump pumps messages from the hub to the WebSocket connection.
func (h *Handler) writePump(ws *websocket.Conn, messages chan domain.Notification, done chan struct{}) {
	ticker := time.NewTicker(pingPeriod)
	defer ticker.Stop()

	for {
		select {
		case notification, ok := <-messages:
			if !ok {
				// Channel closed
				ws.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}

			ws.SetWriteDeadline(time.Now().Add(writeWait))
			if err := ws.WriteJSON(notification); err != nil {
				slog.Error("WebSocket write error", "error", err)
				return
			}

		case <-ticker.C:
			ws.SetWriteDeadline(time.Now().Add(writeWait))
			if err := ws.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}

		case <-done:
			return
		}
	}
}

