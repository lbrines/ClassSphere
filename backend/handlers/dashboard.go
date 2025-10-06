package handlers

import (
	"net/http"
	"strconv"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
)

type DashboardHandler struct {
	userRepo *models.UserRepository
}

func NewDashboardHandler(userRepo *models.UserRepository) *DashboardHandler {
	return &DashboardHandler{
		userRepo: userRepo,
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

	// Mock student dashboard data
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

	// Mock teacher dashboard data
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
				"total_courses": 4,
				"total_students": 120,
				"assignments_graded": 45,
				"assignments_pending": 8,
			},
			"recent_activities": []map[string]interface{}{
				{
					"type": "assignment_graded",
					"title": "Math Homework #3",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
					"students_graded": 25,
				},
				{
					"type": "new_assignment",
					"title": "Science Lab Report",
					"date": time.Now().AddDate(0, 0, -2).Format("2006-01-02"),
					"course": "Chemistry",
				},
			},
			"upcoming_tasks": []map[string]interface{}{
				{
					"title": "Grade History Essays",
					"due_date": time.Now().AddDate(0, 0, 2).Format("2006-01-02"),
					"course": "World History",
					"students": 30,
				},
				{
					"title": "Prepare Math Test",
					"due_date": time.Now().AddDate(0, 0, 4).Format("2006-01-02"),
					"course": "Algebra II",
				},
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
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

	// Mock coordinator dashboard data
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
				"total_courses": 15,
				"total_teachers": 8,
				"total_students": 300,
				"active_programs": 3,
			},
			"recent_activities": []map[string]interface{}{
				{
					"type": "course_created",
					"title": "Advanced Mathematics",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
					"teacher": "Dr. Smith",
				},
				{
					"type": "teacher_assigned",
					"title": "Chemistry Lab",
					"date": time.Now().AddDate(0, 0, -2).Format("2006-01-02"),
					"teacher": "Prof. Johnson",
				},
			},
			"upcoming_tasks": []map[string]interface{}{
				{
					"title": "Review Course Schedules",
					"due_date": time.Now().AddDate(0, 0, 3).Format("2006-01-02"),
					"priority": "high",
				},
				{
					"title": "Teacher Performance Review",
					"due_date": time.Now().AddDate(0, 0, 7).Format("2006-01-02"),
					"teachers": 8,
				},
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
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

	// Get system stats
	allUsers, err := h.userRepo.ListUsers(0, 100)
	if err != nil {
		allUsers = []*models.User{}
	}

	// Mock admin dashboard data
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
			"recent_activities": []map[string]interface{}{
				{
					"type": "user_registered",
					"title": "New Student Registration",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
					"user": "john.doe@example.com",
				},
				{
					"type": "system_backup",
					"title": "Daily Backup Completed",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
					"status": "success",
				},
			},
			"system_alerts": []map[string]interface{}{
				{
					"type": "warning",
					"title": "High Server Load",
					"message": "Server CPU usage above 80%",
					"date": time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
				},
				{
					"type": "info",
					"title": "Scheduled Maintenance",
					"message": "System maintenance scheduled for Sunday",
					"date": time.Now().AddDate(0, 0, 2).Format("2006-01-02"),
				},
			},
		},
		"timestamp": time.Now().Format("2006-01-02T15:04:05Z07:00"),
	}

	return c.JSON(http.StatusOK, dashboardData)
}
