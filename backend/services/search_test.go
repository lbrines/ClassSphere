package services

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestSearchService_SearchStudents(t *testing.T) {
	service := NewSearchService()
	
	tests := []struct {
		name    string
		query   string
		filters SearchFilters
		wantLen int
	}{
		{
			name:    "search by name",
			query:   "john",
			filters: SearchFilters{},
			wantLen: 1,
		},
		{
			name:    "search by email",
			query:   "jane@example.com",
			filters: SearchFilters{},
			wantLen: 1,
		},
		{
			name:    "search with empty query",
			query:   "",
			filters: SearchFilters{},
			wantLen: 5,
		},
		{
			name:    "search with no matches",
			query:   "nonexistent",
			filters: SearchFilters{},
			wantLen: 0,
		},
		{
			name:    "case insensitive search",
			query:   "JOHN",
			filters: SearchFilters{},
			wantLen: 1,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := service.SearchStudents(tt.query, tt.filters)
			assert.Len(t, results, tt.wantLen)
			
			// Verify all results are students
			for _, result := range results {
				assert.Equal(t, "student", result.Type)
				assert.NotEmpty(t, result.ID)
				assert.NotEmpty(t, result.Title)
				assert.NotEmpty(t, result.Description)
				assert.GreaterOrEqual(t, result.Score, 0.0)
				assert.LessOrEqual(t, result.Score, 1.0)
			}
		})
	}
}

func TestSearchService_SearchCourses(t *testing.T) {
	service := NewSearchService()
	
	tests := []struct {
		name    string
		query   string
		filters SearchFilters
		wantLen int
	}{
		{
			name:    "search by course name",
			query:   "math",
			filters: SearchFilters{},
			wantLen: 1,
		},
		{
			name:    "search by description",
			query:   "basic",
			filters: SearchFilters{},
			wantLen: 2,
		},
		{
			name:    "search with course filter",
			query:   "",
			filters: SearchFilters{Course: "physics"},
			wantLen: 1,
		},
		{
			name:    "search with both query and filter",
			query:   "chemistry",
			filters: SearchFilters{Course: "chemistry"},
			wantLen: 1,
		},
		{
			name:    "search with no matches",
			query:   "nonexistent",
			filters: SearchFilters{},
			wantLen: 0,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := service.SearchCourses(tt.query, tt.filters)
			assert.Len(t, results, tt.wantLen)
			
			// Verify all results are courses
			for _, result := range results {
				assert.Equal(t, "course", result.Type)
				assert.NotEmpty(t, result.ID)
				assert.NotEmpty(t, result.Title)
				assert.NotEmpty(t, result.Description)
				assert.GreaterOrEqual(t, result.Score, 0.0)
				assert.LessOrEqual(t, result.Score, 1.0)
			}
		})
	}
}

func TestSearchService_SearchAssignments(t *testing.T) {
	service := NewSearchService()
	
	tests := []struct {
		name    string
		query   string
		filters SearchFilters
		wantLen int
	}{
		{
			name:    "search by assignment title",
			query:   "homework",
			filters: SearchFilters{},
			wantLen: 1,
		},
		{
			name:    "search by description",
			query:   "lab",
			filters: SearchFilters{},
			wantLen: 1,
		},
		{
			name:    "search with points filter",
			query:   "",
			filters: SearchFilters{MinPoints: 100, MaxPoints: 200},
			wantLen: 3,
		},
		{
			name:    "search with state filter",
			query:   "",
			filters: SearchFilters{State: "PUBLISHED"},
			wantLen: 3,
		},
		{
			name:    "search with multiple filters",
			query:   "math",
			filters: SearchFilters{MinPoints: 50, State: "PUBLISHED"},
			wantLen: 1,
		},
		{
			name:    "search with no matches",
			query:   "nonexistent",
			filters: SearchFilters{},
			wantLen: 0,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := service.SearchAssignments(tt.query, tt.filters)
			assert.Len(t, results, tt.wantLen)
			
			// Verify all results are assignments
			for _, result := range results {
				assert.Equal(t, "assignment", result.Type)
				assert.NotEmpty(t, result.ID)
				assert.NotEmpty(t, result.Title)
				assert.NotEmpty(t, result.Description)
				assert.GreaterOrEqual(t, result.Score, 0.0)
				assert.LessOrEqual(t, result.Score, 1.0)
			}
		})
	}
}

func TestSearchService_SearchAll(t *testing.T) {
	service := NewSearchService()
	
	tests := []struct {
		name     string
		request  SearchRequest
		wantMin  int
		wantMax  int
	}{
		{
			name: "search all with query",
			request: SearchRequest{
				Query:   "math",
				Filters: SearchFilters{},
				Limit:   10,
				Offset:  0,
			},
			wantMin: 1,
			wantMax: 2,
		},
		{
			name: "search all with empty query",
			request: SearchRequest{
				Query:   "",
				Filters: SearchFilters{},
				Limit:   10,
				Offset:  0,
			},
			wantMin: 10, // Limited by pagination
			wantMax: 10,
		},
		{
			name: "search all with pagination",
			request: SearchRequest{
				Query:   "",
				Filters: SearchFilters{},
				Limit:   5,
				Offset:  0,
			},
			wantMin: 5,
			wantMax: 5,
		},
		{
			name: "search all with offset",
			request: SearchRequest{
				Query:   "",
				Filters: SearchFilters{},
				Limit:   5,
				Offset:  10,
			},
			wantMin: 5,
			wantMax: 5,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			response := service.SearchAll(tt.request)
			
			assert.GreaterOrEqual(t, len(response.Results), tt.wantMin)
			assert.LessOrEqual(t, len(response.Results), tt.wantMax)
			assert.Equal(t, tt.request.Query, response.Query)
			assert.Equal(t, tt.request.Filters, response.Filters)
			assert.Greater(t, response.SearchTime, time.Duration(0))
			assert.GreaterOrEqual(t, response.Total, len(response.Results))
			
			// Verify results are sorted by relevance (highest first)
			for i := 1; i < len(response.Results); i++ {
				assert.GreaterOrEqual(t, response.Results[i-1].Score, response.Results[i].Score)
			}
		})
	}
}

func TestSearchService_CalculateRelevanceScore(t *testing.T) {
	service := NewSearchService()
	
	tests := []struct {
		name        string
		query       string
		title       string
		description string
		wantMin     float64
		wantMax     float64
	}{
		{
			name:        "exact title match",
			query:       "math",
			title:       "math homework",
			description: "basic problems",
			wantMin:     0.8,
			wantMax:     1.0,
		},
		{
			name:        "description match",
			query:       "problems",
			title:       "homework",
			description: "basic problems",
			wantMin:     0.4,
			wantMax:     0.6,
		},
		{
			name:        "no match",
			query:       "nonexistent",
			title:       "homework",
			description: "basic problems",
			wantMin:     0.0,
			wantMax:     0.0,
		},
		{
			name:        "empty query",
			query:       "",
			title:       "homework",
			description: "basic problems",
			wantMin:     1.0,
			wantMax:     1.0,
		},
		{
			name:        "multiple word match",
			query:       "math homework",
			title:       "math homework assignment",
			description: "basic math problems",
			wantMin:     0.8,
			wantMax:     1.0,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			score := service.calculateRelevanceScore(tt.query, tt.title, tt.description)
			assert.GreaterOrEqual(t, score, tt.wantMin)
			assert.LessOrEqual(t, score, tt.wantMax)
		})
	}
}

func TestSearchService_SortByRelevance(t *testing.T) {
	service := NewSearchService()
	
	results := []SearchResult{
		{Score: 0.3, Title: "Low score"},
		{Score: 0.9, Title: "High score"},
		{Score: 0.6, Title: "Medium score"},
		{Score: 0.1, Title: "Very low score"},
	}
	
	service.sortByRelevance(results)
	
	// Verify results are sorted by score (highest first)
	assert.Equal(t, 0.9, results[0].Score)
	assert.Equal(t, 0.6, results[1].Score)
	assert.Equal(t, 0.3, results[2].Score)
	assert.Equal(t, 0.1, results[3].Score)
}

func TestNewSearchService(t *testing.T) {
	service := NewSearchService()
	assert.NotNil(t, service)
}

func TestSearchFilters_Empty(t *testing.T) {
	filters := SearchFilters{}
	assert.Empty(t, filters.Course)
	assert.Empty(t, filters.Grade)
	assert.Empty(t, filters.DateFrom)
	assert.Empty(t, filters.DateTo)
	assert.Equal(t, 0, filters.MinPoints)
	assert.Equal(t, 0, filters.MaxPoints)
	assert.Empty(t, filters.State)
}

func TestSearchRequest_DefaultValues(t *testing.T) {
	request := SearchRequest{
		Query: "test",
		Filters: SearchFilters{},
		Limit: 10,
		Offset: 0,
	}
	
	assert.Equal(t, "test", request.Query)
	assert.Equal(t, 10, request.Limit)
	assert.Equal(t, 0, request.Offset)
	assert.NotNil(t, request.Filters)
}

func TestSearchResponse_Structure(t *testing.T) {
	response := SearchResponse{
		Results:    []SearchResult{},
		Total:      0,
		Query:      "test",
		Filters:    SearchFilters{},
		SearchTime: time.Millisecond * 100,
	}
	
	assert.NotNil(t, response.Results)
	assert.Equal(t, 0, response.Total)
	assert.Equal(t, "test", response.Query)
	assert.NotNil(t, response.Filters)
	assert.Greater(t, response.SearchTime, time.Duration(0))
}
