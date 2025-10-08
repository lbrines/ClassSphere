package http

import (
	"net/http"
	"strconv"
	"strings"

	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/domain"
)

// handleSearch performs multi-entity search with pagination support.
func (h *Handler) handleSearch(c echo.Context) error {
	// Get query parameters
	query := c.QueryParam("q")
	entitiesParam := c.QueryParam("entities")
	limitParam := c.QueryParam("limit")
	pageParam := c.QueryParam("page")
	
	// Validate required parameters
	if entitiesParam == "" {
		return ErrBadRequest("entities parameter is required")
	}
	
	// Parse entities
	entityStrings := strings.Split(entitiesParam, ",")
	entities := make([]domain.SearchEntity, 0, len(entityStrings))
	for _, e := range entityStrings {
		entities = append(entities, domain.SearchEntity(strings.TrimSpace(e)))
	}
	
	// Parse limit (page size)
	limit := 10 // default
	if limitParam != "" {
		if parsedLimit, err := strconv.Atoi(limitParam); err == nil && parsedLimit > 0 {
			limit = parsedLimit
		}
	}
	
	// Parse page (1-indexed)
	page := 1 // default
	if pageParam != "" {
		if parsedPage, err := strconv.Atoi(pageParam); err == nil && parsedPage > 0 {
			page = parsedPage
		}
	}
	
	// Get user from context (set by AuthMiddleware)
	user, ok := c.Get("current_user").(domain.User)
	if !ok {
		return ErrUnauthorized("authentication required")
	}
	
	// Create search query with pagination
	searchQuery := domain.SearchQuery{
		Query:    query,
		Entities: entities,
		Role:     user.Role,
		UserID:   user.ID,
		Limit:    limit,
		Page:     page,
	}
	
	// Perform search
	response, err := h.searchService.Search(c.Request().Context(), searchQuery)
	if err != nil {
		return ErrInternal("search failed", err)
	}
	
	return c.JSON(http.StatusOK, response)
}

