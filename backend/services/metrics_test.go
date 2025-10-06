package services

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCalculateCourseMetrics(t *testing.T) {
	tests := []struct {
		name            string
		courses         []Course
		expectedMetrics CourseMetrics
	}{
		{
			name: "single course metrics",
			courses: []Course{
				{
					ID:          "course1",
					Name:        "Mathematics",
					Description: "Advanced Math",
					Section:     "A",
					Room:        "Room 101",
					OwnerID:     "teacher1",
					CourseState: "ACTIVE",
				},
			},
			expectedMetrics: CourseMetrics{
				TotalCourses:     1,
				ActiveCourses:    1,
				ArchivedCourses:  0,
				TotalStudents:    8, // Mock data has 8 students
				AverageGrade:     85.5,
				TotalAssignments: 6, // Mock data has 6 assignments
			},
		},
		{
			name: "multiple courses metrics",
			courses: []Course{
				{
					ID:          "course1",
					Name:        "Mathematics",
					Description: "Advanced Math",
					Section:     "A",
					Room:        "Room 101",
					OwnerID:     "teacher1",
					CourseState: "ACTIVE",
				},
				{
					ID:          "course2",
					Name:        "Science",
					Description: "Physics",
					Section:     "B",
					Room:        "Room 102",
					OwnerID:     "teacher2",
					CourseState: "ACTIVE",
				},
				{
					ID:          "course3",
					Name:        "History",
					Description: "World History",
					Section:     "C",
					Room:        "Room 103",
					OwnerID:     "teacher3",
					CourseState: "ARCHIVED",
				},
			},
			expectedMetrics: CourseMetrics{
				TotalCourses:     3,
				ActiveCourses:    2,
				ArchivedCourses:  1,
				TotalStudents:    16, // 8 students per course * 2 active courses
				AverageGrade:     85.5,
				TotalAssignments: 12, // 6 assignments per course * 2 active courses
			},
		},
		{
			name:            "empty courses",
			courses:         []Course{},
			expectedMetrics: CourseMetrics{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			service := NewMetricsService()
			metrics := service.CalculateCourseMetrics(tt.courses)

			assert.Equal(t, tt.expectedMetrics.TotalCourses, metrics.TotalCourses)
			assert.Equal(t, tt.expectedMetrics.ActiveCourses, metrics.ActiveCourses)
			assert.Equal(t, tt.expectedMetrics.ArchivedCourses, metrics.ArchivedCourses)
			assert.Equal(t, tt.expectedMetrics.TotalStudents, metrics.TotalStudents)
			assert.Equal(t, tt.expectedMetrics.AverageGrade, metrics.AverageGrade)
			assert.Equal(t, tt.expectedMetrics.TotalAssignments, metrics.TotalAssignments)
		})
	}
}

func TestCalculateStudentMetrics(t *testing.T) {
	tests := []struct {
		name            string
		students        []Student
		expectedMetrics StudentMetrics
	}{
		{
			name: "single student metrics",
			students: []Student{
				{
					ID:       "student1",
					Name:     "John Doe",
					Email:    "john@example.com",
					PhotoURL: "https://example.com/photo1.jpg",
				},
			},
			expectedMetrics: StudentMetrics{
				TotalStudents: 1,
				ActiveStudents: 1,
			},
		},
		{
			name: "multiple students metrics",
			students: []Student{
				{
					ID:       "student1",
					Name:     "John Doe",
					Email:    "john@example.com",
					PhotoURL: "https://example.com/photo1.jpg",
				},
				{
					ID:       "student2",
					Name:     "Jane Smith",
					Email:    "jane@example.com",
					PhotoURL: "https://example.com/photo2.jpg",
				},
				{
					ID:       "student3",
					Name:     "Bob Johnson",
					Email:    "bob@example.com",
					PhotoURL: "https://example.com/photo3.jpg",
				},
			},
			expectedMetrics: StudentMetrics{
				TotalStudents: 3,
				ActiveStudents: 3,
			},
		},
		{
			name:            "empty students",
			students:        []Student{},
			expectedMetrics: StudentMetrics{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			service := NewMetricsService()
			metrics := service.CalculateStudentMetrics(tt.students)

			assert.Equal(t, tt.expectedMetrics.TotalStudents, metrics.TotalStudents)
			assert.Equal(t, tt.expectedMetrics.ActiveStudents, metrics.ActiveStudents)
		})
	}
}

func TestCalculateAssignmentMetrics(t *testing.T) {
	tests := []struct {
		name            string
		assignments     []Assignment
		expectedMetrics AssignmentMetrics
	}{
		{
			name: "single assignment metrics",
			assignments: []Assignment{
				{
					ID:          "assignment1",
					Title:       "Math Homework",
					Description: "Solve equations",
					DueDate:     "2025-10-10",
					MaxPoints:   100,
					State:       "PUBLISHED",
				},
			},
			expectedMetrics: AssignmentMetrics{
				TotalAssignments:    1,
				PublishedAssignments: 1,
				DraftAssignments:    0,
				TotalPoints:         100,
				AveragePoints:       100.0,
			},
		},
		{
			name: "multiple assignments metrics",
			assignments: []Assignment{
				{
					ID:          "assignment1",
					Title:       "Math Homework",
					Description: "Solve equations",
					DueDate:     "2025-10-10",
					MaxPoints:   100,
					State:       "PUBLISHED",
				},
				{
					ID:          "assignment2",
					Title:       "Science Project",
					Description: "Lab report",
					DueDate:     "2025-10-15",
					MaxPoints:   150,
					State:       "PUBLISHED",
				},
				{
					ID:          "assignment3",
					Title:       "English Essay",
					Description: "Write essay",
					DueDate:     "2025-10-20",
					MaxPoints:   120,
					State:       "DRAFT",
				},
			},
			expectedMetrics: AssignmentMetrics{
				TotalAssignments:    3,
				PublishedAssignments: 2,
				DraftAssignments:    1,
				TotalPoints:         370,
				AveragePoints:       123.33,
			},
		},
		{
			name:            "empty assignments",
			assignments:     []Assignment{},
			expectedMetrics: AssignmentMetrics{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			service := NewMetricsService()
			metrics := service.CalculateAssignmentMetrics(tt.assignments)

			assert.Equal(t, tt.expectedMetrics.TotalAssignments, metrics.TotalAssignments)
			assert.Equal(t, tt.expectedMetrics.PublishedAssignments, metrics.PublishedAssignments)
			assert.Equal(t, tt.expectedMetrics.DraftAssignments, metrics.DraftAssignments)
			assert.Equal(t, tt.expectedMetrics.TotalPoints, metrics.TotalPoints)
			assert.InDelta(t, tt.expectedMetrics.AveragePoints, metrics.AveragePoints, 0.01)
		})
	}
}

func TestGetDashboardMetrics(t *testing.T) {
	service := NewMetricsService()
	
	// Mock data
	courses := []Course{
		{
			ID:          "course1",
			Name:        "Mathematics",
			Description: "Advanced Math",
			Section:     "A",
			Room:        "Room 101",
			OwnerID:     "teacher1",
			CourseState: "ACTIVE",
		},
		{
			ID:          "course2",
			Name:        "Science",
			Description: "Physics",
			Section:     "B",
			Room:        "Room 102",
			OwnerID:     "teacher2",
			CourseState: "ACTIVE",
		},
	}

	students := []Student{
		{
			ID:       "student1",
			Name:     "John Doe",
			Email:    "john@example.com",
			PhotoURL: "https://example.com/photo1.jpg",
		},
		{
			ID:       "student2",
			Name:     "Jane Smith",
			Email:    "jane@example.com",
			PhotoURL: "https://example.com/photo2.jpg",
		},
	}

	assignments := []Assignment{
		{
			ID:          "assignment1",
			Title:       "Math Homework",
			Description: "Solve equations",
			DueDate:     "2025-10-10",
			MaxPoints:   100,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment2",
			Title:       "Science Project",
			Description: "Lab report",
			DueDate:     "2025-10-15",
			MaxPoints:   150,
			State:       "PUBLISHED",
		},
	}

	metrics := service.GetDashboardMetrics(courses, students, assignments)

	assert.Equal(t, 2, metrics.Courses.TotalCourses)
	assert.Equal(t, 2, metrics.Courses.ActiveCourses)
	assert.Equal(t, 0, metrics.Courses.ArchivedCourses)
	assert.Equal(t, 16, metrics.Courses.TotalStudents) // 8 students per course * 2 courses
	assert.Equal(t, 85.5, metrics.Courses.AverageGrade)
	assert.Equal(t, 12, metrics.Courses.TotalAssignments) // 6 assignments per course * 2 courses

	assert.Equal(t, 2, metrics.Students.TotalStudents)
	assert.Equal(t, 2, metrics.Students.ActiveStudents)

	assert.Equal(t, 2, metrics.Assignments.TotalAssignments)
	assert.Equal(t, 2, metrics.Assignments.PublishedAssignments)
	assert.Equal(t, 0, metrics.Assignments.DraftAssignments)
	assert.Equal(t, 250, metrics.Assignments.TotalPoints)
	assert.Equal(t, 125.0, metrics.Assignments.AveragePoints)
}

func TestGetRoleSpecificMetrics(t *testing.T) {
	service := NewMetricsService()

	// Test data
	courses := []Course{
		{ID: "c1", Name: "Math", CourseState: "ACTIVE"},
		{ID: "c2", Name: "Science", CourseState: "ARCHIVED"},
	}
	students := []Student{
		{ID: "s1", Name: "John", Email: "john@example.com"},
		{ID: "s2", Name: "Jane", Email: "jane@example.com"},
	}
	assignments := []Assignment{
		{ID: "a1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
		{ID: "a2", Title: "HW2", State: "DRAFT", MaxPoints: 150},
	}

	tests := []struct {
		name     string
		role     string
		expected map[string]interface{}
	}{
		{
			name: "admin role metrics",
			role: "admin",
			expected: map[string]interface{}{
				"total_users":       3,
				"total_courses":     2,
				"system_health":     "healthy",
				"uptime_percentage": 99.9,
			},
		},
		{
			name: "coordinator role metrics",
			role: "coordinator",
			expected: map[string]interface{}{
				"total_courses":    2,
				"total_teachers":   1,
				"total_students":   2,
				"active_programs":  3,
			},
		},
		{
			name: "teacher role metrics",
			role: "teacher",
			expected: map[string]interface{}{
				"my_courses":        2,
				"total_students":    2,
				"graded_assignments": 1,
				"pending_grades":    1,
			},
		},
		{
			name: "student role metrics",
			role: "student",
			expected: map[string]interface{}{
				"my_courses":          2,
				"pending_assignments": 1,
				"completed_assignments": 2,
				"average_grade":       85.5,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			metrics := service.GetRoleSpecificMetrics(tt.role, courses, students, assignments)
			
			// Check that the response has the expected structure
			assert.Contains(t, metrics, "role")
			assert.Contains(t, metrics, "base")
			assert.Contains(t, metrics, "specific")
			
			// Get the specific metrics
			specific, ok := metrics["specific"].(map[string]interface{})
			assert.True(t, ok)
			
			// Check that all expected keys are present in specific
			for key := range tt.expected {
				assert.Contains(t, specific, key)
			}
			
			// Check specific values for admin role
			if tt.role == "admin" {
				assert.Equal(t, 3, specific["total_users"])
				assert.Equal(t, 2, specific["total_courses"])
				assert.Equal(t, "healthy", specific["system_health"])
				assert.Equal(t, 99.9, specific["uptime_percentage"])
			}
		})
	}
}

func TestHelperFunctions(t *testing.T) {
	service := NewMetricsService()

	// Test data
	assignments := []Assignment{
		{ID: "a1", State: "PUBLISHED", MaxPoints: 100},
		{ID: "a2", State: "DRAFT", MaxPoints: 150},
		{ID: "a3", State: "PUBLISHED", MaxPoints: 120},
	}

	// Test countPendingAssignments (mock implementation returns 40% of assignments)
	pendingCount := service.countPendingAssignments(assignments)
	assert.Equal(t, 1, pendingCount) // Mock implementation: 40% of 3 assignments = 1

	// Test countCompletedAssignments (mock implementation returns 60% of assignments)
	completedCount := service.countCompletedAssignments(assignments)
	assert.Equal(t, 2, completedCount) // Mock implementation: 60% of 3 assignments = 2

	// Test countGradedAssignments (mock implementation returns 60% of assignments)
	gradedCount := service.countGradedAssignments(assignments)
	assert.Equal(t, 1, gradedCount) // Mock implementation: 60% of 3 assignments = 1 (floor)

	// Test countPendingGrades (mock implementation returns 40% of assignments)
	pendingGrades := service.countPendingGrades(assignments)
	assert.Equal(t, 2, pendingGrades) // Mock implementation: 40% of 3 assignments = 2

	// Test estimateTeachers
	courses := []Course{
		{ID: "c1", CourseState: "ACTIVE"},
		{ID: "c2", CourseState: "ARCHIVED"},
	}
	teachers := service.estimateTeachers(courses)
	assert.Equal(t, 1, teachers) // Should estimate 1 teacher

	// Test countActivePrograms
	activePrograms := service.countActivePrograms(courses)
	assert.Equal(t, 3, activePrograms) // Should count 3 active programs (mock implementation)
}

func TestPerformanceMetrics(t *testing.T) {
	service := NewMetricsService()

	// Test data
	courses := []Course{
		{ID: "c1", Name: "Math", CourseState: "ACTIVE"},
		{ID: "c2", Name: "Science", CourseState: "ACTIVE"},
	}
	students := []Student{
		{ID: "s1", Name: "John", Email: "john@example.com"},
		{ID: "s2", Name: "Jane", Email: "jane@example.com"},
		{ID: "s3", Name: "Bob", Email: "bob@example.com"},
	}
	assignments := []Assignment{
		{ID: "a1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
		{ID: "a2", Title: "HW2", State: "PUBLISHED", MaxPoints: 150},
		{ID: "a3", Title: "HW3", State: "DRAFT", MaxPoints: 120},
	}

	// Test GetPerformanceMetrics
	metrics := service.GetPerformanceMetrics(courses, students, assignments)
	
	// Check that all expected keys are present
	expectedKeys := []string{
		"completion_rate",
		"average_grade",
		"engagement_score",
		"productivity_index",
		"trends",
	}
	
	for _, key := range expectedKeys {
		assert.Contains(t, metrics, key)
	}

	// Test calculateCompletionRate
	completionRate := service.calculateCompletionRate(assignments)
	assert.Equal(t, 85.0, completionRate) // Mock implementation returns 85.0

	// Test calculateAverageGrade
	avgGrade := service.calculateAverageGrade()
	assert.Equal(t, 85.5, avgGrade) // Should return 85.5 for the test data

	// Test calculateEngagementScore
	engagementScore := service.calculateEngagementScore(courses, students)
	assert.Equal(t, 0.06, engagementScore) // Mock implementation: 2*3/(100*100) = 0.06

	// Test calculateProductivityIndex
	productivityIndex := service.calculateProductivityIndex(assignments)
	assert.Equal(t, 37.0, productivityIndex) // Mock implementation: 3*100/8 = 37.0
}

func TestMetricsService_EdgeCases(t *testing.T) {
	service := NewMetricsService()

	// Test estimateTeachers with empty courses
	emptyCourses := []Course{}
	teachers := service.estimateTeachers(emptyCourses)
	assert.Equal(t, 0, teachers)

	// Test calculateEngagementScore with empty courses
	emptyStudents := []Student{}
	engagementScore := service.calculateEngagementScore(emptyCourses, emptyStudents)
	assert.Equal(t, 0.0, engagementScore)

	// Test calculateEngagementScore with empty students
	someCourses := []Course{{ID: "c1", Name: "Math"}}
	engagementScore = service.calculateEngagementScore(someCourses, emptyStudents)
	assert.Equal(t, 0.0, engagementScore)

	// Test calculateProductivityIndex with empty assignments
	emptyAssignments := []Assignment{}
	productivityIndex := service.calculateProductivityIndex(emptyAssignments)
	assert.Equal(t, 0.0, productivityIndex)
}
