package ports

import (
	"context"

	"github.com/lbrines/classsphere/internal/domain"
)

// ClassroomProvider abstracts the data source used to obtain Google Classroom
// information (real API or mock dataset).
type ClassroomProvider interface {
	Mode() string
	Snapshot(ctx context.Context) (domain.ClassroomSnapshot, error)
}
