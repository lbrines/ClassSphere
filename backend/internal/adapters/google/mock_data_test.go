package google

import (
	"testing"
	"time"

	"github.com/lbrines/classsphere/internal/domain"
)

func TestMockCourses(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := mockCourses(now)

	if len(courses) == 0 {
		t.Fatal("Expected courses to be generated")
	}

	// Test that we have the expected number of courses
	expectedCourseCount := 3
	if len(courses) != expectedCourseCount {
		t.Errorf("Expected %d courses, got %d", expectedCourseCount, len(courses))
	}

	// Test each course structure
	for i, course := range courses {
		t.Run("Course_"+course.ID, func(t *testing.T) {
			testCourseStructure(t, course, i)
		})
	}
}

func TestMockCourses_TimeConsistency(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := mockCourses(now)

	for _, course := range courses {
		// All last activity times should be before or equal to now
		if course.LastActivity.After(now) {
			t.Errorf("Course %s last activity %v should be before or equal to now %v", 
				course.ID, course.LastActivity, now)
		}

		// Test assignments due dates
		for _, assignment := range course.Assignments {
			if assignment.DueDate.IsZero() {
				t.Errorf("Assignment %s due date should not be zero", assignment.ID)
			}
		}

		// Test student progress last submission
		for _, student := range course.Students {
			if student.Progress.LastSubmission.IsZero() {
				t.Errorf("Student %s last submission should not be zero", student.Person.ID)
			}
			if student.Progress.LastSubmission.After(now) {
				t.Errorf("Student %s last submission %v should be before or equal to now %v", 
					student.Person.ID, student.Progress.LastSubmission, now)
			}
		}
	}
}

func TestGoogleSampleCourses(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := googleSampleCourses(now)

	if len(courses) == 0 {
		t.Fatal("Expected courses to be generated")
	}

	// Test that we have the expected number of courses
	expectedCourseCount := 3
	if len(courses) != expectedCourseCount {
		t.Errorf("Expected %d courses, got %d", expectedCourseCount, len(courses))
	}

	// Test that the data is different from mock data (adjusted)
	for i, course := range courses {
		t.Run("SampleCourse_"+course.ID, func(t *testing.T) {
			testCourseStructure(t, course, i)
			
			// Test that last activity is adjusted (should be different from mock)
			expectedActivity := now.Add(-time.Duration((i+1)*2) * time.Hour)
			if !course.LastActivity.Equal(expectedActivity) {
				t.Errorf("Expected last activity %v, got %v", expectedActivity, course.LastActivity)
			}
		})
	}
}

func TestGoogleSampleCourses_DataAdjustments(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := googleSampleCourses(now)

	for _, course := range courses {
		// Test that student scores are adjusted (increased by 1.5)
		for _, student := range course.Students {
			if student.Progress.AverageScore > 100 {
				t.Errorf("Student %s average score %f should not exceed 100", 
					student.Person.ID, student.Progress.AverageScore)
			}
		}

		// Test that assignments are adjusted
		for _, assignment := range course.Assignments {
			if assignment.Status == domain.AssignmentStatusOpen {
				// Should have some completed assignments
				if assignment.Completed == 0 {
					t.Errorf("Assignment %s should have some completed submissions", assignment.ID)
				}
			}
		}
	}
}

func TestMockCourses_DataConsistency(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := mockCourses(now)

	// Test that all courses have valid data
	for _, course := range courses {
		// Test course basic info
		if course.ID == "" {
			t.Error("Course ID should not be empty")
		}
		if course.Name == "" {
			t.Error("Course name should not be empty")
		}
		if course.Section == "" {
			t.Error("Course section should not be empty")
		}
		if course.Program == "" {
			t.Error("Course program should not be empty")
		}

		// Test teachers
		if len(course.Teachers) == 0 {
			t.Error("Course should have at least one teacher")
		}
		for _, teacher := range course.Teachers {
			if teacher.ID == "" {
				t.Error("Teacher ID should not be empty")
			}
			if teacher.Name == "" {
				t.Error("Teacher name should not be empty")
			}
			if teacher.Email == "" {
				t.Error("Teacher email should not be empty")
			}
		}

		// Test students
		if len(course.Students) == 0 {
			t.Error("Course should have at least one student")
		}
		for _, student := range course.Students {
			if student.Person.ID == "" {
				t.Error("Student ID should not be empty")
			}
			if student.Person.Name == "" {
				t.Error("Student name should not be empty")
			}
			if student.Person.Email == "" {
				t.Error("Student email should not be empty")
			}

			// Test progress data
			progress := student.Progress
			if progress.CompletedAssignments < 0 {
				t.Error("Completed assignments should not be negative")
			}
			if progress.PendingAssignments < 0 {
				t.Error("Pending assignments should not be negative")
			}
			if progress.AverageScore < 0 || progress.AverageScore > 100 {
				t.Errorf("Average score %f should be between 0 and 100", progress.AverageScore)
			}
			if progress.AttendanceRate < 0 || progress.AttendanceRate > 1 {
				t.Errorf("Attendance rate %f should be between 0 and 1", progress.AttendanceRate)
			}
			if progress.LateSubmissions < 0 {
				t.Error("Late submissions should not be negative")
			}
			if progress.UpcomingAssignments < 0 {
				t.Error("Upcoming assignments should not be negative")
			}
		}

		// Test assignments
		if len(course.Assignments) == 0 {
			t.Error("Course should have at least one assignment")
		}
		for _, assignment := range course.Assignments {
			if assignment.ID == "" {
				t.Error("Assignment ID should not be empty")
			}
			if assignment.Title == "" {
				t.Error("Assignment title should not be empty")
			}
			if assignment.MaxPoints <= 0 {
				t.Error("Max points should be positive")
			}
			if assignment.Completed < 0 {
				t.Error("Completed count should not be negative")
			}
			if assignment.Pending < 0 {
				t.Error("Pending count should not be negative")
			}
			if assignment.Late < 0 {
				t.Error("Late count should not be negative")
			}
		}

		// Test schedule
		if len(course.Schedule.Days) == 0 {
			t.Error("Course should have schedule days")
		}
		if course.Schedule.StartTime == "" {
			t.Error("Course should have start time")
		}
		if course.Schedule.EndTime == "" {
			t.Error("Course should have end time")
		}
	}
}

func TestMockCourses_UniqueIDs(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	courses := mockCourses(now)

	// Test that all course IDs are unique
	seenIDs := make(map[string]bool)
	for _, course := range courses {
		if seenIDs[course.ID] {
			t.Errorf("Duplicate course ID found: %s", course.ID)
		}
		seenIDs[course.ID] = true

		// Test that all assignment IDs are unique within a course
		seenAssignmentIDs := make(map[string]bool)
		for _, assignment := range course.Assignments {
			if seenAssignmentIDs[assignment.ID] {
				t.Errorf("Duplicate assignment ID found in course %s: %s", course.ID, assignment.ID)
			}
			seenAssignmentIDs[assignment.ID] = true
		}

		// Test that all student IDs are unique within a course
		seenStudentIDs := make(map[string]bool)
		for _, student := range course.Students {
			if seenStudentIDs[student.Person.ID] {
				t.Errorf("Duplicate student ID found in course %s: %s", course.ID, student.Person.ID)
			}
			seenStudentIDs[student.Person.ID] = true
		}

		// Test that all teacher IDs are unique within a course
		seenTeacherIDs := make(map[string]bool)
		for _, teacher := range course.Teachers {
			if seenTeacherIDs[teacher.ID] {
				t.Errorf("Duplicate teacher ID found in course %s: %s", course.ID, teacher.ID)
			}
			seenTeacherIDs[teacher.ID] = true
		}
	}
}

func testCourseStructure(t *testing.T, course domain.Course, index int) {
	// Basic course validation
	if course.ID == "" {
		t.Error("Course ID should not be empty")
	}
	if course.Name == "" {
		t.Error("Course name should not be empty")
	}
	if course.Section == "" {
		t.Error("Course section should not be empty")
	}
	if course.Program == "" {
		t.Error("Course program should not be empty")
	}

	// Test that we have expected course types
	expectedPrograms := []string{"STEM", "Humanities"}
	found := false
	for _, program := range expectedPrograms {
		if course.Program == program {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Course program %s should be one of %v", course.Program, expectedPrograms)
	}

	// Test that we have the expected number of students per course
	if len(course.Students) < 2 {
		t.Errorf("Course %s should have at least 2 students, got %d", course.ID, len(course.Students))
	}

	// Test that we have the expected number of assignments per course
	if len(course.Assignments) < 1 {
		t.Errorf("Course %s should have at least 1 assignment, got %d", course.ID, len(course.Assignments))
	}
}