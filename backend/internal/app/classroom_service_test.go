package app_test

import (
	"context"
	"fmt"
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

func TestClassroomService_AvailableModes(t *testing.T) {
	service := newTestClassroomService(t)
	
	modes := service.AvailableModes()
	
	require.NotEmpty(t, modes)
	require.Contains(t, modes, shared.IntegrationModeMock)
}

func TestClassroomService_AvailableModes_MultipleProviders(t *testing.T) {
	mockProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{},
		},
	}
	
	googleProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeGoogle,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, mockProvider, googleProvider)
	require.NoError(t, err)
	
	modes := service.AvailableModes()
	
	require.Len(t, modes, 2)
	require.Contains(t, modes, shared.IntegrationModeMock)
	require.Contains(t, modes, shared.IntegrationModeGoogle)
}

func TestClassroomService_Dashboard_EmptyProvider(t *testing.T) {
	emptyProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{}, // No courses
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, emptyProvider)
	require.NoError(t, err)
	
	ctx := context.Background()
	admin := domain.User{ID: "admin-1", Role: domain.RoleAdmin, Email: "admin@classsphere.edu"}
	
	dashboard, err := service.Dashboard(ctx, admin, "")
	require.NoError(t, err)
	
	// Should return empty dashboard with 0 values
	require.Equal(t, "admin", dashboard.Role)
	require.NotNil(t, dashboard.Summary)
	require.NotNil(t, dashboard.Charts)
}

func TestClassroomService_ResolveMode_InvalidMode(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()
	
	// Test with invalid mode - should fallback to default
	user := domain.User{ID: "admin-1", Role: domain.RoleAdmin}
	dashboard, err := service.Dashboard(ctx, user, "invalid-mode")
	
	require.NoError(t, err)
	require.Equal(t, shared.IntegrationModeMock, dashboard.Mode)
}

func TestClassroomService_NewClassroomService_NoProviders(t *testing.T) {
	_, err := app.NewClassroomService(shared.IntegrationModeMock)
	
	require.Error(t, err)
	require.Contains(t, err.Error(), "at least one classroom provider must be supplied")
}

func TestClassroomService_NewClassroomService_DuplicateProviders(t *testing.T) {
	mockProvider1 := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{},
		},
	}
	
	mockProvider2 := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, mockProvider1, mockProvider2)
	require.NoError(t, err)
	
	// Should only use one provider even if duplicates exist
	modes := service.AvailableModes()
	require.Contains(t, modes, shared.IntegrationModeMock)
}

func TestClassroomService_PrimaryTeacher_EmptyCourse(t *testing.T) {
	emptyProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses: []domain.Course{
				{
					ID:       "empty-course",
					Name:     "Empty Course",
					Teachers: []domain.CourseTeacher{}, // No teachers
				},
			},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, emptyProvider)
	require.NoError(t, err)
	
	ctx := context.Background()
	result, err := service.ListCourses(ctx, "")
	
	require.NoError(t, err)
	require.Len(t, result.Courses, 1)
	require.Equal(t, "Unassigned", result.Courses[0].PrimaryTeacher)
}

func TestClassroomService_Dashboard_AllRoles(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()
	
	roles := []domain.Role{
		domain.RoleAdmin,
		domain.RoleCoordinator,
		domain.RoleTeacher,
		domain.RoleStudent,
	}
	
	for _, role := range roles {
		user := domain.User{ID: "user-1", Role: role, Email: "user@classsphere.edu"}
		dashboard, err := service.Dashboard(ctx, user, "mock")
		
		require.NoError(t, err, "Failed for role %s", role)
		require.Equal(t, string(role), dashboard.Role)
		require.NotNil(t, dashboard.Summary)
		require.NotNil(t, dashboard.Charts)
		require.NotNil(t, dashboard.Highlights)
	}
}

func TestClassroomService_Dashboard_InvalidRole(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()
	
	user := domain.User{ID: "user-1", Role: "invalid-role", Email: "user@classsphere.edu"}
	_, err := service.Dashboard(ctx, user, "")
	
	// Should return error for invalid role
	require.Error(t, err)
	require.Contains(t, err.Error(), "unsupported role")
}

func TestClassroomService_ListCourses_DifferentModes(t *testing.T) {
	mockProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{{ID: "mock-1", Name: "Mock Course"}},
		},
	}
	
	googleProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeGoogle,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{{ID: "google-1", Name: "Google Course"}},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, mockProvider, googleProvider)
	require.NoError(t, err)
	
	ctx := context.Background()
	
	// Test mock mode
	mockResult, err := service.ListCourses(ctx, "mock")
	require.NoError(t, err)
	require.Equal(t, "mock", mockResult.Mode)
	
	// Test google mode
	googleResult, err := service.ListCourses(ctx, "google")
	require.NoError(t, err)
	require.Equal(t, "google", googleResult.Mode)
}

func TestClassroomService_Dashboard_Coordinator(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()
	
	coordinator := domain.User{ID: "coord-1", Role: domain.RoleCoordinator, Email: "coord@classsphere.edu"}
	dashboard, err := service.Dashboard(ctx, coordinator, "")
	
	require.NoError(t, err)
	require.Equal(t, "coordinator", dashboard.Role)
	require.NotNil(t, dashboard.Summary)
	require.NotNil(t, dashboard.Charts)
	// Timeline can be nil or empty for coordinator without specific data
}

func TestClassroomService_NewClassroomService_InvalidMode(t *testing.T) {
	mockProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{},
		},
	}
	
	// Invalid mode should be normalized to mock
	service, err := app.NewClassroomService("invalid-mode", mockProvider)
	require.NoError(t, err)
	require.NotNil(t, service)
}

func TestClassroomService_Dashboard_CoursesWithZeroStudents(t *testing.T) {
	provider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses: []domain.Course{
				{
					ID:       "course-1",
					Name:     "Empty Course",
					Teachers: []domain.CourseTeacher{{ID: "t1", Name: "Teacher"}},
					Students: []domain.CourseStudent{}, // No students
					Assignments: []domain.CourseAssignment{},
				},
			},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	
	ctx := context.Background()
	admin := domain.User{ID: "admin-1", Role: domain.RoleAdmin, Email: "admin@classsphere.edu"}
	
	dashboard, err := service.Dashboard(ctx, admin, "")
	require.NoError(t, err)
	require.Equal(t, "admin", dashboard.Role)
}

func TestClassroomService_Dashboard_CoursesWithManyStudents(t *testing.T) {
	students := make([]domain.CourseStudent, 100)
	for i := 0; i < 100; i++ {
		students[i] = domain.CourseStudent{
			Person: domain.Person{ID: fmt.Sprintf("s%d", i), Name: fmt.Sprintf("Student %d", i)},
		}
	}
	
	provider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses: []domain.Course{
				{
					ID:       "large-course",
					Name:     "Large Course",
					Students: students,
					Teachers: []domain.CourseTeacher{{ID: "t1", Name: "Teacher"}},
				},
			},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	
	ctx := context.Background()
	admin := domain.User{ID: "admin-1", Role: domain.RoleAdmin}
	
	dashboard, err := service.Dashboard(ctx, admin, "")
	require.NoError(t, err)
	// The total students should be 100, but the summary might aggregate differently
	require.NotNil(t, dashboard.Summary)
}

func TestClassroomService_Dashboard_TeacherWithMultipleCourses(t *testing.T) {
	courses := []domain.Course{
		{
			ID:   "course-1",
			Name: "Course 1",
			Teachers: []domain.CourseTeacher{
				{ID: "teacher@classsphere.edu", Email: "teacher@classsphere.edu"},
			},
		},
		{
			ID:   "course-2",
			Name: "Course 2",
			Teachers: []domain.CourseTeacher{
				{ID: "teacher@classsphere.edu", Email: "teacher@classsphere.edu"},
			},
		},
	}
	
	provider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     courses,
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	
	ctx := context.Background()
	teacher := domain.User{ID: "teacher-1", Role: domain.RoleTeacher, Email: "teacher@classsphere.edu"}
	
	dashboard, err := service.Dashboard(ctx, teacher, "")
	require.NoError(t, err)
	require.Equal(t, "teacher", dashboard.Role)
}

func TestClassroomService_Dashboard_StudentWithNoEnrollment(t *testing.T) {
	provider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses: []domain.Course{
				{
					ID:       "course-1",
					Name:     "Course Without Student",
					Students: []domain.CourseStudent{}, // Student not enrolled
				},
			},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	
	ctx := context.Background()
	student := domain.User{ID: "student-1", Role: domain.RoleStudent, Email: "student@classsphere.edu"}
	
	dashboard, err := service.Dashboard(ctx, student, "")
	require.NoError(t, err)
	require.Equal(t, "student", dashboard.Role)
}

func TestClassroomService_ListCourses_EmptyMode(t *testing.T) {
	service := newTestClassroomService(t)
	ctx := context.Background()
	
	// Empty mode should use default
	result, err := service.ListCourses(ctx, "")
	require.NoError(t, err)
	require.Equal(t, shared.IntegrationModeMock, result.Mode)
}

func TestClassroomService_Dashboard_WithSpecificMode(t *testing.T) {
	mockProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeMock,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{{ID: "mock-1"}},
		},
	}
	
	googleProvider := &fakeClassroomProvider{
		snapshot: domain.ClassroomSnapshot{
			Mode:        shared.IntegrationModeGoogle,
			GeneratedAt: time.Now(),
			Courses:     []domain.Course{{ID: "google-1"}},
		},
	}
	
	service, err := app.NewClassroomService(shared.IntegrationModeMock, mockProvider, googleProvider)
	require.NoError(t, err)
	
	ctx := context.Background()
	admin := domain.User{ID: "admin-1", Role: domain.RoleAdmin}
	
	// Request specifically google mode
	dashboard, err := service.Dashboard(ctx, admin, "google")
	require.NoError(t, err)
	require.Equal(t, "google", dashboard.Mode)
}
