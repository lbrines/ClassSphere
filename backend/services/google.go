package services

import (
	"fmt"
	"math/rand"
	"time"
)

// GoogleClient interface for dependency injection
type GoogleClient interface {
	ListCourses(userID string) ([]Course, error)
	ListStudents(courseID string) ([]Student, error)
	ListAssignments(courseID string) ([]Assignment, error)
}

// Course represents a Google Classroom course
type Course struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Section     string `json:"section"`
	Room        string `json:"room"`
	OwnerID     string `json:"ownerId"`
	CourseState string `json:"courseState"`
}

// Student represents a Google Classroom student
type Student struct {
	ID       string `json:"id"`
	Name     string `json:"name"`
	Email    string `json:"email"`
	PhotoURL string `json:"photoUrl"`
}

// Assignment represents a Google Classroom assignment
type Assignment struct {
	ID          string `json:"id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	DueDate     string `json:"dueDate"`
	MaxPoints   int    `json:"maxPoints"`
	State       string `json:"state"`
}

// GoogleClassroomService handles Google Classroom API integration
type GoogleClassroomService struct {
	client   GoogleClient
	mockMode bool
}

// NewGoogleClassroomService creates a new Google Classroom service
func NewGoogleClassroomService(client GoogleClient) *GoogleClassroomService {
	return &GoogleClassroomService{
		client:   client,
		mockMode: client == nil, // Enable mock mode if no client is provided
	}
}

// SetMockMode enables or disables mock mode
func (s *GoogleClassroomService) SetMockMode(enabled bool) {
	s.mockMode = enabled
}

// ListCourses retrieves courses for a user
func (s *GoogleClassroomService) ListCourses(userID string) ([]Course, error) {
	if s.mockMode {
		fmt.Printf("DEBUG: Using mock mode for userID: %s\n", userID)
		courses := s.getMockCourses()
		fmt.Printf("DEBUG: Returning %d mock courses\n", len(courses))
		return courses, nil
	}

	if s.client == nil {
		return nil, fmt.Errorf("Google client not initialized")
	}

	return s.client.ListCourses(userID)
}

// ListStudents retrieves students for a course
func (s *GoogleClassroomService) ListStudents(courseID string) ([]Student, error) {
	if s.mockMode {
		return s.getMockStudents(), nil
	}

	if s.client == nil {
		return nil, fmt.Errorf("Google client not initialized")
	}

	return s.client.ListStudents(courseID)
}

// ListAssignments retrieves assignments for a course
func (s *GoogleClassroomService) ListAssignments(courseID string) ([]Assignment, error) {
	if s.mockMode {
		return s.getMockAssignments(), nil
	}

	if s.client == nil {
		return nil, fmt.Errorf("Google client not initialized")
	}

	return s.client.ListAssignments(courseID)
}

// getMockCourses returns mock course data for testing and development
func (s *GoogleClassroomService) getMockCourses() []Course {
	return []Course{
		{
			ID:          "course_mock_1",
			Name:        "Advanced Mathematics",
			Description: "Comprehensive study of calculus, algebra, and geometry",
			Section:     "A",
			Room:        "Room 201",
			OwnerID:     "teacher_mock_1",
			CourseState: "ACTIVE",
		},
		{
			ID:          "course_mock_2",
			Name:        "Physics Laboratory",
			Description: "Hands-on experiments in mechanics, thermodynamics, and electromagnetism",
			Section:     "B",
			Room:        "Lab 301",
			OwnerID:     "teacher_mock_2",
			CourseState: "ACTIVE",
		},
		{
			ID:          "course_mock_3",
			Name:        "English Literature",
			Description: "Study of classic and contemporary literature",
			Section:     "C",
			Room:        "Room 105",
			OwnerID:     "teacher_mock_3",
			CourseState: "ACTIVE",
		},
		{
			ID:          "course_mock_4",
			Name:        "Computer Science",
			Description: "Programming fundamentals and software engineering",
			Section:     "D",
			Room:        "Computer Lab 1",
			OwnerID:     "teacher_mock_4",
			CourseState: "ACTIVE",
		},
		{
			ID:          "course_mock_5",
			Name:        "World History",
			Description: "Comprehensive study of world civilizations and events",
			Section:     "E",
			Room:        "Room 208",
			OwnerID:     "teacher_mock_5",
			CourseState: "ACTIVE",
		},
	}
}

// getMockStudents returns mock student data for testing and development
func (s *GoogleClassroomService) getMockStudents() []Student {
	return []Student{
		{
			ID:       "student_mock_1",
			Name:     "Alice Johnson",
			Email:    "alice.johnson@classsphere.edu",
			PhotoURL: "https://example.com/photos/alice.jpg",
		},
		{
			ID:       "student_mock_2",
			Name:     "Bob Smith",
			Email:    "bob.smith@classsphere.edu",
			PhotoURL: "https://example.com/photos/bob.jpg",
		},
		{
			ID:       "student_mock_3",
			Name:     "Carol Davis",
			Email:    "carol.davis@classsphere.edu",
			PhotoURL: "https://example.com/photos/carol.jpg",
		},
		{
			ID:       "student_mock_4",
			Name:     "David Wilson",
			Email:    "david.wilson@classsphere.edu",
			PhotoURL: "https://example.com/photos/david.jpg",
		},
		{
			ID:       "student_mock_5",
			Name:     "Eva Brown",
			Email:    "eva.brown@classsphere.edu",
			PhotoURL: "https://example.com/photos/eva.jpg",
		},
		{
			ID:       "student_mock_6",
			Name:     "Frank Miller",
			Email:    "frank.miller@classsphere.edu",
			PhotoURL: "https://example.com/photos/frank.jpg",
		},
		{
			ID:       "student_mock_7",
			Name:     "Grace Lee",
			Email:    "grace.lee@classsphere.edu",
			PhotoURL: "https://example.com/photos/grace.jpg",
		},
		{
			ID:       "student_mock_8",
			Name:     "Henry Taylor",
			Email:    "henry.taylor@classsphere.edu",
			PhotoURL: "https://example.com/photos/henry.jpg",
		},
	}
}

// getMockAssignments returns mock assignment data for testing and development
func (s *GoogleClassroomService) getMockAssignments() []Assignment {
	now := time.Now()
	
	return []Assignment{
		{
			ID:          "assignment_mock_1",
			Title:       "Calculus Problem Set 1",
			Description: "Solve differential equations and integration problems",
			DueDate:     now.AddDate(0, 0, 7).Format("2006-01-02"),
			MaxPoints:   100,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment_mock_2",
			Title:       "Physics Lab Report: Pendulum Motion",
			Description: "Write a comprehensive report on pendulum motion experiments",
			DueDate:     now.AddDate(0, 0, 5).Format("2006-01-02"),
			MaxPoints:   150,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment_mock_3",
			Title:       "Literature Analysis: Shakespeare's Hamlet",
			Description: "Analyze themes and character development in Hamlet",
			DueDate:     now.AddDate(0, 0, 10).Format("2006-01-02"),
			MaxPoints:   120,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment_mock_4",
			Title:       "Programming Project: Web Application",
			Description: "Build a full-stack web application using modern technologies",
			DueDate:     now.AddDate(0, 0, 14).Format("2006-01-02"),
			MaxPoints:   200,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment_mock_5",
			Title:       "History Research Paper: World War II",
			Description: "Research and analyze the causes and effects of World War II",
			DueDate:     now.AddDate(0, 0, 12).Format("2006-01-02"),
			MaxPoints:   180,
			State:       "PUBLISHED",
		},
		{
			ID:          "assignment_mock_6",
			Title:       "Algebra Quiz: Linear Equations",
			Description: "Quiz covering solving linear equations and graphing",
			DueDate:     now.AddDate(0, 0, 3).Format("2006-01-02"),
			MaxPoints:   80,
			State:       "PUBLISHED",
		},
	}
}

// GetRandomCourse returns a random course from mock data
func (s *GoogleClassroomService) GetRandomCourse() Course {
	courses := s.getMockCourses()
	if len(courses) == 0 {
		return Course{}
	}
	
	rand.Seed(time.Now().UnixNano())
	return courses[rand.Intn(len(courses))]
}

// GetRandomStudent returns a random student from mock data
func (s *GoogleClassroomService) GetRandomStudent() Student {
	students := s.getMockStudents()
	if len(students) == 0 {
		return Student{}
	}
	
	rand.Seed(time.Now().UnixNano())
	return students[rand.Intn(len(students))]
}

// GetRandomAssignment returns a random assignment from mock data
func (s *GoogleClassroomService) GetRandomAssignment() Assignment {
	assignments := s.getMockAssignments()
	if len(assignments) == 0 {
		return Assignment{}
	}
	
	rand.Seed(time.Now().UnixNano())
	return assignments[rand.Intn(len(assignments))]
}

// GetCourseStats returns statistics for a course
func (s *GoogleClassroomService) GetCourseStats(courseID string) (map[string]interface{}, error) {
	// Get students for the course
	students, err := s.ListStudents(courseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get students: %v", err)
	}

	// Get assignments for the course
	assignments, err := s.ListAssignments(courseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get assignments: %v", err)
	}

	// Calculate statistics
	stats := map[string]interface{}{
		"course_id":           courseID,
		"total_students":      len(students),
		"total_assignments":   len(assignments),
		"published_assignments": 0,
		"draft_assignments":   0,
	}

	// Count assignment states
	for _, assignment := range assignments {
		if assignment.State == "PUBLISHED" {
			stats["published_assignments"] = stats["published_assignments"].(int) + 1
		} else {
			stats["draft_assignments"] = stats["draft_assignments"].(int) + 1
		}
	}

	return stats, nil
}
