package google

import (
	"time"

	"github.com/lbrines/classsphere/internal/domain"
)

func mockCourses(now time.Time) []domain.Course {
	return []domain.Course{
		{
			ID:               "course-stem-101",
			Name:             "STEM Foundations",
			Section:          "STEM-101",
			Program:          "STEM",
			Room:             "Lab 3",
			CoordinatorEmail: "coordinator@classsphere.edu",
			LastActivity:     now.Add(-12 * time.Hour),
			Schedule: domain.CourseSchedule{
				Days:      []string{"Monday", "Wednesday"},
				StartTime: "09:00",
				EndTime:   "10:30",
			},
			Teachers: []domain.CourseTeacher{
				{ID: "teacher-1", Name: "Carlos Vega", Email: "teacher@classsphere.edu"},
			},
			Students: []domain.CourseStudent{
				{
					Person: domain.Person{ID: "student-1", Name: "Sara Kim", Email: "student@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 7,
						PendingAssignments:   2,
						AverageScore:         92,
						AttendanceRate:       0.96,
						LateSubmissions:      1,
						UpcomingAssignments:  1,
						LastSubmission:       now.Add(-18 * time.Hour),
					},
				},
				{
					Person: domain.Person{ID: "student-2", Name: "Miguel Torres", Email: "miguel.torres@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 6,
						PendingAssignments:   3,
						AverageScore:         84,
						AttendanceRate:       0.91,
						LateSubmissions:      2,
						UpcomingAssignments:  2,
						LastSubmission:       now.Add(-36 * time.Hour),
					},
				},
				{
					Person: domain.Person{ID: "student-3", Name: "Emma Li", Email: "emma.li@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 8,
						PendingAssignments:   1,
						AverageScore:         95,
						AttendanceRate:       0.98,
						LateSubmissions:      0,
						UpcomingAssignments:  1,
						LastSubmission:       now.Add(-6 * time.Hour),
					},
				},
			},
			Assignments: []domain.CourseAssignment{
				{
					ID:        "assign-stem-1",
					Title:     "Kinematics Lab",
					DueDate:   now.Add(48 * time.Hour),
					MaxPoints: 100,
					Status:    domain.AssignmentStatusOpen,
					Completed: 18,
					Pending:   4,
					Late:      1,
				},
				{
					ID:        "assign-stem-2",
					Title:     "Robotics Challenge",
					DueDate:   now.Add(-24 * time.Hour),
					MaxPoints: 100,
					Status:    domain.AssignmentStatusClosed,
					Completed: 22,
					Pending:   0,
					Late:      2,
				},
				{
					ID:        "assign-stem-3",
					Title:     "Energy Systems Quiz",
					DueDate:   now.Add(96 * time.Hour),
					MaxPoints: 50,
					Status:    domain.AssignmentStatusPlanned,
					Completed: 0,
					Pending:   24,
					Late:      0,
				},
			},
		},
		{
			ID:               "course-hum-201",
			Name:             "Global Literature",
			Section:          "HUM-201",
			Program:          "Humanities",
			Room:             "Room 5A",
			CoordinatorEmail: "coordinator@classsphere.edu",
			LastActivity:     now.Add(-6 * time.Hour),
			Schedule: domain.CourseSchedule{
				Days:      []string{"Tuesday", "Thursday"},
				StartTime: "11:00",
				EndTime:   "12:30",
			},
			Teachers: []domain.CourseTeacher{
				{ID: "teacher-2", Name: "Laura Nguyen", Email: "laura.nguyen@classsphere.edu"},
			},
			Students: []domain.CourseStudent{
				{
					Person: domain.Person{ID: "student-4", Name: "Noah Patel", Email: "noah.patel@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 9,
						PendingAssignments:   1,
						AverageScore:         88,
						AttendanceRate:       0.94,
						LateSubmissions:      1,
						UpcomingAssignments:  1,
						LastSubmission:       now.Add(-10 * time.Hour),
					},
				},
				{
					Person: domain.Person{ID: "student-5", Name: "Olivia Mendes", Email: "olivia.mendes@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 10,
						PendingAssignments:   0,
						AverageScore:         97,
						AttendanceRate:       0.99,
						LateSubmissions:      0,
						UpcomingAssignments:  1,
						LastSubmission:       now.Add(-4 * time.Hour),
					},
				},
				{
					Person: domain.Person{ID: "student-6", Name: "Ethan Brooks", Email: "ethan.brooks@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 7,
						PendingAssignments:   3,
						AverageScore:         80,
						AttendanceRate:       0.89,
						LateSubmissions:      3,
						UpcomingAssignments:  2,
						LastSubmission:       now.Add(-72 * time.Hour),
					},
				},
			},
			Assignments: []domain.CourseAssignment{
				{
					ID:        "assign-hum-1",
					Title:     "Literary Analysis Essay",
					DueDate:   now.Add(72 * time.Hour),
					MaxPoints: 100,
					Status:    domain.AssignmentStatusOpen,
					Completed: 15,
					Pending:   6,
					Late:      0,
				},
				{
					ID:        "assign-hum-2",
					Title:     "Poetry Recital",
					DueDate:   now.Add(-48 * time.Hour),
					MaxPoints: 50,
					Status:    domain.AssignmentStatusClosed,
					Completed: 21,
					Pending:   0,
					Late:      1,
				},
			},
		},
		{
			ID:               "course-robot-301",
			Name:             "Robotics Capstone",
			Section:          "STEM-301",
			Program:          "STEM",
			Room:             "Innovation Hub",
			CoordinatorEmail: "coordinator@classsphere.edu",
			LastActivity:     now.Add(-2 * time.Hour),
			Schedule: domain.CourseSchedule{
				Days:      []string{"Friday"},
				StartTime: "14:00",
				EndTime:   "17:00",
			},
			Teachers: []domain.CourseTeacher{
				{ID: "teacher-1", Name: "Carlos Vega", Email: "teacher@classsphere.edu"},
				{ID: "teacher-3", Name: "Priya Desai", Email: "priya.desai@classsphere.edu"},
			},
			Students: []domain.CourseStudent{
				{
					Person: domain.Person{ID: "student-1", Name: "Sara Kim", Email: "student@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 4,
						PendingAssignments:   1,
						AverageScore:         91,
						AttendanceRate:       0.97,
						LateSubmissions:      0,
						UpcomingAssignments:  1,
						LastSubmission:       now.Add(-8 * time.Hour),
					},
				},
				{
					Person: domain.Person{ID: "student-7", Name: "David Romero", Email: "david.romero@classsphere.edu"},
					Progress: domain.StudentProgress{
						CompletedAssignments: 3,
						PendingAssignments:   2,
						AverageScore:         76,
						AttendanceRate:       0.88,
						LateSubmissions:      2,
						UpcomingAssignments:  2,
						LastSubmission:       now.Add(-96 * time.Hour),
					},
				},
			},
			Assignments: []domain.CourseAssignment{
				{
					ID:        "assign-rob-1",
					Title:     "Prototype Demo",
					DueDate:   now.Add(120 * time.Hour),
					MaxPoints: 200,
					Status:    domain.AssignmentStatusOpen,
					Completed: 6,
					Pending:   8,
					Late:      0,
				},
				{
					ID:        "assign-rob-2",
					Title:     "Design Review",
					DueDate:   now.Add(-72 * time.Hour),
					MaxPoints: 100,
					Status:    domain.AssignmentStatusClosed,
					Completed: 10,
					Pending:   0,
					Late:      1,
				},
			},
		},
	}
}

// googleSampleCourses mirrors real-world data distribution while remaining
// deterministic for local environments without API credentials.
func googleSampleCourses(now time.Time) []domain.Course {
	data := mockCourses(now)

	// Slightly adjust the dataset to reflect a different mode.
	for i := range data {
		course := &data[i]
		course.LastActivity = now.Add(-time.Duration((i+1)*2) * time.Hour)
		for s := range course.Students {
			course.Students[s].Progress.AverageScore += 1.5
			if course.Students[s].Progress.AverageScore > 100 {
				course.Students[s].Progress.AverageScore = 100
			}
			if course.Students[s].Progress.PendingAssignments > 0 {
				course.Students[s].Progress.PendingAssignments--
			}
		}
		for a := range course.Assignments {
			if course.Assignments[a].Status == domain.AssignmentStatusOpen {
				course.Assignments[a].Completed += 2
				if course.Assignments[a].Pending > 1 {
					course.Assignments[a].Pending--
				}
			}
		}
	}
	return data
}
