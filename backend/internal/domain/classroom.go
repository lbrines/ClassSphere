package domain

import "time"

// ClassroomSnapshot aggregates the current state of Google Classroom data that
// the application consumes to build dashboards and listings.
type ClassroomSnapshot struct {
	Mode        string
	GeneratedAt time.Time
	Courses     []Course
}

// Course represents a Google Classroom course enriched with analytics-ready
// information.
type Course struct {
	ID               string
	Name             string
	Section          string
	Program          string
	Room             string
	CoordinatorEmail string
	Teachers         []CourseTeacher
	Students         []CourseStudent
	Assignments      []CourseAssignment
	Schedule         CourseSchedule
	LastActivity     time.Time
}

// CourseTeacher contains the minimal metadata required for dashboards.
type CourseTeacher struct {
	ID    string
	Name  string
	Email string
}

// CourseStudent models a student enrolled in a course with progress metrics.
type CourseStudent struct {
	Person   Person
	Progress StudentProgress
}

// Person contains shared contact information.
type Person struct {
	ID    string
	Name  string
	Email string
}

// StudentProgress encapsulates analytical data for a student inside a course.
type StudentProgress struct {
	CompletedAssignments int
	PendingAssignments   int
	AverageScore         float64
	AttendanceRate       float64
	LateSubmissions      int
	UpcomingAssignments  int
	LastSubmission       time.Time
}

// CourseAssignment details an assignment and submission statistics.
type CourseAssignment struct {
	ID        string
	Title     string
	DueDate   time.Time
	MaxPoints float64
	Status    CourseAssignmentStatus
	Completed int
	Pending   int
	Late      int
}

// CourseAssignmentStatus captures the lifecycle of an assignment.
type CourseAssignmentStatus string

const (
	AssignmentStatusPlanned CourseAssignmentStatus = "planned"
	AssignmentStatusOpen    CourseAssignmentStatus = "open"
	AssignmentStatusClosed  CourseAssignmentStatus = "closed"
)

// CourseSchedule contains structured schedule details.
type CourseSchedule struct {
	Days      []string
	StartTime string
	EndTime   string
}
