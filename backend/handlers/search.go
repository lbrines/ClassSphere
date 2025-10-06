package handlers

import (
	"net/http"
	"strconv"

	"classsphere-backend/auth"
	"classsphere-backend/services"

	"github.com/labstack/echo/v4"
)

// SearchHandler handles search-related requests
type SearchHandler struct {
	userRepo      UserRepository
	searchService SearchService
}

// SearchService interface for dependency injection
type SearchService interface {
	SearchStudents(query string, filters services.SearchFilters) []services.SearchResult
	SearchCourses(query string, filters services.SearchFilters) []services.SearchResult
	SearchAssignments(query string, filters services.SearchFilters) []services.SearchResult
	SearchAll(request services.SearchRequest) services.SearchResponse
}


// NewSearchHandler creates a new search handler
func NewSearchHandler(userRepo UserRepository, searchService SearchService) *SearchHandler {
	return &SearchHandler{
		userRepo:      userRepo,
		searchService: searchService,
	}
}

// SearchRequest represents the search request payload
type SearchRequest struct {
	Query   string                `json:"query"`
	Filters services.SearchFilters `json:"filters"`
	Limit   int                   `json:"limit"`
	Offset  int                   `json:"offset"`
}

// SearchResponse represents the search response
type SearchResponse struct {
	Results    []services.SearchResult `json:"results"`
	Total      int                     `json:"total"`
	Query      string                  `json:"query"`
	Filters    services.SearchFilters  `json:"filters"`
	SearchTime string                  `json:"search_time"`
}

// SearchErrorResponse represents an error response for search
type SearchErrorResponse struct {
	Error string `json:"error"`
}

// SearchAll performs a comprehensive search across all entities
func (h *SearchHandler) SearchAll(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid user ID"})
	}
	
	// Get user info
	_, err = h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, SearchErrorResponse{Error: "User not found"})
	}

	// Parse request
	var req SearchRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid request format"})
	}

	// Set default values
	if req.Limit <= 0 {
		req.Limit = 10
	}
	if req.Limit > 100 {
		req.Limit = 100 // Max limit
	}
	if req.Offset < 0 {
		req.Offset = 0
	}

	// Convert to service request
	serviceRequest := services.SearchRequest{
		Query:   req.Query,
		Filters: req.Filters,
		Limit:   req.Limit,
		Offset:  req.Offset,
	}

	// Perform search
	serviceResponse := h.searchService.SearchAll(serviceRequest)

	// Convert to handler response
	response := SearchResponse{
		Results:    serviceResponse.Results,
		Total:      serviceResponse.Total,
		Query:      serviceResponse.Query,
		Filters:    serviceResponse.Filters,
		SearchTime: serviceResponse.SearchTime.String(),
	}

	return c.JSON(http.StatusOK, response)
}

// SearchStudents searches for students
func (h *SearchHandler) SearchStudents(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid user ID"})
	}
	
	// Get user info
	_, err = h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, SearchErrorResponse{Error: "User not found"})
	}

	// Get query parameters
	query := c.QueryParam("q")
	filters := services.SearchFilters{
		Course: c.QueryParam("course"),
		Grade:  c.QueryParam("grade"),
		State:  c.QueryParam("state"),
	}

	// Perform search
	results := h.searchService.SearchStudents(query, filters)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"results": results,
		"total":   len(results),
		"query":   query,
		"filters": filters,
	})
}

// SearchCourses searches for courses
func (h *SearchHandler) SearchCourses(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid user ID"})
	}
	
	// Get user info
	_, err = h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, SearchErrorResponse{Error: "User not found"})
	}

	// Get query parameters
	query := c.QueryParam("q")
	filters := services.SearchFilters{
		Course: c.QueryParam("course"),
		State:  c.QueryParam("state"),
	}

	// Perform search
	results := h.searchService.SearchCourses(query, filters)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"results": results,
		"total":   len(results),
		"query":   query,
		"filters": filters,
	})
}

// SearchAssignments searches for assignments
func (h *SearchHandler) SearchAssignments(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid user ID"})
	}
	
	// Get user info
	_, err = h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, SearchErrorResponse{Error: "User not found"})
	}

	// Get query parameters
	query := c.QueryParam("q")
	
	// Parse numeric filters
	minPoints := 0
	maxPoints := 0
	if minPointsStr := c.QueryParam("min_points"); minPointsStr != "" {
		if parsed, err := strconv.Atoi(minPointsStr); err == nil {
			minPoints = parsed
		}
	}
	if maxPointsStr := c.QueryParam("max_points"); maxPointsStr != "" {
		if parsed, err := strconv.Atoi(maxPointsStr); err == nil {
			maxPoints = parsed
		}
	}

	filters := services.SearchFilters{
		Course:    c.QueryParam("course"),
		MinPoints: minPoints,
		MaxPoints: maxPoints,
		State:     c.QueryParam("state"),
	}

	// Perform search
	results := h.searchService.SearchAssignments(query, filters)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"results": results,
		"total":   len(results),
		"query":   query,
		"filters": filters,
	})
}

// GetSearchSuggestions returns search suggestions based on query
func (h *SearchHandler) GetSearchSuggestions(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, SearchErrorResponse{Error: "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, SearchErrorResponse{Error: "Invalid user ID"})
	}
	
	// Get user info
	_, err = h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, SearchErrorResponse{Error: "User not found"})
	}

	// Get query parameter
	query := c.QueryParam("q")
	if len(query) < 2 {
		return c.JSON(http.StatusOK, map[string]interface{}{
			"suggestions": []string{},
		})
	}

	// Get suggestions from all search types
	studentResults := h.searchService.SearchStudents(query, services.SearchFilters{})
	courseResults := h.searchService.SearchCourses(query, services.SearchFilters{})
	assignmentResults := h.searchService.SearchAssignments(query, services.SearchFilters{})

	// Build suggestions list
	suggestions := []string{}
	
	// Add student names
	for _, result := range studentResults {
		if len(suggestions) < 5 {
			suggestions = append(suggestions, result.Title)
		}
	}
	
	// Add course names
	for _, result := range courseResults {
		if len(suggestions) < 5 {
			suggestions = append(suggestions, result.Title)
		}
	}
	
	// Add assignment titles
	for _, result := range assignmentResults {
		if len(suggestions) < 5 {
			suggestions = append(suggestions, result.Title)
		}
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"suggestions": suggestions,
		"query":       query,
	})
}
