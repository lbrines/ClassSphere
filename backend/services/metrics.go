package services

import (
	"math"
)

// MetricsService handles calculation of educational metrics
type MetricsService struct{}

// NewMetricsService creates a new metrics service
func NewMetricsService() *MetricsService {
	return &MetricsService{}
}

// CourseMetrics represents metrics for courses
type CourseMetrics struct {
	TotalCourses      int     `json:"total_courses"`
	ActiveCourses     int     `json:"active_courses"`
	ArchivedCourses   int     `json:"archived_courses"`
	TotalStudents     int     `json:"total_students"`
	AverageGrade      float64 `json:"average_grade"`
	TotalAssignments  int     `json:"total_assignments"`
}

// StudentMetrics represents metrics for students
type StudentMetrics struct {
	TotalStudents   int `json:"total_students"`
	ActiveStudents  int `json:"active_students"`
}

// AssignmentMetrics represents metrics for assignments
type AssignmentMetrics struct {
	TotalAssignments      int     `json:"total_assignments"`
	PublishedAssignments  int     `json:"published_assignments"`
	DraftAssignments      int     `json:"draft_assignments"`
	TotalPoints           int     `json:"total_points"`
	AveragePoints         float64 `json:"average_points"`
}

// DashboardMetrics represents combined dashboard metrics
type DashboardMetrics struct {
	Courses     CourseMetrics     `json:"courses"`
	Students    StudentMetrics    `json:"students"`
	Assignments AssignmentMetrics `json:"assignments"`
}

// CalculateCourseMetrics calculates metrics for a list of courses
func (s *MetricsService) CalculateCourseMetrics(courses []Course) CourseMetrics {
	metrics := CourseMetrics{}

	if len(courses) == 0 {
		return metrics
	}

	metrics.TotalCourses = len(courses)
	
	// Count active and archived courses
	for _, course := range courses {
		if course.CourseState == "ACTIVE" {
			metrics.ActiveCourses++
		} else if course.CourseState == "ARCHIVED" {
			metrics.ArchivedCourses++
		}
	}

	// For active courses, calculate total students and assignments
	// Using mock data: 8 students per course, 6 assignments per course
	metrics.TotalStudents = metrics.ActiveCourses * 8
	metrics.TotalAssignments = metrics.ActiveCourses * 6
	
	// Mock average grade
	metrics.AverageGrade = 85.5

	return metrics
}

// CalculateStudentMetrics calculates metrics for a list of students
func (s *MetricsService) CalculateStudentMetrics(students []Student) StudentMetrics {
	metrics := StudentMetrics{}

	if len(students) == 0 {
		return metrics
	}

	metrics.TotalStudents = len(students)
	metrics.ActiveStudents = len(students) // All students are considered active in mock data

	return metrics
}

// CalculateAssignmentMetrics calculates metrics for a list of assignments
func (s *MetricsService) CalculateAssignmentMetrics(assignments []Assignment) AssignmentMetrics {
	metrics := AssignmentMetrics{}

	if len(assignments) == 0 {
		return metrics
	}

	metrics.TotalAssignments = len(assignments)
	
	totalPoints := 0
	
	// Count published and draft assignments, calculate total points
	for _, assignment := range assignments {
		if assignment.State == "PUBLISHED" {
			metrics.PublishedAssignments++
		} else if assignment.State == "DRAFT" {
			metrics.DraftAssignments++
		}
		
		totalPoints += assignment.MaxPoints
	}

	metrics.TotalPoints = totalPoints
	
	// Calculate average points
	if metrics.TotalAssignments > 0 {
		metrics.AveragePoints = math.Round(float64(totalPoints)/float64(metrics.TotalAssignments)*100) / 100
	}

	return metrics
}

// GetDashboardMetrics calculates combined dashboard metrics
func (s *MetricsService) GetDashboardMetrics(courses []Course, students []Student, assignments []Assignment) DashboardMetrics {
	return DashboardMetrics{
		Courses:     s.CalculateCourseMetrics(courses),
		Students:    s.CalculateStudentMetrics(students),
		Assignments: s.CalculateAssignmentMetrics(assignments),
	}
}

// GetRoleSpecificMetrics calculates metrics specific to user roles
func (s *MetricsService) GetRoleSpecificMetrics(role string, courses []Course, students []Student, assignments []Assignment) map[string]interface{} {
	baseMetrics := s.GetDashboardMetrics(courses, students, assignments)
	
	roleMetrics := map[string]interface{}{
		"role":     role,
		"base":     baseMetrics,
		"specific": map[string]interface{}{},
	}

	switch role {
	case "student":
		roleMetrics["specific"] = map[string]interface{}{
			"my_courses":        len(courses),
			"pending_assignments": s.countPendingAssignments(assignments),
			"completed_assignments": s.countCompletedAssignments(assignments),
			"average_grade":     baseMetrics.Courses.AverageGrade,
		}
	case "teacher":
		roleMetrics["specific"] = map[string]interface{}{
			"my_courses":        len(courses),
			"total_students":    baseMetrics.Students.TotalStudents,
			"graded_assignments": s.countGradedAssignments(assignments),
			"pending_grades":    s.countPendingGrades(assignments),
		}
	case "coordinator":
		roleMetrics["specific"] = map[string]interface{}{
			"total_courses":     baseMetrics.Courses.TotalCourses,
			"total_teachers":    s.estimateTeachers(courses),
			"total_students":    baseMetrics.Students.TotalStudents,
			"active_programs":   s.countActivePrograms(courses),
		}
	case "admin":
		roleMetrics["specific"] = map[string]interface{}{
			"total_users":       baseMetrics.Students.TotalStudents + s.estimateTeachers(courses),
			"total_courses":     baseMetrics.Courses.TotalCourses,
			"system_health":     "healthy",
			"uptime_percentage": 99.9,
		}
	}

	return roleMetrics
}

// Helper methods for role-specific calculations

func (s *MetricsService) countPendingAssignments(assignments []Assignment) int {
	// Mock implementation: assume 30% of assignments are pending
	return int(math.Ceil(float64(len(assignments)) * 0.3))
}

func (s *MetricsService) countCompletedAssignments(assignments []Assignment) int {
	// Mock implementation: assume 70% of assignments are completed
	return int(math.Floor(float64(len(assignments)) * 0.7))
}

func (s *MetricsService) countGradedAssignments(assignments []Assignment) int {
	// Mock implementation: assume 60% of assignments are graded
	return int(math.Floor(float64(len(assignments)) * 0.6))
}

func (s *MetricsService) countPendingGrades(assignments []Assignment) int {
	// Mock implementation: assume 40% of assignments are pending grades
	return int(math.Ceil(float64(len(assignments)) * 0.4))
}

func (s *MetricsService) estimateTeachers(courses []Course) int {
	// Mock implementation: assume each teacher handles 2 courses on average
	if len(courses) == 0 {
		return 0
	}
	return int(math.Ceil(float64(len(courses)) / 2.0))
}

func (s *MetricsService) countActivePrograms(courses []Course) int {
	// Mock implementation: assume 3 active programs
	return 3
}

// GetPerformanceMetrics calculates performance-related metrics
func (s *MetricsService) GetPerformanceMetrics(courses []Course, students []Student, assignments []Assignment) map[string]interface{} {
	return map[string]interface{}{
		"completion_rate":     s.calculateCompletionRate(assignments),
		"average_grade":       s.calculateAverageGrade(),
		"engagement_score":    s.calculateEngagementScore(courses, students),
		"productivity_index":  s.calculateProductivityIndex(assignments),
		"trends": map[string]interface{}{
			"grade_trend":      "increasing",
			"participation":    "stable",
			"completion_rate":  "improving",
		},
	}
}

func (s *MetricsService) calculateCompletionRate(assignments []Assignment) float64 {
	// Mock implementation: 85% completion rate
	return 85.0
}

func (s *MetricsService) calculateAverageGrade() float64 {
	// Mock implementation: average grade of 85.5
	return 85.5
}

func (s *MetricsService) calculateEngagementScore(courses []Course, students []Student) float64 {
	// Mock implementation: engagement score based on course and student count
	if len(courses) == 0 || len(students) == 0 {
		return 0.0
	}
	
	// Simple calculation: engagement = (courses * students) / 100
	engagement := float64(len(courses) * len(students)) / 100.0
	
	// Cap at 100
	if engagement > 100.0 {
		engagement = 100.0
	}
	
	return math.Round(engagement*100) / 100
}

func (s *MetricsService) calculateProductivityIndex(assignments []Assignment) float64 {
	// Mock implementation: productivity based on assignment count and points
	if len(assignments) == 0 {
		return 0.0
	}
	
	totalPoints := 0
	for _, assignment := range assignments {
		totalPoints += assignment.MaxPoints
	}
	
	// Simple calculation: productivity = (assignments * avg_points) / 10
	avgPoints := float64(totalPoints) / float64(len(assignments))
	productivity := float64(len(assignments)) * avgPoints / 10.0
	
	// Cap at 100
	if productivity > 100.0 {
		productivity = 100.0
	}
	
	return math.Round(productivity*100) / 100
}
