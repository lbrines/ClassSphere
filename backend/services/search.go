package services

import (
	"strings"
	"time"
)

// SearchService handles advanced search functionality
type SearchService struct{}

// NewSearchService creates a new search service
func NewSearchService() *SearchService {
	return &SearchService{}
}

// SearchFilters represents search criteria
type SearchFilters struct {
	Course     string  `json:"course"`
	Grade      string  `json:"grade"`
	DateFrom   string  `json:"date_from"`
	DateTo     string  `json:"date_to"`
	MinPoints  int     `json:"min_points"`
	MaxPoints  int     `json:"max_points"`
	State      string  `json:"state"`
}

// SearchResult represents a search result
type SearchResult struct {
	Type        string    `json:"type"`        // "student", "course", "assignment"
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Score       float64   `json:"score"`       // Relevance score
	Metadata    map[string]interface{} `json:"metadata"`
}

// SearchRequest represents a search request
type SearchRequest struct {
	Query   string        `json:"query"`
	Filters SearchFilters `json:"filters"`
	Limit   int           `json:"limit"`
	Offset  int           `json:"offset"`
}

// SearchResponse represents a search response
type SearchResponse struct {
	Results    []SearchResult `json:"results"`
	Total      int            `json:"total"`
	Query      string         `json:"query"`
	Filters    SearchFilters  `json:"filters"`
	SearchTime time.Duration  `json:"search_time"`
}

// SearchStudents searches for students with given criteria
func (s *SearchService) SearchStudents(query string, filters SearchFilters) []SearchResult {
	results := []SearchResult{}
	
	// Mock students data for search
	mockStudents := []Student{
		{ID: "1", Name: "John Doe", Email: "john@example.com"},
		{ID: "2", Name: "Jane Smith", Email: "jane@example.com"},
		{ID: "3", Name: "Bob Wilson", Email: "bob@example.com"},
		{ID: "4", Name: "Alice Brown", Email: "alice@example.com"},
		{ID: "5", Name: "Charlie Davis", Email: "charlie@example.com"},
	}
	
	// Filter by query
	for _, student := range mockStudents {
		matchesQuery := false
		if query == "" {
			matchesQuery = true
		} else {
			queryLower := strings.ToLower(query)
			nameLower := strings.ToLower(student.Name)
			emailLower := strings.ToLower(student.Email)
			
			// Exact word match for names (to avoid "john" matching "Johnson")
			nameWords := strings.Fields(nameLower)
			for _, word := range nameWords {
				if strings.HasPrefix(word, queryLower) {
					matchesQuery = true
					break
				}
			}
			
			// Full email match
			if !matchesQuery && strings.Contains(emailLower, queryLower) {
				matchesQuery = true
			}
		}
		
		if matchesQuery {
			
			score := s.calculateRelevanceScore(query, student.Name, student.Email)
			
			result := SearchResult{
				Type:        "student",
				ID:          student.ID,
				Title:       student.Name,
				Description: student.Email,
				Score:       score,
				Metadata: map[string]interface{}{
					"email": student.Email,
					"photo_url": student.PhotoURL,
				},
			}
			
			results = append(results, result)
		}
	}
	
	return results
}

// SearchCourses searches for courses with given criteria
func (s *SearchService) SearchCourses(query string, filters SearchFilters) []SearchResult {
	results := []SearchResult{}
	
	// Mock courses data for search
	mockCourses := []Course{
		{ID: "1", Name: "Mathematics 101", Description: "Basic mathematics course", Section: "A"},
		{ID: "2", Name: "Physics 201", Description: "Advanced physics course", Section: "B"},
		{ID: "3", Name: "Chemistry 101", Description: "Basic chemistry course", Section: "C"},
		{ID: "4", Name: "Biology 201", Description: "Advanced biology course", Section: "D"},
		{ID: "5", Name: "English Literature", Description: "Literature analysis course", Section: "E"},
	}
	
	// Filter by query and course filter
	for _, course := range mockCourses {
		matchesQuery := query == "" || strings.Contains(strings.ToLower(course.Name), strings.ToLower(query)) ||
			strings.Contains(strings.ToLower(course.Description), strings.ToLower(query))
		
		matchesCourseFilter := filters.Course == "" || strings.Contains(strings.ToLower(course.Name), strings.ToLower(filters.Course))
		
		if matchesQuery && matchesCourseFilter {
			score := s.calculateRelevanceScore(query, course.Name, course.Description)
			
			result := SearchResult{
				Type:        "course",
				ID:          course.ID,
				Title:       course.Name,
				Description: course.Description,
				Score:       score,
				Metadata: map[string]interface{}{
					"section": course.Section,
					"room": course.Room,
					"state": course.CourseState,
				},
			}
			
			results = append(results, result)
		}
	}
	
	return results
}

// SearchAssignments searches for assignments with given criteria
func (s *SearchService) SearchAssignments(query string, filters SearchFilters) []SearchResult {
	results := []SearchResult{}
	
	// Mock assignments data for search
	mockAssignments := []Assignment{
		{ID: "1", Title: "Math Homework 1", Description: "Basic algebra problems", MaxPoints: 100, State: "PUBLISHED"},
		{ID: "2", Title: "Physics Lab Report", Description: "Lab experiment analysis", MaxPoints: 150, State: "DRAFT"},
		{ID: "3", Title: "Chemistry Quiz", Description: "Periodic table quiz", MaxPoints: 50, State: "PUBLISHED"},
		{ID: "4", Title: "Biology Essay", Description: "Evolution essay", MaxPoints: 200, State: "PUBLISHED"},
		{ID: "5", Title: "English Reading", Description: "Shakespeare analysis", MaxPoints: 75, State: "DRAFT"},
	}
	
	// Filter by query and various filters
	for _, assignment := range mockAssignments {
		matchesQuery := query == "" || strings.Contains(strings.ToLower(assignment.Title), strings.ToLower(query)) ||
			strings.Contains(strings.ToLower(assignment.Description), strings.ToLower(query))
		
		matchesPointsFilter := (filters.MinPoints == 0 || assignment.MaxPoints >= filters.MinPoints) &&
			(filters.MaxPoints == 0 || assignment.MaxPoints <= filters.MaxPoints)
		
		matchesStateFilter := filters.State == "" || assignment.State == filters.State
		
		if matchesQuery && matchesPointsFilter && matchesStateFilter {
			score := s.calculateRelevanceScore(query, assignment.Title, assignment.Description)
			
			result := SearchResult{
				Type:        "assignment",
				ID:          assignment.ID,
				Title:       assignment.Title,
				Description: assignment.Description,
				Score:       score,
				Metadata: map[string]interface{}{
					"max_points": assignment.MaxPoints,
					"state": assignment.State,
					"due_date": assignment.DueDate,
				},
			}
			
			results = append(results, result)
		}
	}
	
	return results
}

// SearchAll performs a comprehensive search across all entities
func (s *SearchService) SearchAll(request SearchRequest) SearchResponse {
	startTime := time.Now()
	
	// Search all entity types
	studentResults := s.SearchStudents(request.Query, request.Filters)
	courseResults := s.SearchCourses(request.Query, request.Filters)
	assignmentResults := s.SearchAssignments(request.Query, request.Filters)
	
	// Combine results
	allResults := append(studentResults, courseResults...)
	allResults = append(allResults, assignmentResults...)
	
	// Sort by relevance score (highest first)
	s.sortByRelevance(allResults)
	
	// Apply pagination
	total := len(allResults)
	start := request.Offset
	end := start + request.Limit
	
	if end > total {
		end = total
	}
	
	if start > total {
		start = total
	}
	
	var paginatedResults []SearchResult
	if start < total {
		paginatedResults = allResults[start:end]
	}
	
	searchTime := time.Since(startTime)
	
	return SearchResponse{
		Results:    paginatedResults,
		Total:      total,
		Query:      request.Query,
		Filters:    request.Filters,
		SearchTime: searchTime,
	}
}

// calculateRelevanceScore calculates relevance score for search results
func (s *SearchService) calculateRelevanceScore(query, title, description string) float64 {
	if query == "" {
		return 1.0
	}
	
	query = strings.ToLower(query)
	title = strings.ToLower(title)
	description = strings.ToLower(description)
	
	score := 0.0
	
	// Exact title match gets highest score
	if strings.Contains(title, query) {
		score += 0.8
	}
	
	// Partial title match
	if strings.Contains(title, query) {
		score += 0.6
	}
	
	// Description match
	if strings.Contains(description, query) {
		score += 0.4
	}
	
	// Word boundary matches get bonus
	words := strings.Fields(query)
	for _, word := range words {
		if strings.Contains(title, word) {
			score += 0.2
		}
		if strings.Contains(description, word) {
			score += 0.1
		}
	}
	
	// Normalize score to 0-1 range
	if score > 1.0 {
		score = 1.0
	}
	
	return score
}

// sortByRelevance sorts results by relevance score (highest first)
func (s *SearchService) sortByRelevance(results []SearchResult) {
	for i := 0; i < len(results)-1; i++ {
		for j := i + 1; j < len(results); j++ {
			if results[i].Score < results[j].Score {
				results[i], results[j] = results[j], results[i]
			}
		}
	}
}
