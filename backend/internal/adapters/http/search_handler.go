package http

import (
	"net/http"
	"strconv"
	"strings"

	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/domain"
)

// handleSearch performs multi-entity search.
func (h *Handler) handleSearch(c echo.Context) error {
	// Get query parameters
	query := c.QueryParam("q")
	entitiesParam := c.QueryParam("entities")
	limitParam := c.QueryParam("limit")
	
	// Validate required parameters
	if entitiesParam == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "entities parameter is required",
		})
	}
	
	// Parse entities
	entityStrings := strings.Split(entitiesParam, ",")
	entities := make([]domain.SearchEntity, 0, len(entityStrings))
	for _, e := range entityStrings {
		entities = append(entities, domain.SearchEntity(strings.TrimSpace(e)))
	}
	
	// Parse limit
	limit := 10 // default
	if limitParam != "" {
		if parsedLimit, err := strconv.Atoi(limitParam); err == nil && parsedLimit > 0 {
			limit = parsedLimit
		}
	}
	
	// Get user from context (set by AuthMiddleware)
	user, ok := c.Get("current_user").(domain.User)
	if !ok {
		return c.JSON(http.StatusUnauthorized, map[string]string{
			"error": "unauthorized",
		})
	}
	
	// Create search query
	searchQuery := domain.SearchQuery{
		Query:    query,
		Entities: entities,
		Role:     user.Role,
		UserID:   user.ID,
		Limit:    limit,
	}
	
	// Perform search
	response, err := h.searchService.Search(c.Request().Context(), searchQuery)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "search failed",
		})
	}
	
	return c.JSON(http.StatusOK, response)
}

