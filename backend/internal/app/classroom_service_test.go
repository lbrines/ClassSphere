package app_test

import (
	"context"
	"testing"
	"time"

	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

func TestClassroomService_ListCourses(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()

	result, err := service.ListCourses(ctx, "")
	require.NoError(t, err)
	require.Equal(t, shared.IntegrationModeMock, result.Mode)
	require.Len(t, result.Courses, 2)
	require.Equal(t, "Humanities Seminar", result.Courses[0].Name)
	require.Equal(t, 2, result.Courses[0].UpcomingAssignments)
	require.InDelta(t, 100, result.Courses[0].CompletionRate, 0.1)
	require.InDelta(t, 62.5, result.Courses[1].CompletionRate, 0.1)
}

func TestClassroomService_DashboardByRole(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()

	admin := domain.User{ID: "admin-1", Role: domain.RoleAdmin, Email: "admin@classsphere.edu"}
	adminDashboard, err := service.Dashboard(ctx, admin, "mock")
	require.NoError(t, err)
	require.Equal(t, "admin", adminDashboard.Role)
	require.Equal(t, shared.IntegrationModeMock, adminDashboard.Mode)
	require.Equal(t, float64(2), summaryValue(adminDashboard, "totalCourses"))

	teacher := domain.User{ID: "teacher-1", Role: domain.RoleTeacher, Email: "teacher@classsphere.edu"}
	teacherDashboard, err := service.Dashboard(ctx, teacher, "")
	require.NoError(t, err)
	require.Equal(t, "teacher", teacherDashboard.Role)
	require.Equal(t, float64(1), summaryValue(teacherDashboard, "teacherCourses"))
	require.NotEmpty(t, teacherDashboard.Timeline)

	student := domain.User{ID: "student-1", Role: domain.RoleStudent, Email: "student@classsphere.edu"}
	studentDashboard, err := service.Dashboard(ctx, student, "")
	require.NoError(t, err)
	require.Equal(t, "student", studentDashboard.Role)
	require.InDelta(t, 3, summaryValue(studentDashboard, "completedAssignments"), 0.1)

	coordinator := domain.User{ID: "coord-1", Role: domain.RoleCoordinator, Email: "coordinator@classsphere.edu"}
	coordDashboard, err := service.Dashboard(ctx, coordinator, "")
	require.NoError(t, err)
	require.Equal(t, "coordinator", coordDashboard.Role)
	require.Equal(t, float64(2), summaryValue(coordDashboard, "coordinatorCourses"))
}

func summaryValue(data app.DashboardData, id string) float64 {
	for _, metric := range data.Summary {
		if metric.ID == id {
			return metric.Value
		}
	}
	return 0
}

func newTestClassroomService(t *testing.T) *app.ClassroomService {
	t.Helper()
	now := time.Date(2025, time.January, 7, 9, 0, 0, 0, time.UTC)

	courseA := domain.Course{
		ID:               "course-a",
		Name:             "Advanced Robotics",
		Section:          "STEM-201",
		Program:          "STEM",
		Room:             "Lab 5",
		CoordinatorEmail: "coordinator@classsphere.edu",
		Teachers: []domain.CourseTeacher{{
			ID:    "teacher-1",
			Name:  "Carlos Vega",
			Email: "teacher@classsphere.edu",
		}},
		Students: []domain.CourseStudent{
			{
				Person: domain.Person{ID: "student-1", Name: "Sara Kim", Email: "student@classsphere.edu"},
				Progress: domain.StudentProgress{
					CompletedAssignments: 3,
					PendingAssignments:   1,
					AverageScore:         92,
					AttendanceRate:       0.95,
					LateSubmissions:      1,
					UpcomingAssignments:  1,
					LastSubmission:       now.Add(-24 * time.Hour),
				},
			},
			{
				Person: domain.Person{ID: "student-2", Name: "Leo Park", Email: "leo.park@classsphere.edu"},
				Progress: domain.StudentProgress{
					CompletedAssignments: 2,
					PendingAssignments:   2,
					AverageScore:         78,
					AttendanceRate:       0.9,
					LateSubmissions:      2,
					UpcomingAssignments:  1,
					LastSubmission:       now.Add(-48 * time.Hour),
				},
			},
		},
		Assignments: []domain.CourseAssignment{
			{
				ID:        "assign-a1",
				Title:     "Prototype Demo",
				DueDate:   now.Add(72 * time.Hour),
				MaxPoints: 100,
				Status:    domain.AssignmentStatusOpen,
				Completed: 12,
				Pending:   4,
				Late:      2,
			},
			{
				ID:        "assign-a2",
				Title:     "Systems Report",
				DueDate:   now.Add(-24 * time.Hour),
				MaxPoints: 100,
				Status:    domain.AssignmentStatusClosed,
				Completed: 14,
				Pending:   0,
				Late:      1,
			},
		},
		LastActivity: now.Add(-6 * time.Hour),
	}

	courseB := domain.Course{
		ID:               "course-b",
		Name:             "Humanities Seminar",
		Section:          "HUM-101",
		Program:          "Humanities",
		Room:             "Room 4",
		CoordinatorEmail: "coordinator@classsphere.edu",
		Teachers: []domain.CourseTeacher{{
			ID:    "teacher-2",
			Name:  "Laura Nguyen",
			Email: "laura.nguyen@classsphere.edu",
		}},
		Students: []domain.CourseStudent{
			{
				Person: domain.Person{ID: "student-3", Name: "Ava Moore", Email: "ava.moore@classsphere.edu"},
				Progress: domain.StudentProgress{
					CompletedAssignments: 5,
					PendingAssignments:   0,
					AverageScore:         96,
					AttendanceRate:       0.99,
					LateSubmissions:      0,
					UpcomingAssignments:  1,
					LastSubmission:       now.Add(-12 * time.Hour),
				},
			},
			{
				Person: domain.Person{ID: "student-4", Name: "Noah Patel", Email: "noah.patel@classsphere.edu"},
				Progress: domain.StudentProgress{
					CompletedAssignments: 4,
					PendingAssignments:   0,
					AverageScore:         93,
					AttendanceRate:       0.97,
					LateSubmissions:      0,
					UpcomingAssignments:  1,
					LastSubmission:       now.Add(-18 * time.Hour),
				},
			},
		},
		Assignments: []domain.CourseAssignment{
			{
				ID:        "assign-b1",
				Title:     "Essay Draft",
				DueDate:   now.Add(24 * time.Hour),
				MaxPoints: 50,
				Status:    domain.AssignmentStatusOpen,
				Completed: 10,
				Pending:   0,
				Late:      0,
			},
			{
				ID:        "assign-b2",
				Title:     "Seminar Presentation",
				DueDate:   now.Add(120 * time.Hour),
				MaxPoints: 100,
				Status:    domain.AssignmentStatusPlanned,
				Completed: 0,
				Pending:   12,
				Late:      0,
			},
		},
		LastActivity: now.Add(-3 * time.Hour),
	}

	provider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: now,
			Courses:     []domain.Course{courseA, courseB},
		},
	}

	service, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	service.WithClock(func() time.Time { return now })
	return service
}

type fakeClassroomProvider struct {
	snapshot domain.ClassroomSnapshot
}

func (f *fakeClassroomProvider) Mode() string {
	return f.snapshot.Mode
}

func (f *fakeClassroomProvider) Snapshot(_ context.Context) (domain.ClassroomSnapshot, error) {
	return f.snapshot, nil
}
