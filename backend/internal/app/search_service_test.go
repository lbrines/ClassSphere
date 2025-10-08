package app

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/domain"
)

func TestSearchService_NewSearchService(t *testing.T) {
	service := NewSearchService()
	
	assert.NotNil(t, service)
}

func TestSearchService_SearchSingleEntity(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "Math",
		Entities: []domain.SearchEntity{domain.SearchEntityCourse},
		Limit:    10,
	}
	
	response, err := service.Search(ctx, query)
	
	require.NoError(t, err)
	assert.NotNil(t, response)
	assert.Equal(t, "Math", response.Query)
	assert.GreaterOrEqual(t, response.Total, 0)
}

func TestSearchService_SearchMultipleEntities(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query: "John",
		Entities: []domain.SearchEntity{
			domain.SearchEntityStudent,
			domain.SearchEntityTeacher,
		},
		Role:  domain.RoleTeacher, // Teacher can see both students and teachers
		Limit: 10,
	}
	
	response, err := service.Search(ctx, query)
	
	require.NoError(t, err)
	assert.Equal(t, "John", response.Query)
	
	// Should have results for both entity types (teacher can see both)
	_, hasStudents := response.Results[domain.SearchEntityStudent]
	_, hasTeachers := response.Results[domain.SearchEntityTeacher]
	
	assert.True(t, hasStudents || hasTeachers, "Should have results for at least one entity type")
}

func TestSearchService_SearchWithRoleFilter(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	tests := []struct {
		name     string
		role     domain.Role
		entities []domain.SearchEntity
	}{
		{
			name:     "Student can search courses",
			role:     domain.RoleStudent,
			entities: []domain.SearchEntity{domain.SearchEntityCourse},
		},
		{
			name:     "Teacher can search students and courses",
			role:     domain.RoleTeacher,
			entities: []domain.SearchEntity{domain.SearchEntityStudent, domain.SearchEntityCourse},
		},
		{
			name:     "Admin can search all entities",
			role:     domain.RoleAdmin,
			entities: []domain.SearchEntity{
				domain.SearchEntityStudent,
				domain.SearchEntityTeacher,
				domain.SearchEntityCourse,
				domain.SearchEntityAssignment,
			},
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			query := domain.SearchQuery{
				Query:    "test",
				Entities: tt.entities,
				Role:     tt.role,
				Limit:    5,
			}
			
			response, err := service.Search(ctx, query)
			
			require.NoError(t, err)
			assert.NotNil(t, response)
		})
	}
}

func TestSearchService_EmptyQuery(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "",
		Entities: []domain.SearchEntity{domain.SearchEntityCourse},
		Limit:    10,
	}
	
	response, err := service.Search(ctx, query)
	
	// Empty query should return empty results, not error
	require.NoError(t, err)
	assert.Equal(t, 0, response.Total)
}

func TestSearchService_InvalidEntity(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "test",
		Entities: []domain.SearchEntity{"invalid"},
		Limit:    10,
	}
	
	response, err := service.Search(ctx, query)
	
	// Should skip invalid entities, not error
	require.NoError(t, err)
	assert.NotNil(t, response)
}

func TestSearchService_LimitResults(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "Math",
		Entities: []domain.SearchEntity{domain.SearchEntityCourse},
		Limit:    3,
	}
	
	response, err := service.Search(ctx, query)
	
	require.NoError(t, err)
	
	// Each entity type should respect limit
	for _, results := range response.Results {
		assert.LessOrEqual(t, len(results), 3)
	}
}

func TestSearchService_SearchWithUserContext(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "assignment",
		Entities: []domain.SearchEntity{domain.SearchEntityAssignment},
		UserID:   "student-1",
		Role:     domain.RoleStudent,
		Limit:    10,
	}
	
	response, err := service.Search(ctx, query)
	
	// Should return personalized results for the user
	require.NoError(t, err)
	assert.NotNil(t, response)
}

func TestSearchService_CaseInsensitiveSearch(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	tests := []struct {
		query string
	}{
		{"math"},
		{"MATH"},
		{"Math"},
		{"mAtH"},
	}
	
	for _, tt := range tests {
		t.Run(tt.query, func(t *testing.T) {
			query := domain.SearchQuery{
				Query:    tt.query,
				Entities: []domain.SearchEntity{domain.SearchEntityCourse},
				Limit:    10,
			}
			
			response, err := service.Search(ctx, query)
			
			require.NoError(t, err)
			assert.NotNil(t, response)
		})
	}
}

func TestSearchService_RelevanceScoring(t *testing.T) {
	ctx := context.Background()
	service := NewSearchService()
	
	query := domain.SearchQuery{
		Query:    "Mathematics",
		Entities: []domain.SearchEntity{domain.SearchEntityCourse},
		Limit:    10,
	}
	
	response, err := service.Search(ctx, query)
	
	require.NoError(t, err)
	
	// Results should be sorted by relevance (descending)
	for _, results := range response.Results {
		for i := 1; i < len(results); i++ {
			assert.GreaterOrEqual(t, results[i-1].Relevance, results[i].Relevance,
				"Results should be sorted by relevance (descending)")
		}
	}
}

// ==============================================================================
// Security Tests - RBAC Filtering
// ==============================================================================

func TestSearchService_FilterByRole_StudentCannotSeeTeachers(t *testing.T) {
	// GIVEN: Search service with teacher results
	service := NewSearchService()
	
	teacherResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-1",
			Title:       "Prof. John Doe",
			Description: "john@faculty.edu",
			Relevance:   1.0,
		},
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-2",
			Title:       "Dr. Jane Smith",
			Description: "jane@faculty.edu",
			Relevance:   0.9,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(teacherResults, domain.RoleStudent)
	
	// THEN: No teachers should be returned
	assert.Empty(t, filtered, "students should not see teacher search results")
}

func TestSearchService_FilterByRole_StudentCannotSeeOtherStudents(t *testing.T) {
	// GIVEN: Search service with student results
	service := NewSearchService()
	
	studentResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityStudent,
			ID:          "student-1",
			Title:       "John Student",
			Description: "john@student.edu",
			Relevance:   1.0,
		},
		{
			Type:        domain.SearchEntityStudent,
			ID:          "student-2",
			Title:       "Jane Student",
			Description: "jane@student.edu",
			Relevance:   0.9,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(studentResults, domain.RoleStudent)
	
	// THEN: No students should be returned (privacy)
	assert.Empty(t, filtered, "students should not see other students in search")
}

func TestSearchService_FilterByRole_StudentCanSeeCourses(t *testing.T) {
	// GIVEN: Search service with course results
	service := NewSearchService()
	
	courseResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityCourse,
			ID:          "course-1",
			Title:       "Mathematics 101",
			Description: "Intro to Calculus",
			Relevance:   1.0,
		},
		{
			Type:        domain.SearchEntityCourse,
			ID:          "course-2",
			Title:       "Physics 101",
			Description: "Basic Physics",
			Relevance:   0.9,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(courseResults, domain.RoleStudent)
	
	// THEN: Courses should be visible
	assert.Len(t, filtered, 2, "students should see course results")
	assert.Equal(t, "course-1", filtered[0].ID)
	assert.Equal(t, "course-2", filtered[1].ID)
}

func TestSearchService_FilterByRole_StudentCanSeeAssignments(t *testing.T) {
	// GIVEN: Search service with assignment results
	service := NewSearchService()
	
	assignmentResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityAssignment,
			ID:          "assignment-1",
			Title:       "Homework 1",
			Description: "Math problems",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(assignmentResults, domain.RoleStudent)
	
	// THEN: Assignments should be visible
	assert.Len(t, filtered, 1, "students should see assignment results")
	assert.Equal(t, "assignment-1", filtered[0].ID)
}

func TestSearchService_FilterByRole_TeacherCanSeeStudents(t *testing.T) {
	// GIVEN: Search service with student results
	service := NewSearchService()
	
	studentResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityStudent,
			ID:          "student-1",
			Title:       "John Student",
			Description: "john@student.edu",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as teacher role
	filtered := service.filterByRole(studentResults, domain.RoleTeacher)
	
	// THEN: Students should be visible to teachers
	assert.Len(t, filtered, 1, "teachers should see student results")
	assert.Equal(t, "student-1", filtered[0].ID)
}

func TestSearchService_FilterByRole_TeacherCanSeeOtherTeachers(t *testing.T) {
	// GIVEN: Search service with teacher results
	service := NewSearchService()
	
	teacherResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-1",
			Title:       "Prof. Colleague",
			Description: "colleague@faculty.edu",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as teacher role
	filtered := service.filterByRole(teacherResults, domain.RoleTeacher)
	
	// THEN: Teachers should be visible to other teachers
	assert.Len(t, filtered, 1, "teachers should see other teachers")
	assert.Equal(t, "teacher-1", filtered[0].ID)
}

func TestSearchService_FilterByRole_CoordinatorCannotSeeStudents(t *testing.T) {
	// GIVEN: Search service with student results
	service := NewSearchService()
	
	studentResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityStudent,
			ID:          "student-1",
			Title:       "John Student",
			Description: "john@student.edu",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as coordinator role
	filtered := service.filterByRole(studentResults, domain.RoleCoordinator)
	
	// THEN: Students should NOT be visible (privacy)
	assert.Empty(t, filtered, "coordinators should not see student details")
}

func TestSearchService_FilterByRole_CoordinatorCanSeeTeachers(t *testing.T) {
	// GIVEN: Search service with teacher results
	service := NewSearchService()
	
	teacherResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-1",
			Title:       "Prof. Faculty",
			Description: "faculty@edu.com",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as coordinator role
	filtered := service.filterByRole(teacherResults, domain.RoleCoordinator)
	
	// THEN: Teachers should be visible
	assert.Len(t, filtered, 1, "coordinators should see teacher results")
}

func TestSearchService_FilterByRole_AdminSeesEverything(t *testing.T) {
	// GIVEN: Search service with all types of results
	service := NewSearchService()
	
	mixedResults := []domain.SearchResult{
		{Type: domain.SearchEntityStudent, ID: "student-1", Title: "Student", Relevance: 1.0},
		{Type: domain.SearchEntityTeacher, ID: "teacher-1", Title: "Teacher", Relevance: 1.0},
		{Type: domain.SearchEntityCourse, ID: "course-1", Title: "Course", Relevance: 1.0},
		{Type: domain.SearchEntityAssignment, ID: "assign-1", Title: "Assignment", Relevance: 1.0},
		{Type: domain.SearchEntityAnnouncement, ID: "ann-1", Title: "Announcement", Relevance: 1.0},
	}
	
	// WHEN: Filter as admin role
	filtered := service.filterByRole(mixedResults, domain.RoleAdmin)
	
	// THEN: All results should be visible
	assert.Len(t, filtered, 5, "admins should see all results")
	
	// Verify all entity types are present
	entityTypes := make(map[domain.SearchEntity]bool)
	for _, result := range filtered {
		entityTypes[result.Type] = true
	}
	assert.Len(t, entityTypes, 5, "admin should see all 5 entity types")
}

func TestSearchService_FilterByRole_MixedResultsFiltering(t *testing.T) {
	// GIVEN: Search service with mixed results
	service := NewSearchService()
	
	mixedResults := []domain.SearchResult{
		{Type: domain.SearchEntityStudent, ID: "student-1", Title: "Student", Relevance: 1.0},
		{Type: domain.SearchEntityTeacher, ID: "teacher-1", Title: "Teacher", Relevance: 0.9},
		{Type: domain.SearchEntityCourse, ID: "course-1", Title: "Course", Relevance: 0.8},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(mixedResults, domain.RoleStudent)
	
	// THEN: Only courses should be visible (students can't see teachers or other students)
	assert.Len(t, filtered, 1, "student should only see courses")
	assert.Equal(t, domain.SearchEntityCourse, filtered[0].Type)
	assert.Equal(t, "course-1", filtered[0].ID)
}

func TestSearchService_FilterByRole_EmptyResults(t *testing.T) {
	// GIVEN: Search service with empty results
	service := NewSearchService()
	
	emptyResults := []domain.SearchResult{}
	
	// WHEN: Filter as any role
	filtered := service.filterByRole(emptyResults, domain.RoleStudent)
	
	// THEN: Should return empty slice (not nil)
	assert.NotNil(t, filtered)
	assert.Empty(t, filtered)
}

func TestSearchService_FilterByRole_UnknownRole(t *testing.T) {
	// GIVEN: Search service with results
	service := NewSearchService()
	
	results := []domain.SearchResult{
		{Type: domain.SearchEntityCourse, ID: "course-1", Title: "Course", Relevance: 1.0},
	}
	
	// WHEN: Filter with unknown/invalid role
	unknownRole := domain.Role("unknown-role")
	filtered := service.filterByRole(results, unknownRole)
	
	// THEN: Should deny all (secure by default)
	assert.Empty(t, filtered, "unknown roles should be denied access to all results")
}

func TestSearchService_Search_IntegrationWithRBAC(t *testing.T) {
	// GIVEN: Search service with full search query
	ctx := context.Background()
	service := NewSearchService()
	
	// WHEN: Student searches for teachers
	studentQuery := domain.SearchQuery{
		Query:    "prof",
		Entities: []domain.SearchEntity{domain.SearchEntityTeacher},
		Role:     domain.RoleStudent,
		UserID:   "student-1",
		Limit:    10,
	}
	
	studentResponse, err := service.Search(ctx, studentQuery)
	
	// THEN: Student should get empty results (RBAC filters teachers)
	require.NoError(t, err)
	assert.NotNil(t, studentResponse)
	teacherResults, hasTeachers := studentResponse.Results[domain.SearchEntityTeacher]
	if hasTeachers {
		assert.Empty(t, teacherResults, "students should not see teacher results")
	}
	
	// WHEN: Teacher searches for teachers
	teacherQuery := domain.SearchQuery{
		Query:    "prof",
		Entities: []domain.SearchEntity{domain.SearchEntityTeacher},
		Role:     domain.RoleTeacher,
		UserID:   "teacher-1",
		Limit:    10,
	}
	
	teacherResponse, err := service.Search(ctx, teacherQuery)
	
	// THEN: Teacher should potentially get results (RBAC allows)
	require.NoError(t, err)
	assert.NotNil(t, teacherResponse)
	// Teacher can see results if they match the query
}

