package ports

import (
	"context"

	"github.com/lbrines/classsphere/internal/domain"
)

// SearchRepository defines the interface for searching entities.
type SearchRepository interface {
	// SearchCourses searches for courses matching the query.
	// Returns results, total count, and error.
	SearchCourses(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error)

	// SearchStudents searches for students matching the query.
	SearchStudents(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error)

	// SearchTeachers searches for teachers matching the query.
	SearchTeachers(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error)

	// SearchAssignments searches for assignments matching the query.
	SearchAssignments(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error)

	// SearchAnnouncements searches for announcements matching the query.
	SearchAnnouncements(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error)
}

