package http

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"net/http"
	"time"

	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/domain"
)

const (
	// SSE configuration
	sseKeepAliveInterval = 15 * time.Second // Send keep-alive every 15 seconds
	sseWriteTimeout      = 10 * time.Second // Timeout for writing to client
	sseFlushInterval     = 100 * time.Millisecond // Flush buffer frequently
)

// handleSSE handles Server-Sent Events for real-time notifications.
// Requires JWT authentication via AuthMiddleware to extract authenticated user.
//
// SSE is simpler than WebSocket for unidirectional server-to-client communication:
// - Uses standard HTTP (better proxy/firewall compatibility)
// - Automatic reconnection by browser
// - Text-based protocol (easier debugging)
// - No ping/pong mechanism needed
func (h *Handler) handleSSE(c echo.Context) error {
	// Extract authenticated user from context (set by AuthMiddleware)
	user := CurrentUser(c)
	if user.ID == "" {
		slog.Warn("SSE connection attempt without authenticated user")
		return ErrUnauthorized("authentication required")
	}

	// Get the response writer
	w := c.Response().Writer
	
	// Set SSE headers
	c.Response().Header().Set("Content-Type", "text/event-stream")
	c.Response().Header().Set("Cache-Control", "no-cache")
	c.Response().Header().Set("Connection", "keep-alive")
	c.Response().Header().Set("X-Accel-Buffering", "no") // Disable nginx buffering
	
	// Write headers immediately
	c.Response().WriteHeader(http.StatusOK)
	if f, ok := w.(http.Flusher); ok {
		f.Flush()
	}

	slog.Info("SSE client connecting",
		"userID", user.ID,
		"role", user.Role,
		"email", user.Email)

	// Register client with notification hub
	clientID := h.notificationHub.RegisterClient(user.ID)
	defer h.notificationHub.UnregisterClient(clientID)

	// Create message channel
	messages := make(chan domain.Notification, 100)
	h.notificationHub.Subscribe(clientID, messages)
	defer h.notificationHub.Unsubscribe(clientID)

	// Create context with cancellation
	ctx, cancel := context.WithCancel(c.Request().Context())
	defer cancel()

	// Send initial connection success message
	if err := h.sendSSEEvent(w, "connected", map[string]string{
		"clientId": clientID,
		"userId":   user.ID,
	}); err != nil {
		slog.Error("SSE failed to send initial message", "error", err)
		return err
	}

	// Create ticker for keep-alive messages
	keepAliveTicker := time.NewTicker(sseKeepAliveInterval)
	defer keepAliveTicker.Stop()

	// Event loop
	for {
		select {
		case <-ctx.Done():
			// Client disconnected
			slog.Info("SSE client disconnected (context done)",
				"userID", user.ID,
				"clientID", clientID)
			return nil

		case notification, ok := <-messages:
			if !ok {
				// Channel closed
				slog.Info("SSE messages channel closed",
					"userID", user.ID,
					"clientID", clientID)
				return nil
			}

			// Send notification to client
			if err := h.sendSSENotification(w, notification); err != nil {
				slog.Error("SSE failed to send notification",
					"error", err,
					"userID", user.ID,
					"clientID", clientID)
				return err
			}

		case <-keepAliveTicker.C:
			// Send keep-alive comment to prevent timeout
			if err := h.sendSSEKeepAlive(w); err != nil {
				slog.Debug("SSE keep-alive failed (client likely disconnected)",
					"error", err,
					"userID", user.ID,
					"clientID", clientID)
				return err
			}
		}
	}
}

// sendSSEEvent sends a Server-Sent Event with the specified event type and data.
func (h *Handler) sendSSEEvent(w http.ResponseWriter, eventType string, data interface{}) error {
	// Marshal data to JSON
	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("marshal SSE data: %w", err)
	}

	// Write SSE format: event: type\ndata: json\n\n
	_, err = fmt.Fprintf(w, "event: %s\ndata: %s\n\n", eventType, jsonData)
	if err != nil {
		return fmt.Errorf("write SSE event: %w", err)
	}

	// Flush immediately
	if f, ok := w.(http.Flusher); ok {
		f.Flush()
	}

	return nil
}

// sendSSENotification sends a notification as an SSE event.
func (h *Handler) sendSSENotification(w http.ResponseWriter, notification domain.Notification) error {
	return h.sendSSEEvent(w, "notification", notification)
}

// sendSSEKeepAlive sends a keep-alive comment to prevent connection timeout.
// SSE comments start with ":" and are ignored by the client.
func (h *Handler) sendSSEKeepAlive(w http.ResponseWriter) error {
	_, err := fmt.Fprintf(w, ": keep-alive %s\n\n", time.Now().Format(time.RFC3339))
	if err != nil {
		return fmt.Errorf("write SSE keep-alive: %w", err)
	}

	// Flush immediately
	if f, ok := w.(http.Flusher); ok {
		f.Flush()
	}

	return nil
}

