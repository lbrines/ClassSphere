package handlers

import (
	"net/http"
	"strconv"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"
	"classsphere-backend/services"

	"github.com/labstack/echo/v4"
)

// GoogleClassroomService and MetricsService interfaces are defined in google.go

// UserRepository interface for dependency injection
type UserRepository interface {
	GetUserByID(id uint) (*models.User, error)
	GetUserByEmail(email string) (*models.User, error)
	CreateUser(user *models.User) error
	UpdateUser(user *models.User) error
	DeleteUser(id uint) error
	ListUsers(offset, limit int) ([]*models.User, error)
	GetUserCount() (int64, error)
	DeactivateUser(id uint) error
	ActivateUser(id uint) error
}

type DashboardHandler struct {
	userRepo       UserRepository
	googleService  GoogleClassroomService
	metricsService MetricsService
}

func NewDashboardHandler(userRepo UserRepository) *DashboardHandler {
	return &DashboardHandler{
		userRepo: userRepo,
	}
}

// NewEnhancedDashboardHandler creates a dashboard handler with Google services
func NewEnhancedDashboardHandler(userRepo UserRepository, googleService GoogleClassroomService, metricsService MetricsService) *DashboardHandler {
	return &DashboardHandler{
		userRepo:       userRepo,
		googleService:  googleService,
		metricsService: metricsService,
	}
}

// GetStudentDashboard returns student-specific dashboard data
func (h *DashboardHandler) GetStudentDashboard(c echo.Context) error {
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
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid user ID"})
	}
	
	// Get user info
	dbUser, err := h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "User not found"})
	}

	// If Google services are available, use them
	if h.googleService != nil && h.metricsService != nil {
		return h.getEnhancedStudentDashboard(c, dbUser, userID)
	}

	// Fallback to mock data
	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "student",
			"welcome_message": "Welcome to your student dashboard!",
			"stats": map[string]interface{}{
				"total_courses": 3,
				"assignments_pending": 5,
				"assignments_completed": 12,
				"average_grade": 85.5,
			},
			"recent_activities": []map[string]interface{}{
				{
					"type": "assignment_submitted",
					"title": "Math Homework #3",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
					"status": "submitted",
				},
				{
					"type": "grade_received",
					"title": "Science Quiz",
					"date": time.Now().AddDate(0, 0, -2).Format("2006-01-02"),
					"grade": 92,
				},
			},
			"upcoming_deadlines": []map[string]interface{}{
				{
					"title": "History Essay",
					"due_date": time.Now().AddDate(0, 0, 3).Format("2006-01-02"),
					"course": "World History",
				},
				{
					"title": "Math Test",
					"due_date": time.Now().AddDate(0, 0, 5).Format("2006-01-02"),
					"course": "Algebra II",
				},
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// getEnhancedStudentDashboard returns student dashboard with Google Classroom integration
func (h *DashboardHandler) getEnhancedStudentDashboard(c echo.Context, dbUser *models.User, userID string) error {
	// Get courses from Google Classroom
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		// Fallback to mock data if Google service fails
		return h.getFallbackStudentDashboard(c, dbUser)
	}

	// Get all assignments from all courses
	var allAssignments []services.Assignment
	for _, course := range courses {
		assignments, err := h.googleService.ListAssignments(course.ID)
		if err != nil {
			continue // Skip courses with assignment errors
		}
		allAssignments = append(allAssignments, assignments...)
	}

	// Calculate metrics
	courseMetrics := h.metricsService.CalculateCourseMetrics(courses)
	assignmentMetrics := h.metricsService.CalculateAssignmentMetrics(allAssignments)
	roleMetrics := h.metricsService.GetRoleSpecificMetrics("student", courses, []services.Student{}, allAssignments)

	// Prepare upcoming deadlines from assignments
	upcomingDeadlines := []map[string]interface{}{}
	for _, assignment := range allAssignments {
		if assignment.State == "PUBLISHED" && assignment.DueDate != "" {
			// Find course name for this assignment
			courseName := "Unknown Course"
			for _, course := range courses {
				if course.ID == assignment.ID { // This is a simplified match
					courseName = course.Name
					break
				}
			}
			
			upcomingDeadlines = append(upcomingDeadlines, map[string]interface{}{
				"title":    assignment.Title,
				"due_date": assignment.DueDate,
				"course":   courseName,
				"points":   assignment.MaxPoints,
			})
		}
	}

	// Prepare recent activities (mock for now)
	recentActivities := []map[string]interface{}{
		{
			"type": "assignment_submitted",
			"title": "Math Homework #3",
			"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
			"status": "submitted",
		},
		{
			"type": "grade_received",
			"title": "Science Quiz",
			"date": time.Now().AddDate(0, 0, -2).Format("2006-01-02"),
			"grade": 92,
		},
	}

	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "student",
			"welcome_message": "Welcome to your student dashboard!",
			"stats": map[string]interface{}{
				"total_courses":          courseMetrics.TotalCourses,
				"assignments_pending":    assignmentMetrics.TotalAssignments - assignmentMetrics.PublishedAssignments,
				"assignments_completed":  assignmentMetrics.PublishedAssignments,
				"average_grade":          courseMetrics.AverageGrade,
			},
			"recent_activities": recentActivities,
			"upcoming_deadlines": upcomingDeadlines,
			"google_integration": map[string]interface{}{
				"enabled": true,
				"courses_count": len(courses),
				"assignments_count": len(allAssignments),
			},
		},
		"metrics": map[string]interface{}{
			"course_metrics": courseMetrics,
			"assignment_metrics": assignmentMetrics,
			"role_specific": roleMetrics,
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// getFallbackStudentDashboard returns mock student dashboard data
func (h *DashboardHandler) getFallbackStudentDashboard(c echo.Context, dbUser *models.User) error {
	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "student",
			"welcome_message": "Welcome to your student dashboard!",
			"stats": map[string]interface{}{
				"total_courses": 3,
				"assignments_pending": 5,
				"assignments_completed": 12,
				"average_grade": 85.5,
			},
			"google_integration": map[string]interface{}{
				"enabled": false,
				"fallback": true,
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// GetTeacherDashboard returns teacher-specific dashboard data
func (h *DashboardHandler) GetTeacherDashboard(c echo.Context) error {
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
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid user ID"})
	}
	
	// Get user info
	dbUser, err := h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "User not found"})
	}

	// If Google services are available, use them
	if h.googleService != nil && h.metricsService != nil {
		return h.getEnhancedTeacherDashboard(c, dbUser, userID)
	}

	// Fallback to mock data
	return h.getFallbackTeacherDashboard(c, dbUser)
}

// GetCoordinatorDashboard returns coordinator-specific dashboard data
func (h *DashboardHandler) GetCoordinatorDashboard(c echo.Context) error {
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
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid user ID"})
	}
	
	// Get user info
	dbUser, err := h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "User not found"})
	}

	// If Google services are available, use them
	if h.googleService != nil && h.metricsService != nil {
		return h.getEnhancedCoordinatorDashboard(c, dbUser, userID)
	}

	// Fallback to mock data
	return h.getFallbackCoordinatorDashboard(c, dbUser)
}

// GetAdminDashboard returns admin-specific dashboard data
func (h *DashboardHandler) GetAdminDashboard(c echo.Context) error {
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
	
	// Convert string to uint
	id, err := strconv.ParseUint(userID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid user ID"})
	}
	
	// Get user info
	dbUser, err := h.userRepo.GetUserByID(uint(id))
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "User not found"})
	}

	// If Google services are available, use them
	if h.googleService != nil && h.metricsService != nil {
		return h.getEnhancedAdminDashboard(c, dbUser, userID)
	}

	// Fallback to mock data
	return h.getFallbackAdminDashboard(c, dbUser)
}

// getEnhancedTeacherDashboard returns teacher dashboard with Google Classroom integration
func (h *DashboardHandler) getEnhancedTeacherDashboard(c echo.Context, dbUser *models.User, userID string) error {
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		return h.getFallbackTeacherDashboard(c, dbUser)
	}

	var allStudents []services.Student
	var allAssignments []services.Assignment
	for _, course := range courses {
		students, err := h.googleService.ListStudents(course.ID)
		if err != nil {
			continue
		}
		allStudents = append(allStudents, students...)

		assignments, err := h.googleService.ListAssignments(course.ID)
		if err != nil {
			continue
		}
		allAssignments = append(allAssignments, assignments...)
	}

	courseMetrics := h.metricsService.CalculateCourseMetrics(courses)
	studentMetrics := h.metricsService.CalculateStudentMetrics(allStudents)
	assignmentMetrics := h.metricsService.CalculateAssignmentMetrics(allAssignments)
	roleMetrics := h.metricsService.GetRoleSpecificMetrics("teacher", courses, allStudents, allAssignments)

	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "teacher",
			"welcome_message": "Welcome to your teacher dashboard!",
			"stats": map[string]interface{}{
				"total_courses":     courseMetrics.TotalCourses,
				"total_students":    studentMetrics.TotalStudents,
				"graded_assignments": assignmentMetrics.PublishedAssignments,
				"pending_grades":    assignmentMetrics.TotalAssignments - assignmentMetrics.PublishedAssignments,
			},
			"google_integration": map[string]interface{}{
				"enabled": true,
				"courses_count": len(courses),
				"students_count": len(allStudents),
				"assignments_count": len(allAssignments),
			},
		},
		"metrics": map[string]interface{}{
			"course_metrics": courseMetrics,
			"student_metrics": studentMetrics,
			"assignment_metrics": assignmentMetrics,
			"role_specific": roleMetrics,
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// getFallbackTeacherDashboard returns mock teacher dashboard data
func (h *DashboardHandler) getFallbackTeacherDashboard(c echo.Context, dbUser *models.User) error {
	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "teacher",
			"welcome_message": "Welcome to your teacher dashboard!",
			"stats": map[string]interface{}{
				"total_courses":     5,
				"total_students":    50,
				"graded_assignments": 30,
				"pending_grades":    15,
			},
			"google_integration": map[string]interface{}{
				"enabled": false,
				"fallback": true,
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}
	return c.JSON(http.StatusOK, dashboardData)
}

// getEnhancedCoordinatorDashboard returns coordinator dashboard with Google Classroom integration
func (h *DashboardHandler) getEnhancedCoordinatorDashboard(c echo.Context, dbUser *models.User, userID string) error {
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		return h.getFallbackCoordinatorDashboard(c, dbUser)
	}

	var allStudents []services.Student
	var allAssignments []services.Assignment
	for _, course := range courses {
		students, err := h.googleService.ListStudents(course.ID)
		if err != nil {
			continue
		}
		allStudents = append(allStudents, students...)

		assignments, err := h.googleService.ListAssignments(course.ID)
		if err != nil {
			continue
		}
		allAssignments = append(allAssignments, assignments...)
	}

	courseMetrics := h.metricsService.CalculateCourseMetrics(courses)
	studentMetrics := h.metricsService.CalculateStudentMetrics(allStudents)
	assignmentMetrics := h.metricsService.CalculateAssignmentMetrics(allAssignments)
	roleMetrics := h.metricsService.GetRoleSpecificMetrics("coordinator", courses, allStudents, allAssignments)

	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "coordinator",
			"welcome_message": "Welcome to your coordinator dashboard!",
			"stats": map[string]interface{}{
				"total_courses":     courseMetrics.TotalCourses,
				"total_teachers":    courseMetrics.TotalCourses / 2, // Estimate
				"total_students":    studentMetrics.TotalStudents,
				"active_programs":   3, // Mock value
			},
			"google_integration": map[string]interface{}{
				"enabled": true,
				"courses_count": len(courses),
				"students_count": len(allStudents),
				"assignments_count": len(allAssignments),
			},
		},
		"metrics": map[string]interface{}{
			"course_metrics": courseMetrics,
			"student_metrics": studentMetrics,
			"assignment_metrics": assignmentMetrics,
			"role_specific": roleMetrics,
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// getFallbackCoordinatorDashboard returns mock coordinator dashboard data
func (h *DashboardHandler) getFallbackCoordinatorDashboard(c echo.Context, dbUser *models.User) error {
	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "coordinator",
			"welcome_message": "Welcome to your coordinator dashboard!",
			"stats": map[string]interface{}{
				"total_courses":     15,
				"total_teachers":    8,
				"total_students":    300,
				"active_programs":   3,
			},
			"google_integration": map[string]interface{}{
				"enabled": false,
				"fallback": true,
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}
	return c.JSON(http.StatusOK, dashboardData)
}

// getEnhancedAdminDashboard returns admin dashboard with Google Classroom integration
func (h *DashboardHandler) getEnhancedAdminDashboard(c echo.Context, dbUser *models.User, userID string) error {
	courses, err := h.googleService.ListCourses(userID)
	if err != nil {
		return h.getFallbackAdminDashboard(c, dbUser)
	}

	var allStudents []services.Student
	var allAssignments []services.Assignment
	for _, course := range courses {
		students, err := h.googleService.ListStudents(course.ID)
		if err != nil {
			continue
		}
		allStudents = append(allStudents, students...)

		assignments, err := h.googleService.ListAssignments(course.ID)
		if err != nil {
			continue
		}
		allAssignments = append(allAssignments, assignments...)
	}

	// Get system stats
	allUsers, err := h.userRepo.ListUsers(0, 100)
	if err != nil {
		allUsers = []*models.User{}
	}

	courseMetrics := h.metricsService.CalculateCourseMetrics(courses)
	studentMetrics := h.metricsService.CalculateStudentMetrics(allStudents)
	assignmentMetrics := h.metricsService.CalculateAssignmentMetrics(allAssignments)
	roleMetrics := h.metricsService.GetRoleSpecificMetrics("admin", courses, allStudents, allAssignments)

	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "admin",
			"welcome_message": "Welcome to your admin dashboard!",
			"stats": map[string]interface{}{
				"total_users":       len(allUsers),
				"total_courses":     courseMetrics.TotalCourses,
				"total_teachers":    courseMetrics.TotalCourses / 2, // Estimate
				"total_students":    studentMetrics.TotalStudents,
				"system_uptime":     "99.9%",
			},
			"google_integration": map[string]interface{}{
				"enabled": true,
				"courses_count": len(courses),
				"students_count": len(allStudents),
				"assignments_count": len(allAssignments),
			},
		},
		"metrics": map[string]interface{}{
			"course_metrics": courseMetrics,
			"student_metrics": studentMetrics,
			"assignment_metrics": assignmentMetrics,
			"role_specific": roleMetrics,
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}

// getFallbackAdminDashboard returns mock admin dashboard data
func (h *DashboardHandler) getFallbackAdminDashboard(c echo.Context, dbUser *models.User) error {
	// Get system stats
	allUsers, err := h.userRepo.ListUsers(0, 100)
	if err != nil {
		allUsers = []*models.User{}
	}

	dashboardData := map[string]interface{}{
		"user": map[string]interface{}{
			"id":    dbUser.ID,
			"name":  dbUser.Name,
			"email": dbUser.Email,
			"role":  dbUser.Role,
		},
		"dashboard": map[string]interface{}{
			"type": "admin",
			"welcome_message": "Welcome to your admin dashboard!",
			"stats": map[string]interface{}{
				"total_users": len(allUsers),
				"total_courses": 25,
				"total_teachers": 12,
				"total_students": 450,
				"system_uptime": "99.9%",
			},
			"google_integration": map[string]interface{}{
				"enabled": false,
				"fallback": true,
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}
