package google

import (
	"context"
	"fmt"
	"strings"
	"time"

	"google.golang.org/api/classroom/v1"
	"google.golang.org/api/option"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

var _ ports.ClassroomProvider = (*ClassroomService)(nil)

// ClassroomService integrates with Google Classroom or provides a rich mock
// dataset depending on the active mode.
type ClassroomService struct {
	service     *classroom.Service
	mode        string
	credentials string
	now         func() time.Time
}

// Option allows configuring the ClassroomService.
type Option func(*ClassroomService)

// WithClock overrides the time provider (used in tests).
func WithClock(clock func() time.Time) Option {
	return func(c *ClassroomService) {
		if clock != nil {
			c.now = clock
		}
	}
}

// WithGoogleService injects an already initialized classroom.Service.
func WithGoogleService(svc *classroom.Service) Option {
	return func(c *ClassroomService) {
		c.service = svc
	}
}

// NewClassroomService creates a new provider. When mode is "google" it attempts
// to instantiate the official Google Classroom client. For "mock" mode it uses
// in-memory datasets.
func NewClassroomService(credentialsPath, mode string, opts ...Option) (*ClassroomService, error) {
	normalizedMode := shared.NormalizeIntegrationMode(mode)
	provider := &ClassroomService{
		mode:        normalizedMode,
		credentials: credentialsPath,
		now:         time.Now,
	}

	for _, opt := range opts {
		opt(provider)
	}

	if provider.mode == shared.IntegrationModeGoogle && provider.service == nil {
		if credentialsPath == "" {
			return nil, fmt.Errorf("credentials path required for google mode")
		}
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		srv, err := classroom.NewService(ctx, option.WithCredentialsFile(credentialsPath))
		if err != nil {
			return nil, fmt.Errorf("create classroom service: %w", err)
		}
		provider.service = srv
	}

	return provider, nil
}

// Mode returns the configured provider mode.
func (c *ClassroomService) Mode() string {
	return c.mode
}

// Service returns the underlying Google Classroom service.
// Returns nil if not in Google mode or service not initialized.
func (c *ClassroomService) Service() *classroom.Service {
	return c.service
}

// Snapshot returns an aggregated snapshot of classroom data for dashboards. It
// falls back to curated datasets when the Google API is unavailable to keep the
// experience consistent in local development.
func (c *ClassroomService) Snapshot(ctx context.Context) (domain.ClassroomSnapshot, error) {
	now := c.now()
	switch c.mode {
	case shared.IntegrationModeMock:
		return domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: now,
			Courses:     mockCourses(now),
		}, nil
	case shared.IntegrationModeGoogle:
		if c.service == nil {
			// When credentials are not available we return a simulated snapshot so
			// dashboards can still be exercised.
			return domain.ClassroomSnapshot{
				Mode:        shared.IntegrationModeGoogle,
				GeneratedAt: now,
				Courses:     googleSampleCourses(now),
			}, nil
		}
		courses, err := c.fetchCourses(ctx)
		if err != nil || len(courses) == 0 {
			// If the API call fails we degrade gracefully and use sample data.
			return domain.ClassroomSnapshot{
				Mode:        shared.IntegrationModeGoogle,
				GeneratedAt: now,
				Courses:     googleSampleCourses(now),
			}, nil
		}
		return domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeGoogle,
			GeneratedAt: now,
			Courses:     courses,
		}, nil
	default:
		return domain.ClassroomSnapshot{}, fmt.Errorf("unsupported mode %q", c.mode)
	}
}

func (c *ClassroomService) fetchCourses(ctx context.Context) ([]domain.Course, error) {
	if c.service == nil {
		return nil, nil
	}
	req := c.service.Courses.List()
	req.Context(ctx)

	resp, err := req.Do()
	if err != nil {
		return nil, fmt.Errorf("list courses: %w", err)
	}

	now := c.now()
	courses := make([]domain.Course, 0, len(resp.Courses))
	for _, item := range resp.Courses {
		if item == nil {
			continue
		}
		courses = append(courses, domain.Course{
			ID:               item.Id,
			Name:             item.Name,
			Section:          item.Section,
			Program:          strings.Title(strings.ToLower(item.Section)),
			Room:             item.Room,
			CoordinatorEmail: "",
			Teachers: []domain.CourseTeacher{
				{
					ID:    item.OwnerId,
					Name:  item.OwnerId,
					Email: item.OwnerId,
				},
			},
			LastActivity: now,
		})
	}
	return courses, nil
}
