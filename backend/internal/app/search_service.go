package app

import (
	"context"
	"log/slog"
	"strings"

	"github.com/lbrines/classsphere/internal/domain"
)

// SearchService handles multi-entity search operations.
type SearchService struct {
	// In real implementation, this would use repositories
	// For now, we use mock data for testing
}

// NewSearchService creates a new search service.
func NewSearchService() *SearchService {
	return &SearchService{}
}

// Search performs multi-entity search based on query parameters.
func (s *SearchService) Search(ctx context.Context, query domain.SearchQuery) (*domain.SearchResponse, error) {
	// Validate query
	if query.Query == "" {
		return &domain.SearchResponse{
			Query:   query.Query,
			Total:   0,
			Results: make(map[domain.SearchEntity][]domain.SearchResult),
		}, nil
	}

	// Set default limit if not specified
	if query.Limit == 0 {
		query.Limit = 10
	}

	response := &domain.SearchResponse{
		Query:   query.Query,
		Total:   0,
		Results: make(map[domain.SearchEntity][]domain.SearchResult),
	}

	// Search each requested entity type
	for _, entity := range query.Entities {
		if !entity.IsValid() {
			continue // Skip invalid entities
		}

		var results []domain.SearchResult

		switch entity {
		case domain.SearchEntityCourse:
			results = s.searchCourses(query)
		case domain.SearchEntityStudent:
			results = s.searchStudents(query)
		case domain.SearchEntityTeacher:
			results = s.searchTeachers(query)
		case domain.SearchEntityAssignment:
			results = s.searchAssignments(query)
		case domain.SearchEntityAnnouncement:
			results = s.searchAnnouncements(query)
		}

		// Apply role-based filtering
		results = s.filterByRole(results, query.Role)

		// Apply limit
		if len(results) > query.Limit {
			results = results[:query.Limit]
		}

		if len(results) > 0 {
			response.Results[entity] = results
			response.Total += len(results)
		}
	}

	return response, nil
}

// searchCourses searches for courses matching the query.
func (s *SearchService) searchCourses(query domain.SearchQuery) []domain.SearchResult {
	// Mock course data
	mockCourses := []struct {
		ID          string
		Name        string
		Description string
	}{
		{"course-1", "Mathematics 101", "Introduction to Algebra and Calculus"},
		{"course-2", "Physics 101", "Basic Physics Concepts"},
		{"course-3", "Advanced Mathematics", "Linear Algebra and Differential Equations"},
		{"course-4", "Computer Science 101", "Introduction to Programming"},
		{"course-5", "Biology 101", "Cellular and Molecular Biology"},
	}

	var results []domain.SearchResult
	queryLower := strings.ToLower(query.Query)

	for _, course := range mockCourses {
		nameLower := strings.ToLower(course.Name)
		descLower := strings.ToLower(course.Description)

		// Check if query matches name or description
		if strings.Contains(nameLower, queryLower) || strings.Contains(descLower, queryLower) {
			// Calculate relevance (simple: exact match in name = 1.0, partial = 0.5)
			relevance := 0.5
			if strings.Contains(nameLower, queryLower) && strings.HasPrefix(nameLower, queryLower) {
				relevance = 1.0
			} else if strings.Contains(nameLower, queryLower) {
				relevance = 0.8
			}

			results = append(results, domain.SearchResult{
				Type:        domain.SearchEntityCourse,
				ID:          course.ID,
				Title:       course.Name,
				Description: course.Description,
				Relevance:   relevance,
			})
		}
	}

	// Sort by relevance (descending)
	return sortByRelevance(results)
}

// searchStudents searches for students matching the query.
func (s *SearchService) searchStudents(query domain.SearchQuery) []domain.SearchResult {
	// Mock student data
	mockStudents := []struct {
		ID    string
		Name  string
		Email string
	}{
		{"student-1", "John Smith", "john.smith@student.edu"},
		{"student-2", "Jane Doe", "jane.doe@student.edu"},
		{"student-3", "Mike Johnson", "mike.j@student.edu"},
		{"student-4", "Sarah Williams", "s.williams@student.edu"},
	}

	var results []domain.SearchResult
	queryLower := strings.ToLower(query.Query)

	for _, student := range mockStudents {
		nameLower := strings.ToLower(student.Name)
		emailLower := strings.ToLower(student.Email)

		if strings.Contains(nameLower, queryLower) || strings.Contains(emailLower, queryLower) {
			relevance := 0.7
			if strings.HasPrefix(nameLower, queryLower) {
				relevance = 1.0
			}

			results = append(results, domain.SearchResult{
				Type:        domain.SearchEntityStudent,
				ID:          student.ID,
				Title:       student.Name,
				Description: student.Email,
				Relevance:   relevance,
			})
		}
	}

	return sortByRelevance(results)
}

// searchTeachers searches for teachers matching the query.
func (s *SearchService) searchTeachers(query domain.SearchQuery) []domain.SearchResult {
	// Mock teacher data
	mockTeachers := []struct {
		ID    string
		Name  string
		Email string
	}{
		{"teacher-1", "Prof. John Anderson", "j.anderson@faculty.edu"},
		{"teacher-2", "Dr. Emily Brown", "e.brown@faculty.edu"},
		{"teacher-3", "Prof. Michael Davis", "m.davis@faculty.edu"},
	}

	var results []domain.SearchResult
	queryLower := strings.ToLower(query.Query)

	for _, teacher := range mockTeachers {
		nameLower := strings.ToLower(teacher.Name)
		emailLower := strings.ToLower(teacher.Email)

		if strings.Contains(nameLower, queryLower) || strings.Contains(emailLower, queryLower) {
			relevance := 0.7
			if strings.HasPrefix(nameLower, queryLower) {
				relevance = 1.0
			}

			results = append(results, domain.SearchResult{
				Type:        domain.SearchEntityTeacher,
				ID:          teacher.ID,
				Title:       teacher.Name,
				Description: teacher.Email,
				Relevance:   relevance,
			})
		}
	}

	return sortByRelevance(results)
}

// searchAssignments searches for assignments matching the query.
func (s *SearchService) searchAssignments(query domain.SearchQuery) []domain.SearchResult {
	// Mock assignment data
	mockAssignments := []struct {
		ID          string
		Title       string
		Description string
		CourseID    string
	}{
		{"assignment-1", "Homework 1 - Algebra", "Solve equations 1-10", "course-1"},
		{"assignment-2", "Lab Report - Physics", "Complete lab experiment", "course-2"},
		{"assignment-3", "Final Project", "Build a calculator app", "course-4"},
	}

	var results []domain.SearchResult
	queryLower := strings.ToLower(query.Query)

	for _, assignment := range mockAssignments {
		titleLower := strings.ToLower(assignment.Title)
		descLower := strings.ToLower(assignment.Description)

		if strings.Contains(titleLower, queryLower) || strings.Contains(descLower, queryLower) {
			relevance := 0.6
			if strings.HasPrefix(titleLower, queryLower) {
				relevance = 1.0
			}

			results = append(results, domain.SearchResult{
				Type:        domain.SearchEntityAssignment,
				ID:          assignment.ID,
				Title:       assignment.Title,
				Description: assignment.Description,
				Meta: map[string]interface{}{
					"courseId": assignment.CourseID,
				},
				Relevance: relevance,
			})
		}
	}

	return sortByRelevance(results)
}

// searchAnnouncements searches for announcements matching the query.
func (s *SearchService) searchAnnouncements(query domain.SearchQuery) []domain.SearchResult {
	// Mock announcement data
	mockAnnouncements := []struct {
		ID      string
		Title   string
		Content string
	}{
		{"ann-1", "Class Canceled", "Tomorrow's class is canceled"},
		{"ann-2", "New Assignment Posted", "Check the assignments tab"},
		{"ann-3", "Exam Schedule", "Final exams start next week"},
	}

	var results []domain.SearchResult
	queryLower := strings.ToLower(query.Query)

	for _, ann := range mockAnnouncements {
		titleLower := strings.ToLower(ann.Title)
		contentLower := strings.ToLower(ann.Content)

		if strings.Contains(titleLower, queryLower) || strings.Contains(contentLower, queryLower) {
			relevance := 0.5
			if strings.HasPrefix(titleLower, queryLower) {
				relevance = 1.0
			}

			results = append(results, domain.SearchResult{
				Type:        domain.SearchEntityAnnouncement,
				ID:          ann.ID,
				Title:       ann.Title,
				Description: ann.Content,
				Relevance:   relevance,
			})
		}
	}

	return sortByRelevance(results)
}

// RBAC Permission Matrix for Search
// Defines which roles can see which entity types in search results
var searchPermissions = map[domain.Role]map[domain.SearchEntity]bool{
	domain.RoleAdmin: {
		domain.SearchEntityStudent:      true,  // Admins see everything
		domain.SearchEntityTeacher:      true,
		domain.SearchEntityCourse:       true,
		domain.SearchEntityAssignment:   true,
		domain.SearchEntityAnnouncement: true,
	},
	domain.RoleCoordinator: {
		domain.SearchEntityStudent:      false, // Privacy: coordinators don't see student details
		domain.SearchEntityTeacher:      true,  // Can see faculty
		domain.SearchEntityCourse:       true,  // Can see courses
		domain.SearchEntityAssignment:   true,  // Can see assignments
		domain.SearchEntityAnnouncement: true,  // Can see announcements
	},
	domain.RoleTeacher: {
		domain.SearchEntityStudent:      true,  // Teachers see their students
		domain.SearchEntityTeacher:      true,  // Can see colleagues
		domain.SearchEntityCourse:       true,  // Can see courses
		domain.SearchEntityAssignment:   true,  // Can see assignments
		domain.SearchEntityAnnouncement: true,  // Can see announcements
	},
	domain.RoleStudent: {
		domain.SearchEntityStudent:      false, // Privacy: students don't see other students
		domain.SearchEntityTeacher:      false, // Privacy: students don't see teacher directory
		domain.SearchEntityCourse:       true,  // Can see available courses
		domain.SearchEntityAssignment:   true,  // Can see their assignments
		domain.SearchEntityAnnouncement: true,  // Can see announcements
	},
}

// filterByRole filters results based on user role permissions.
// Implements RBAC (Role-Based Access Control) to prevent information disclosure.
func (s *SearchService) filterByRole(results []domain.SearchResult, role domain.Role) []domain.SearchResult {
	// Check if role exists in permission matrix
	_, exists := searchPermissions[role]
	if !exists {
		// If role not found in matrix, deny all (secure by default)
		slog.Warn("search RBAC: unknown role denied access",
			"role", role,
			"results_count", len(results))
		return []domain.SearchResult{}
	}

	// Filter results based on permissions
	filtered := make([]domain.SearchResult, 0, len(results))
	deniedCount := 0
	
	for _, result := range results {
		// Check if this role can see this entity type
		if s.canAccess(result.Type, role) {
			filtered = append(filtered, result)
		} else {
			deniedCount++
		}
	}

	// Log if any results were filtered for security audit
	if deniedCount > 0 {
		slog.Debug("search RBAC: results filtered by role",
			"role", role,
			"original_count", len(results),
			"filtered_count", len(filtered),
			"denied_count", deniedCount)
	}

	return filtered
}

// canAccess checks if a role can access a specific entity type in search.
// Returns false if the role or entity type is not found (secure by default).
func (s *SearchService) canAccess(entityType domain.SearchEntity, role domain.Role) bool {
	permissions, roleExists := searchPermissions[role]
	if !roleExists {
		return false
	}
	
	allowed, entityExists := permissions[entityType]
	return entityExists && allowed
}

// sortByRelevance sorts results by relevance score (descending).
func sortByRelevance(results []domain.SearchResult) []domain.SearchResult {
	// Simple bubble sort for relevance (good enough for mock data)
	n := len(results)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			if results[j].Relevance < results[j+1].Relevance {
				results[j], results[j+1] = results[j+1], results[j]
			}
		}
	}
	return results
}

