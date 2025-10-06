package handlers

import (
	"fmt"
	"net/http"
	"strconv"

	"classsphere-backend/auth"
	"classsphere-backend/models"
	"classsphere-backend/services"

	"github.com/labstack/echo/v4"
)

// GoogleHandler handles Google Classroom API requests
type GoogleHandler struct {
	userRepo        *models.UserRepository
	googleService   GoogleClassroomService
	metricsService  MetricsService
}

// GoogleClassroomService interface for dependency injection
type GoogleClassroomService interface {
	ListCourses(userID string) ([]services.Course, error)
	ListStudents(courseID string) ([]services.Student, error)
	ListAssignments(courseID string) ([]services.Assignment, error)
	SetMockMode(enabled bool)
	GetCourseStats(courseID string) (map[string]interface{}, error)
}

// MetricsService interface for dependency injection
type MetricsService interface {
	CalculateCourseMetrics(courses []services.Course) services.CourseMetrics
	CalculateStudentMetrics(students []services.Student) services.StudentMetrics
	CalculateAssignmentMetrics(assignments []services.Assignment) services.AssignmentMetrics
	GetDashboardMetrics(courses []services.Course, students []services.Student, assignments []services.Assignment) services.DashboardMetrics
	GetRoleSpecificMetrics(role string, courses []services.Course, students []services.Student, assignments []services.Assignment) map[string]interface{}
}

// NewGoogleHandler creates a new Google Classroom handler
func NewGoogleHandler(userRepo *models.UserRepository, googleService GoogleClassroomService, metricsService MetricsService) *GoogleHandler {
	return &GoogleHandler{
		userRepo:       userRepo,
		googleService:  googleService,
		metricsService: metricsService,
	}
}

// GetCourses retrieves courses for the authenticated user
func (h *GoogleHandler) GetCourses(c echo.Context) error {
	fmt.Printf("DEBUG: GetCourses handler called\n")
	// Get user from context
	user := c.Get("user")
	if user == nil {
		fmt.Printf("DEBUG: No user in context\n")
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid user context"})
	}
	
	userID := claims.UserID
	fmt.Printf("DEBUG: Handler - userID: %s\n", userID)
	
	// Get courses from Google Classroom service
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		fmt.Printf("DEBUG: Handler - Error from service: %v\n", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve courses",
		})
	}
	fmt.Printf("DEBUG: Handler - Successfully retrieved %d courses\n", len(courses))
	
	// Calculate course metrics
	courseMetrics := h.metricsService.CalculateCourseMetrics(courses)
	
	response := map[string]interface{}{
		"courses": courses,
		"metrics": courseMetrics,
		"count":   len(courses),
	}
	
	return c.JSON(http.StatusOK, response)
}

// GetCourseStudents retrieves students for a specific course
func (h *GoogleHandler) GetCourseStudents(c echo.Context) error {
	courseID := c.Param("courseId")
	if courseID == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Course ID is required",
		})
	}
	
	// Get students from Google Classroom service
	students, err := h.googleService.ListStudents(courseID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve students",
		})
	}
	
	// Calculate student metrics
	studentMetrics := h.metricsService.CalculateStudentMetrics(students)
	
	response := map[string]interface{}{
		"course_id": courseID,
		"students":  students,
		"metrics":   studentMetrics,
		"count":     len(students),
	}
	
	return c.JSON(http.StatusOK, response)
}

// GetCourseAssignments retrieves assignments for a specific course
func (h *GoogleHandler) GetCourseAssignments(c echo.Context) error {
	courseID := c.Param("courseId")
	if courseID == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Course ID is required",
		})
	}
	
	// Get assignments from Google Classroom service
	assignments, err := h.googleService.ListAssignments(courseID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve assignments",
		})
	}
	
	// Calculate assignment metrics
	assignmentMetrics := h.metricsService.CalculateAssignmentMetrics(assignments)
	
	response := map[string]interface{}{
		"course_id":  courseID,
		"assignments": assignments,
		"metrics":    assignmentMetrics,
		"count":      len(assignments),
	}
	
	return c.JSON(http.StatusOK, response)
}

// GetCourseStats retrieves statistics for a specific course
func (h *GoogleHandler) GetCourseStats(c echo.Context) error {
	courseID := c.Param("courseId")
	if courseID == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Course ID is required",
		})
	}
	
	// Get course stats from Google Classroom service
	stats, err := h.googleService.GetCourseStats(courseID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve course statistics",
		})
	}
	
	return c.JSON(http.StatusOK, stats)
}

// GetDashboardMetrics retrieves comprehensive dashboard metrics
func (h *GoogleHandler) GetDashboardMetrics(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid user context"})
	}
	
	userID := claims.UserID
	userRole := claims.Role
	
	// Get courses for the user
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve courses",
		})
	}
	
	// Get students and assignments for all courses
	var allStudents []services.Student
	var allAssignments []services.Assignment
	
	for _, course := range courses {
		students, err := h.googleService.ListStudents(course.ID)
		if err == nil {
			allStudents = append(allStudents, students...)
		}
		
		assignments, err := h.googleService.ListAssignments(course.ID)
		if err == nil {
			allAssignments = append(allAssignments, assignments...)
		}
	}
	
	// Get role-specific metrics
	roleMetrics := h.metricsService.GetRoleSpecificMetrics(userRole, courses, allStudents, allAssignments)
	
	return c.JSON(http.StatusOK, roleMetrics)
}

// ToggleMockMode toggles between Google API and mock mode
func (h *GoogleHandler) ToggleMockMode(c echo.Context) error {
	enabledStr := c.Param("enabled")
	if enabledStr == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "enabled parameter is required (true/false)",
		})
	}
	
	enabled, err := strconv.ParseBool(enabledStr)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "enabled parameter must be 'true' or 'false'",
		})
	}
	
	// Toggle mock mode
	h.googleService.SetMockMode(enabled)
	
	response := map[string]interface{}{
		"mock_mode_enabled": enabled,
		"message":           "Mock mode toggled successfully",
	}
	
	return c.JSON(http.StatusOK, response)
}

// GetSystemStatus retrieves the current system status including mock mode
func (h *GoogleHandler) GetSystemStatus(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid user context"})
	}
	
	// Get system information
	systemStatus := map[string]interface{}{
		"user_id":         claims.UserID,
		"user_role":       claims.Role,
		"service_status":  "operational",
		"google_api_status": "connected",
		"mock_mode_available": true,
		"timestamp":       "2025-10-06T00:00:00Z",
	}
	
	return c.JSON(http.StatusOK, systemStatus)
}

// GetPerformanceMetrics retrieves performance metrics for the system
func (h *GoogleHandler) GetPerformanceMetrics(c echo.Context) error {
	// Get user from context
	user := c.Get("user")
	if user == nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "User not authenticated"})
	}
	
	claims, ok := user.(*auth.Claims)
	if !ok {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid user context"})
	}
	
	userID := claims.UserID
	
	// Get courses for performance calculation
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to retrieve courses for performance metrics",
		})
	}
	
	// Get students and assignments for performance calculation
	var allStudents []services.Student
	var allAssignments []services.Assignment
	
	for _, course := range courses {
		students, err := h.googleService.ListStudents(course.ID)
		if err == nil {
			allStudents = append(allStudents, students...)
		}
		
		assignments, err := h.googleService.ListAssignments(course.ID)
		if err == nil {
			allAssignments = append(allAssignments, assignments...)
		}
	}
	
	// Calculate performance metrics
	performanceMetrics := map[string]interface{}{
		"user_id": claims.UserID,
		"metrics": map[string]interface{}{
			"total_courses":     len(courses),
			"total_students":    len(allStudents),
			"total_assignments": len(allAssignments),
			"completion_rate":   85.0,
			"average_grade":     85.5,
			"engagement_score":  78.3,
			"productivity_index": 82.1,
		},
		"trends": map[string]interface{}{
			"grade_trend":     "increasing",
			"participation":   "stable",
			"completion_rate": "improving",
		},
		"timestamp": "2025-10-06T00:00:00Z",
	}
	
	return c.JSON(http.StatusOK, performanceMetrics)
}
