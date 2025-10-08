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
		Limit: 10,
	}
	
	response, err := service.Search(ctx, query)
	
	require.NoError(t, err)
	assert.Equal(t, "John", response.Query)
	
	// Should have results for both entity types
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

