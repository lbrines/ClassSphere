package app

import (
	"context"
	"log/slog"
	"strings"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
)

// SearchService handles multi-entity search operations.
// It can use a real repository (e.g., Google Classroom API) or fallback to mock data.
type SearchService struct {
	repository ports.SearchRepository // Optional: Google Classroom repository
	cache      ports.Cache             // Optional: Cache for performance
}

// NewSearchService creates a new search service with mock data.
func NewSearchService() *SearchService {
	return &SearchService{
		repository: nil, // No repository = uses mock data
		cache:      nil,
	}
}

// NewSearchServiceWithRepository creates a search service using a real repository.
func NewSearchServiceWithRepository(repository ports.SearchRepository, cache ports.Cache) *SearchService {
	return &SearchService{
		repository: repository,
		cache:      cache,
	}
}

// Search performs multi-entity search based on query parameters with pagination support.
func (s *SearchService) Search(ctx context.Context, query domain.SearchQuery) (*domain.SearchResponse, error) {
	// Validate query
	if query.Query == "" {
		return &domain.SearchResponse{
			Query:      query.Query,
			Total:      0,
			TotalPages: 0,
			Page:       1,
			PageSize:   query.Limit,
			Results:    make(map[domain.SearchEntity][]domain.SearchResult),
		}, nil
	}

	// Set default pagination values
	if query.Limit == 0 {
		query.Limit = 10
	}
	if query.Page == 0 {
		query.Page = 1
	}

	// Calculate offset for pagination (Page is 1-indexed)
	query.Offset = (query.Page - 1) * query.Limit

	response := &domain.SearchResponse{
		Query:    query.Query,
		Total:    0,
		Page:     query.Page,
		PageSize: query.Limit,
		Results:  make(map[domain.SearchEntity][]domain.SearchResult),
	}

	// Collect all results to determine total count
	allResults := make(map[domain.SearchEntity][]domain.SearchResult)
	totalResultsCount := 0

	// Search each requested entity type
	for _, entity := range query.Entities {
		if !entity.IsValid() {
			continue // Skip invalid entities
		}

		var results []domain.SearchResult

		var err error

		switch entity {
		case domain.SearchEntityCourse:
			results, err = s.searchCoursesWithRepo(ctx, query)
		case domain.SearchEntityStudent:
			results, err = s.searchStudentsWithRepo(ctx, query)
		case domain.SearchEntityTeacher:
			results, err = s.searchTeachersWithRepo(ctx, query)
		case domain.SearchEntityAssignment:
			results, err = s.searchAssignmentsWithRepo(ctx, query)
		case domain.SearchEntityAnnouncement:
			results, err = s.searchAnnouncementsWithRepo(ctx, query)
		}

		if err != nil {
			slog.Warn("search failed for entity, skipping",
				"entity", entity,
				"error", err)
			continue
		}

		// Apply role-based filtering
		results = s.filterByRole(results, query.Role)

		if len(results) > 0 {
			allResults[entity] = results
			totalResultsCount += len(results)
		}
	}

	// Calculate total pages
	if totalResultsCount > 0 {
		response.TotalPages = (totalResultsCount + query.Limit - 1) / query.Limit
	} else {
		response.TotalPages = 0
	}

	// Apply pagination to results
	currentOffset := 0
	remainingToSkip := query.Offset
	remainingToTake := query.Limit

	for entity, results := range allResults {
		if remainingToTake <= 0 {
			break
		}

		// Skip results until we reach the desired offset
		if remainingToSkip > 0 {
			if remainingToSkip >= len(results) {
				// Skip entire entity results
				remainingToSkip -= len(results)
				continue
			} else {
				// Skip partial results from this entity
				results = results[remainingToSkip:]
				remainingToSkip = 0
			}
		}

		// Take up to the limit
		if len(results) > remainingToTake {
			results = results[:remainingToTake]
		}

		response.Results[entity] = results
		response.Total += len(results)
		remainingToTake -= len(results)
		currentOffset += len(results)
	}

	return response, nil
}

// searchCoursesWithRepo searches for courses using repository or mock data.
func (s *SearchService) searchCoursesWithRepo(ctx context.Context, query domain.SearchQuery) ([]domain.SearchResult, error) {
	// Use repository if available
	if s.repository != nil {
		results, _, err := s.repository.SearchCourses(ctx, query.Query, query.Limit*10, 0) // Get more for filtering
		if err != nil {
			slog.Warn("repository search failed, falling back to mock", "error", err)
		} else {
			return results, nil
		}
	}

	// Fallback to mock data
	return s.searchCoursesMock(query), nil
}

// searchCoursesMock searches for courses using mock data.
func (s *SearchService) searchCoursesMock(query domain.SearchQuery) []domain.SearchResult {
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

// searchStudentsWithRepo searches for students using repository or mock data.
func (s *SearchService) searchStudentsWithRepo(ctx context.Context, query domain.SearchQuery) ([]domain.SearchResult, error) {
	// Use repository if available
	if s.repository != nil {
		results, _, err := s.repository.SearchStudents(ctx, query.Query, query.Limit*10, 0)
		if err != nil {
			slog.Warn("repository search failed, falling back to mock", "error", err)
		} else {
			return results, nil
		}
	}

	// Fallback to mock data
	return s.searchStudentsMock(query), nil
}

// searchStudentsMock searches for students using mock data.
func (s *SearchService) searchStudentsMock(query domain.SearchQuery) []domain.SearchResult {
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

// searchTeachersWithRepo searches for teachers using repository or mock data.
func (s *SearchService) searchTeachersWithRepo(ctx context.Context, query domain.SearchQuery) ([]domain.SearchResult, error) {
	// Use repository if available
	if s.repository != nil {
		results, _, err := s.repository.SearchTeachers(ctx, query.Query, query.Limit*10, 0)
		if err != nil {
			slog.Warn("repository search failed, falling back to mock", "error", err)
		} else {
			return results, nil
		}
	}

	// Fallback to mock data
	return s.searchTeachersMock(query), nil
}

// searchTeachersMock searches for teachers using mock data.
func (s *SearchService) searchTeachersMock(query domain.SearchQuery) []domain.SearchResult {
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

// searchAssignmentsWithRepo searches for assignments using repository or mock data.
func (s *SearchService) searchAssignmentsWithRepo(ctx context.Context, query domain.SearchQuery) ([]domain.SearchResult, error) {
	// Use repository if available
	if s.repository != nil {
		results, _, err := s.repository.SearchAssignments(ctx, query.Query, query.Limit*10, 0)
		if err != nil {
			slog.Warn("repository search failed, falling back to mock", "error", err)
		} else {
			return results, nil
		}
	}

	// Fallback to mock data
	return s.searchAssignmentsMock(query), nil
}

// searchAssignmentsMock searches for assignments using mock data.
func (s *SearchService) searchAssignmentsMock(query domain.SearchQuery) []domain.SearchResult {
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

// searchAnnouncementsWithRepo searches for announcements using repository or mock data.
func (s *SearchService) searchAnnouncementsWithRepo(ctx context.Context, query domain.SearchQuery) ([]domain.SearchResult, error) {
	// Use repository if available
	if s.repository != nil {
		results, _, err := s.repository.SearchAnnouncements(ctx, query.Query, query.Limit*10, 0)
		if err != nil {
			slog.Warn("repository search failed, falling back to mock", "error", err)
		} else {
			return results, nil
		}
	}

	// Fallback to mock data
	return s.searchAnnouncementsMock(query), nil
}

// searchAnnouncementsMock searches for announcements using mock data.
func (s *SearchService) searchAnnouncementsMock(query domain.SearchQuery) []domain.SearchResult {
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

