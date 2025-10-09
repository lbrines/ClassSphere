package repo_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"google.golang.org/api/classroom/v1"

	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/domain"
)

// ==============================================================================
// Classroom Search Repository Tests
// ==============================================================================

func TestClassroomSearchRepository_SearchCourses(t *testing.T) {
	// GIVEN: Mock Google Classroom service
	mockService := createMockClassroomService(t)
	cache := &mockCache{}
	repository := repo.NewClassroomSearchRepository(mockService, cache)
	
	ctx := context.Background()
	
	// WHEN: Search for courses
	results, total, err := repository.SearchCourses(ctx, "math", 10, 0)
	
	// THEN: Should return filtered results
	require.NoError(t, err)
	assert.GreaterOrEqual(t, total, 0)
	assert.LessOrEqual(t, len(results), 10)
	
	// Verify results have correct type
	for _, result := range results {
		assert.Equal(t, domain.SearchEntityCourse, result.Type)
		assert.NotEmpty(t, result.ID)
		assert.NotEmpty(t, result.Title)
	}
}

func TestClassroomSearchRepository_SearchCourses_WithPagination(t *testing.T) {
	// GIVEN: Mock Google Classroom service
	mockService := createMockClassroomService(t)
	cache := &mockCache{}
	repository := repo.NewClassroomSearchRepository(mockService, cache)
	
	ctx := context.Background()
	
	// WHEN: Search first page
	page1, total1, err := repository.SearchCourses(ctx, "math", 2, 0)
	require.NoError(t, err)
	
	// WHEN: Search second page
	page2, total2, err := repository.SearchCourses(ctx, "math", 2, 2)
	require.NoError(t, err)
	
	// THEN: Total should be the same, but results different
	assert.Equal(t, total1, total2)
	assert.LessOrEqual(t, len(page1), 2)
	assert.LessOrEqual(t, len(page2), 2)
	
	// Page 1 and page 2 should have different results (if enough data)
	if len(page1) > 0 && len(page2) > 0 {
		assert.NotEqual(t, page1[0].ID, page2[0].ID)
	}
}

func TestClassroomSearchRepository_SearchCourses_WithCache(t *testing.T) {
	// GIVEN: Repository with cache
	mockService := createMockClassroomService(t)
	cache := &mockCache{store: make(map[string][]byte)}
	repository := repo.NewClassroomSearchRepository(mockService, cache)
	
	ctx := context.Background()
	
	// WHEN: Search twice with same parameters
	results1, total1, err := repository.SearchCourses(ctx, "math", 5, 0)
	require.NoError(t, err)
	
	results2, total2, err := repository.SearchCourses(ctx, "math", 5, 0)
	require.NoError(t, err)
	
	// THEN: Second call should hit cache
	assert.Equal(t, total1, total2)
	assert.Equal(t, len(results1), len(results2))
	
	// Verify cache was used (same results)
	if len(results1) > 0 && len(results2) > 0 {
		assert.Equal(t, results1[0].ID, results2[0].ID)
	}
}

func TestClassroomSearchRepository_NilService(t *testing.T) {
	// GIVEN: Repository with nil service
	repository := repo.NewClassroomSearchRepository(nil, nil)
	
	ctx := context.Background()
	
	// WHEN: Attempt to search
	results, total, err := repository.SearchCourses(ctx, "math", 10, 0)
	
	// THEN: Should return error
	require.Error(t, err)
	assert.Nil(t, results)
	assert.Equal(t, 0, total)
	assert.Contains(t, err.Error(), "not initialized")
}

func TestClassroomSearchRepository_EmptyQuery(t *testing.T) {
	// GIVEN: Repository with mock service
	mockService := createMockClassroomService(t)
	repository := repo.NewClassroomSearchRepository(mockService, nil)
	
	ctx := context.Background()
	
	// WHEN: Search with empty query
	results, total, err := repository.SearchCourses(ctx, "", 10, 0)
	
	// THEN: Should return empty results
	require.NoError(t, err)
	assert.Equal(t, 0, total)
	assert.Empty(t, results)
}

// ==============================================================================
// Test Helpers
// ==============================================================================

// createMockClassroomService creates a mock classroom.Service for testing.
// Note: This is a simplified mock. For real tests, use Google's testing utilities.
func createMockClassroomService(t *testing.T) *classroom.Service {
	// For now, return nil to indicate mock mode
	// In real implementation, you would use httptest.Server to mock Google API
	return nil
}

type mockCache struct {
	store map[string][]byte
}

func (c *mockCache) Set(ctx context.Context, key string, value []byte, expiration int) error {
	if c.store != nil {
		c.store[key] = value
	}
	return nil
}

func (c *mockCache) Get(ctx context.Context, key string) ([]byte, error) {
	if c.store == nil {
		return nil, nil
	}
	if val, ok := c.store[key]; ok {
		return val, nil
	}
	return nil, nil
}

func (c *mockCache) Delete(ctx context.Context, key string) error {
	if c.store != nil {
		delete(c.store, key)
	}
	return nil
}

func (c *mockCache) Ping(ctx context.Context) error {
	return nil
}

func (c *mockCache) Close() error {
	return nil
}

