package app

import (
	"context"
	"fmt"
	"math"
	"sort"
	"strings"
	"time"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

// CourseListResult wraps the output of the course listing use case.
type CourseListResult struct {
	Mode        string
	GeneratedAt time.Time
	Courses     []CourseOverview
}

// ClassroomService orchestrates classroom providers (real Google or mock) and
// builds analytics tailored to each role.
type ClassroomService struct {
	providers   map[string]ports.ClassroomProvider
	defaultMode string
	now         func() time.Time
}

// NewClassroomService constructs the service.
func NewClassroomService(defaultMode string, providers ...ports.ClassroomProvider) (*ClassroomService, error) {
	if len(providers) == 0 {
		return nil, fmt.Errorf("at least one classroom provider must be supplied")
	}
	modeMap := make(map[string]ports.ClassroomProvider, len(providers))
	for _, provider := range providers {
		if provider == nil {
			continue
		}
		mode := shared.NormalizeIntegrationMode(provider.Mode())
		modeMap[mode] = provider
	}
	if len(modeMap) == 0 {
		return nil, fmt.Errorf("no valid classroom providers registered")
	}
	normalizedDefault := shared.NormalizeIntegrationMode(defaultMode)
	if _, ok := modeMap[normalizedDefault]; !ok {
		// If the requested default mode is unavailable fall back to mock.
		if provider, okMock := modeMap[shared.IntegrationModeMock]; okMock {
			normalizedDefault = shared.IntegrationModeMock
			modeMap[shared.IntegrationModeMock] = provider
		} else {
			for mode := range modeMap {
				normalizedDefault = mode
				break
			}
		}
	}
	return &ClassroomService{
		providers:   modeMap,
		defaultMode: normalizedDefault,
		now:         time.Now,
	}, nil
}

// WithClock allows overriding the internal time provider (testing).
func (s *ClassroomService) WithClock(clock func() time.Time) {
	if clock != nil {
		s.now = clock
	}
}

// AvailableModes returns the modes registered in the service.
func (s *ClassroomService) AvailableModes() []string {
	modes := make([]string, 0, len(s.providers))
	for mode := range s.providers {
		modes = append(modes, mode)
	}
	sort.Strings(modes)
	return modes
}

// ListCourses returns condensed course information for the current mode.
func (s *ClassroomService) ListCourses(ctx context.Context, mode string) (CourseListResult, error) {
	provider, resolvedMode, err := s.resolveMode(mode)
	if err != nil {
		return CourseListResult{}, err
	}
	snapshot, err := provider.Snapshot(ctx)
	if err != nil {
		return CourseListResult{}, fmt.Errorf("retrieve classroom snapshot: %w", err)
	}

	courses := make([]CourseOverview, 0, len(snapshot.Courses))
	for _, course := range snapshot.Courses {
		courses = append(courses, overviewFromCourse(course, snapshot.GeneratedAt))
	}

	sort.Slice(courses, func(i, j int) bool {
		return courses[i].CompletionRate > courses[j].CompletionRate
	})

	return CourseListResult{
		Mode:        resolvedMode,
		GeneratedAt: snapshot.GeneratedAt,
		Courses:     courses,
	}, nil
}

// Dashboard resolves the role-specific dashboard view.
func (s *ClassroomService) Dashboard(ctx context.Context, user domain.User, requestedMode string) (DashboardData, error) {
	provider, resolvedMode, err := s.resolveMode(requestedMode)
	if err != nil {
		return DashboardData{}, err
	}
	snapshot, err := provider.Snapshot(ctx)
	if err != nil {
		return DashboardData{}, fmt.Errorf("retrieve classroom snapshot: %w", err)
	}

	snapshot.Mode = resolvedMode
	switch user.Role {
	case domain.RoleAdmin:
		return buildAdminDashboard(snapshot), nil
	case domain.RoleCoordinator:
		return buildCoordinatorDashboard(snapshot, user), nil
	case domain.RoleTeacher:
		return buildTeacherDashboard(snapshot, user), nil
	case domain.RoleStudent:
		return buildStudentDashboard(snapshot, user), nil
	default:
		return DashboardData{}, fmt.Errorf("unsupported role %s", user.Role)
	}
}

func (s *ClassroomService) resolveMode(requested string) (ports.ClassroomProvider, string, error) {
	mode := shared.NormalizeIntegrationMode(requested)
	if mode == "" {
		mode = s.defaultMode
	}
	provider, ok := s.providers[mode]
	if !ok {
		// fallback to default
		provider, ok = s.providers[s.defaultMode]
		mode = s.defaultMode
	}
	if !ok {
		return nil, "", fmt.Errorf("no classroom provider available")
	}
	return provider, mode, nil
}

func buildAdminDashboard(snapshot domain.ClassroomSnapshot) DashboardData {
	now := snapshot.GeneratedAt
	totalCourses := len(snapshot.Courses)
	totalStudents := uniqueStudentCount(snapshot.Courses)
	avgCompletion := averageCourseCompletion(snapshot.Courses)
	onTimeRate := globalOnTimeSubmissionRate(snapshot.Courses)

	completionDelta, completionTrend := deltaAndTrend(avgCompletion, 78)
	studentDelta, studentTrend := deltaAndTrend(float64(totalStudents), 55)
	courseDelta, courseTrend := deltaAndTrend(float64(totalCourses), 3)
	onTimeDelta, onTimeTrend := deltaAndTrend(onTimeRate, 84)

	summary := []SummaryMetric{
		{ID: "totalCourses", Label: "Total Courses", Value: float64(totalCourses), Delta: courseDelta, Trend: courseTrend, Format: "number"},
		{ID: "activeStudents", Label: "Active Students", Value: float64(totalStudents), Delta: studentDelta, Trend: studentTrend, Format: "number"},
		{ID: "avgCompletion", Label: "Avg Completion", Value: round2(avgCompletion), Delta: completionDelta, Trend: completionTrend, Format: "percent"},
		{ID: "onTimeSubmissions", Label: "On-time Submissions", Value: round2(onTimeRate), Delta: onTimeDelta, Trend: onTimeTrend, Format: "percent"},
	}

	charts := []ChartData{
		buildSubmissionChart(snapshot.Courses),
		buildCoursePerformanceChart(snapshot.Courses),
	}

	highlights := buildAdminHighlights(snapshot.Courses)
	alerts := buildAdminAlerts(snapshot.Courses)

	courseOverviews := make([]CourseOverview, 0, len(snapshot.Courses))
	for _, course := range snapshot.Courses {
		courseOverviews = append(courseOverviews, overviewFromCourse(course, snapshot.GeneratedAt))
	}

	return DashboardData{
		Role:        string(domain.RoleAdmin),
		Mode:        snapshot.Mode,
		GeneratedAt: now,
		Summary:     summary,
		Charts:      charts,
		Highlights:  highlights,
		Alerts:      alerts,
		Courses:     courseOverviews,
	}
}

func buildCoordinatorDashboard(snapshot domain.ClassroomSnapshot, user domain.User) DashboardData {
	courses := filterCoursesByCoordinator(snapshot.Courses, user.Email)
	if len(courses) == 0 {
		return emptyDashboard(snapshot.Mode, user.Role, snapshot.GeneratedAt, []string{"No courses assigned to coordinator"})
	}
	totalCourses := len(courses)
	enrollment := totalEnrollment(courses)
	avgCompletion := averageCourseCompletion(courses)
	atRiskCourses := countAtRiskCourses(courses)

	enrollmentDelta, enrollmentTrend := deltaAndTrend(float64(enrollment), 40)
	atRiskDelta, atRiskTrend := deltaAndTrend(float64(atRiskCourses), 3)
	courseDelta, courseTrend := deltaAndTrend(float64(totalCourses), 2)
	completionDelta, completionTrend := deltaAndTrend(avgCompletion, 80)

	summary := []SummaryMetric{
		{ID: "coordinatorCourses", Label: "Program Courses", Value: float64(totalCourses), Delta: courseDelta, Trend: courseTrend, Format: "number"},
		{ID: "enrollment", Label: "Total Enrollment", Value: float64(enrollment), Delta: enrollmentDelta, Trend: enrollmentTrend, Format: "number"},
		{ID: "avgCompletion", Label: "Average Completion", Value: round2(avgCompletion), Delta: completionDelta, Trend: completionTrend, Format: "percent"},
		{ID: "atRiskCourses", Label: "Courses at Risk", Value: float64(atRiskCourses), Delta: atRiskDelta, Trend: atRiskTrend, Format: "number"},
	}

	charts := []ChartData{
		buildProgramDistributionChart(courses),
		buildLateSubmissionChart(courses),
	}

	highlights := buildCoordinatorHighlights(courses)

	courseOverviews := make([]CourseOverview, 0, len(courses))
	for _, course := range courses {
		courseOverviews = append(courseOverviews, overviewFromCourse(course, snapshot.GeneratedAt))
	}

	return DashboardData{
		Role:        string(domain.RoleCoordinator),
		Mode:        snapshot.Mode,
		GeneratedAt: snapshot.GeneratedAt,
		Summary:     summary,
		Charts:      charts,
		Highlights:  highlights,
		Courses:     courseOverviews,
	}
}

func buildTeacherDashboard(snapshot domain.ClassroomSnapshot, user domain.User) DashboardData {
	courses := filterCoursesByTeacher(snapshot.Courses, user.Email)
	if len(courses) == 0 {
		return emptyDashboard(snapshot.Mode, user.Role, snapshot.GeneratedAt, []string{"No active courses for this teacher"})
	}

	totalStudents := totalEnrollment(courses)
	avgCompletion := averageCourseCompletion(courses)
	upcomingAssignments := upcomingAssignmentsForCourses(courses, snapshot.GeneratedAt)
	lateAssignments := lateAssignmentsForCourses(courses)

	summary := []SummaryMetric{
		{ID: "teacherCourses", Label: "Active Courses", Value: float64(len(courses)), Delta: delta(len(courses), 2), Trend: trend(len(courses), 2), Format: "number"},
		{ID: "teacherStudents", Label: "Enrolled Students", Value: float64(totalStudents), Delta: delta(totalStudents, 35), Trend: trend(totalStudents, 35), Format: "number"},
		{ID: "teacherCompletion", Label: "Avg Completion", Value: round2(avgCompletion), Delta: deltaFloat(avgCompletion, 82), Trend: trendFloat(avgCompletion, 82), Format: "percent"},
		{ID: "upcomingAssignments", Label: "Upcoming Assignments", Value: float64(upcomingAssignments), Delta: delta(upcomingAssignments, 4), Trend: trend(upcomingAssignments, 4), Format: "number"},
		{ID: "lateAssignments", Label: "Late Assignments", Value: float64(lateAssignments), Delta: delta(lateAssignments, 2), Trend: trendInverse(lateAssignments, 2), Format: "number"},
	}

	charts := []ChartData{
		buildAssignmentStatusChart(courses),
		buildAttendanceTrendChart(courses),
	}

	timeline := buildUpcomingTimeline(courses, snapshot.GeneratedAt)
	highlights := buildTeacherHighlights(courses)

	courseOverviews := make([]CourseOverview, 0, len(courses))
	for _, course := range courses {
		courseOverviews = append(courseOverviews, overviewFromCourse(course, snapshot.GeneratedAt))
	}

	return DashboardData{
		Role:        string(domain.RoleTeacher),
		Mode:        snapshot.Mode,
		GeneratedAt: snapshot.GeneratedAt,
		Summary:     summary,
		Charts:      charts,
		Highlights:  highlights,
		Timeline:    timeline,
		Courses:     courseOverviews,
	}
}

func buildStudentDashboard(snapshot domain.ClassroomSnapshot, user domain.User) DashboardData {
	courses, progress := filterCoursesByStudent(snapshot.Courses, user.Email)
	if len(courses) == 0 {
		return emptyDashboard(snapshot.Mode, user.Role, snapshot.GeneratedAt, []string{"No enrollments found for this student"})
	}

	totalCompleted := 0
	totalPending := 0
	var avgScore float64
	var attendance float64

	for _, p := range progress {
		totalCompleted += p.CompletedAssignments
		totalPending += p.PendingAssignments
		avgScore += p.AverageScore
		attendance += p.AttendanceRate
	}

	count := float64(len(progress))
	if count > 0 {
		avgScore = avgScore / count
		attendance = attendance / count
	}

	summary := []SummaryMetric{
		{ID: "completedAssignments", Label: "Completed Assignments", Value: float64(totalCompleted), Delta: delta(totalCompleted, 8), Trend: trend(totalCompleted, 8), Format: "number"},
		{ID: "pendingAssignments", Label: "Pending Assignments", Value: float64(totalPending), Delta: delta(totalPending, 3), Trend: trendInverse(totalPending, 3), Format: "number"},
		{ID: "averageScore", Label: "Average Score", Value: round2(avgScore), Delta: deltaFloat(avgScore, 88), Trend: trendFloat(avgScore, 88), Format: "percent"},
		{ID: "attendance", Label: "Attendance", Value: round2(attendance * 100), Delta: deltaFloat(attendance*100, 93), Trend: trendFloat(attendance*100, 93), Format: "percent"},
	}

	charts := []ChartData{
		buildStudentProgressChart(courses, progress),
	}

	timeline := buildUpcomingTimeline(courses, snapshot.GeneratedAt)
	highlights := buildStudentHighlights(courses, user.Email)

	courseOverviews := make([]CourseOverview, 0, len(courses))
	for _, course := range courses {
		courseOverviews = append(courseOverviews, overviewFromCourse(course, snapshot.GeneratedAt))
	}

	return DashboardData{
		Role:        string(domain.RoleStudent),
		Mode:        snapshot.Mode,
		GeneratedAt: snapshot.GeneratedAt,
		Summary:     summary,
		Charts:      charts,
		Highlights:  highlights,
		Timeline:    timeline,
		Courses:     courseOverviews,
	}
}

func overviewFromCourse(course domain.Course, now time.Time) CourseOverview {
	return CourseOverview{
		ID:                  course.ID,
		Name:                course.Name,
		Section:             course.Section,
		Program:             course.Program,
		PrimaryTeacher:      primaryTeacher(course),
		Enrollment:          len(course.Students),
		CompletionRate:      round2(courseCompletionRate(course)),
		UpcomingAssignments: upcomingAssignments(course, now),
		LastActivity:        course.LastActivity,
	}
}

func emptyDashboard(mode string, role domain.Role, generated time.Time, alerts []string) DashboardData {
	return DashboardData{
		Role:        string(role),
		Mode:        mode,
		GeneratedAt: generated,
		Summary:     []SummaryMetric{},
		Charts:      []ChartData{},
		Highlights:  []Highlight{},
		Alerts:      alerts,
	}
}

// Helper functions for calculations ------------------------------------------------

func primaryTeacher(course domain.Course) string {
	if len(course.Teachers) == 0 {
		return "Unassigned"
	}
	return course.Teachers[0].Name
}

func courseCompletionRate(course domain.Course) float64 {
	if len(course.Students) == 0 {
		return 0
	}
	total := 0.0
	for _, student := range course.Students {
		completed := float64(student.Progress.CompletedAssignments)
		totalAssignments := float64(student.Progress.CompletedAssignments + student.Progress.PendingAssignments)
		if totalAssignments == 0 {
			continue
		}
		total += (completed / totalAssignments) * 100
	}
	return total / float64(len(course.Students))
}

func averageCourseCompletion(courses []domain.Course) float64 {
	if len(courses) == 0 {
		return 0
	}
	total := 0.0
	count := 0
	for _, course := range courses {
		rate := courseCompletionRate(course)
		if rate > 0 {
			total += rate
			count++
		}
	}
	if count == 0 {
		return 0
	}
	return total / float64(count)
}

func globalOnTimeSubmissionRate(courses []domain.Course) float64 {
	completed := 0
	onTime := 0
	for _, course := range courses {
		for _, assignment := range course.Assignments {
			completed += assignment.Completed
			onTime += assignment.Completed - assignment.Late
		}
	}
	if completed == 0 {
		return 0
	}
	return (float64(onTime) / float64(completed)) * 100
}

func upcomingAssignments(course domain.Course, now time.Time) int {
	count := 0
	for _, assignment := range course.Assignments {
		if assignment.DueDate.After(now) {
			count++
		}
	}
	return count
}

func upcomingAssignmentsForCourses(courses []domain.Course, now time.Time) int {
	total := 0
	for _, course := range courses {
		total += upcomingAssignments(course, now)
	}
	return total
}

func lateAssignmentsForCourses(courses []domain.Course) int {
	total := 0
	for _, course := range courses {
		for _, assignment := range course.Assignments {
			total += assignment.Late
		}
	}
	return total
}

func totalEnrollment(courses []domain.Course) int {
	total := 0
	for _, course := range courses {
		total += len(course.Students)
	}
	return total
}

func uniqueStudentCount(courses []domain.Course) int {
	set := make(map[string]struct{})
	for _, course := range courses {
		for _, student := range course.Students {
			set[strings.ToLower(student.Person.Email)] = struct{}{}
		}
	}
	return len(set)
}

func countAtRiskCourses(courses []domain.Course) int {
	count := 0
	for _, course := range courses {
		if courseCompletionRate(course) < 75 || lateAssignmentsForCourses([]domain.Course{course}) > 3 {
			count++
		}
	}
	return count
}

func filterCoursesByCoordinator(courses []domain.Course, email string) []domain.Course {
	email = strings.ToLower(email)
	result := make([]domain.Course, 0)
	for _, course := range courses {
		if strings.ToLower(course.CoordinatorEmail) == email {
			result = append(result, course)
		}
	}
	return result
}

func filterCoursesByTeacher(courses []domain.Course, email string) []domain.Course {
	email = strings.ToLower(email)
	result := make([]domain.Course, 0)
	for _, course := range courses {
		for _, teacher := range course.Teachers {
			if strings.ToLower(teacher.Email) == email {
				result = append(result, course)
				break
			}
		}
	}
	return result
}

func filterCoursesByStudent(courses []domain.Course, email string) ([]domain.Course, []domain.StudentProgress) {
	email = strings.ToLower(email)
	resultCourses := make([]domain.Course, 0)
	progress := make([]domain.StudentProgress, 0)
	for _, course := range courses {
		for _, student := range course.Students {
			if strings.ToLower(student.Person.Email) == email {
				resultCourses = append(resultCourses, course)
				progress = append(progress, student.Progress)
				break
			}
		}
	}
	return resultCourses, progress
}

func buildSubmissionChart(courses []domain.Course) ChartData {
	type bucket struct {
		completed float64
		pending   float64
		date      time.Time
	}
	buckets := map[string]*bucket{}
	for _, course := range courses {
		for _, assignment := range course.Assignments {
			key := assignment.DueDate.Format("2006-01-02")
			b, ok := buckets[key]
			if !ok {
				b = &bucket{date: assignment.DueDate}
				buckets[key] = b
			}
			b.completed += float64(assignment.Completed)
			b.pending += float64(assignment.Pending)
		}
	}
	dates := make([]time.Time, 0, len(buckets))
	for _, b := range buckets {
		dates = append(dates, b.date)
	}
	sort.Slice(dates, func(i, j int) bool { return dates[i].Before(dates[j]) })

	categories := make([]string, 0, len(dates))
	completedData := make([]ChartPoint, 0, len(dates))
	pendingData := make([]ChartPoint, 0, len(dates))

	for _, date := range dates {
		key := date.Format("2006-01-02")
		b := buckets[key]
		label := date.Format("Jan 2")
		categories = append(categories, label)
		completedData = append(completedData, ChartPoint{X: label, Y: round1(b.completed)})
		pendingData = append(pendingData, ChartPoint{X: label, Y: round1(b.pending)})
	}

	return ChartData{
		ID:         "weeklySubmissions",
		Title:      "Weekly Submissions",
		Type:       "area",
		Categories: categories,
		Series: []ChartSeries{
			{Name: "Completed", Data: completedData},
			{Name: "Pending", Data: pendingData},
		},
	}
}

func buildCoursePerformanceChart(courses []domain.Course) ChartData {
	sort.Slice(courses, func(i, j int) bool {
		return courseCompletionRate(courses[i]) > courseCompletionRate(courses[j])
	})
	categories := make([]string, 0, len(courses))
	values := make([]ChartPoint, 0, len(courses))
	for _, course := range courses {
		categories = append(categories, course.Name)
		values = append(values, ChartPoint{X: course.Name, Y: round2(courseCompletionRate(course))})
	}
	return ChartData{
		ID:         "coursePerformance",
		Title:      "Course Completion Rate",
		Type:       "bar",
		Categories: categories,
		Series: []ChartSeries{
			{Name: "Completion %", Data: values},
		},
	}
}

func buildProgramDistributionChart(courses []domain.Course) ChartData {
	counts := make(map[string]float64)
	for _, course := range courses {
		counts[course.Program]++
	}
	programs := make([]string, 0, len(counts))
	for program := range counts {
		programs = append(programs, program)
	}
	sort.Strings(programs)
	points := make([]ChartPoint, 0, len(programs))
	for _, program := range programs {
		points = append(points, ChartPoint{X: program, Y: counts[program]})
	}
	return ChartData{
		ID:     "programDistribution",
		Title:  "Course Distribution by Program",
		Type:   "donut",
		Series: []ChartSeries{{Name: "Courses", Data: points}},
	}
}

func buildLateSubmissionChart(courses []domain.Course) ChartData {
	ordered := append([]domain.Course(nil), courses...)
	sort.Slice(ordered, func(i, j int) bool { return ordered[i].Name < ordered[j].Name })
	categories := make([]string, 0, len(ordered))
	values := make([]ChartPoint, 0, len(ordered))
	for _, course := range ordered {
		late := 0.0
		total := 0.0
		for _, assignment := range course.Assignments {
			late += float64(assignment.Late)
			total += float64(assignment.Completed + assignment.Pending)
		}
		categories = append(categories, course.Name)
		percentage := 0.0
		if total > 0 {
			percentage = (late / total) * 100
		}
		values = append(values, ChartPoint{X: course.Name, Y: round2(percentage)})
	}
	return ChartData{
		ID:         "lateSubmissions",
		Title:      "Late Submission Rate",
		Type:       "bar",
		Categories: categories,
		Series: []ChartSeries{
			{Name: "Late %", Data: values},
		},
	}
}

func buildAssignmentStatusChart(courses []domain.Course) ChartData {
	ordered := append([]domain.Course(nil), courses...)
	sort.Slice(ordered, func(i, j int) bool { return ordered[i].Name < ordered[j].Name })
	categories := make([]string, 0, len(ordered))
	completedSeries := make([]ChartPoint, 0, len(ordered))
	pendingSeries := make([]ChartPoint, 0, len(ordered))
	for _, course := range ordered {
		completed := 0.0
		pending := 0.0
		for _, assignment := range course.Assignments {
			completed += float64(assignment.Completed)
			pending += float64(assignment.Pending)
		}
		categories = append(categories, course.Name)
		completedSeries = append(completedSeries, ChartPoint{X: course.Name, Y: completed})
		pendingSeries = append(pendingSeries, ChartPoint{X: course.Name, Y: pending})
	}
	return ChartData{
		ID:         "assignmentStatus",
		Title:      "Assignment Status by Course",
		Type:       "bar",
		Categories: categories,
		Series: []ChartSeries{
			{Name: "Completed", Data: completedSeries},
			{Name: "Pending", Data: pendingSeries},
		},
	}
}

func buildAttendanceTrendChart(courses []domain.Course) ChartData {
	ordered := append([]domain.Course(nil), courses...)
	sort.Slice(ordered, func(i, j int) bool { return ordered[i].Name < ordered[j].Name })
	points := make([]ChartPoint, 0, len(ordered))
	for _, course := range ordered {
		rate := 0.0
		if len(course.Students) > 0 {
			total := 0.0
			for _, student := range course.Students {
				total += student.Progress.AttendanceRate
			}
			rate = (total / float64(len(course.Students))) * 100
		}
		points = append(points, ChartPoint{X: course.Name, Y: round2(rate)})
	}
	return ChartData{
		ID:     "attendanceTrend",
		Title:  "Average Attendance",
		Type:   "line",
		Series: []ChartSeries{{Name: "Attendance %", Data: points}},
	}
}

func buildStudentProgressChart(courses []domain.Course, progress []domain.StudentProgress) ChartData {
	pointsCompleted := make([]ChartPoint, 0, len(courses))
	pointsPending := make([]ChartPoint, 0, len(courses))
	for idx, course := range courses {
		if idx >= len(progress) {
			continue
		}
		pointsCompleted = append(pointsCompleted, ChartPoint{X: course.Name, Y: float64(progress[idx].CompletedAssignments)})
		pointsPending = append(pointsPending, ChartPoint{X: course.Name, Y: float64(progress[idx].PendingAssignments)})
	}
	return ChartData{
		ID:    "studentProgress",
		Title: "Assignments Progress",
		Type:  "bar",
		Series: []ChartSeries{
			{Name: "Completed", Data: pointsCompleted},
			{Name: "Pending", Data: pointsPending},
		},
	}
}

func buildUpcomingTimeline(courses []domain.Course, now time.Time) []TimelineItem {
	timeline := make([]TimelineItem, 0)
	for _, course := range courses {
		for _, assignment := range course.Assignments {
			if assignment.DueDate.After(now) && assignment.DueDate.Before(now.Add(14*24*time.Hour)) {
				status := "onTrack"
				if assignment.Pending > 0 {
					status = "pending"
				}
				if assignment.Late > 0 {
					status = "atRisk"
				}
				timeline = append(timeline, TimelineItem{
					ID:       assignment.ID,
					Title:    assignment.Title,
					DueDate:  assignment.DueDate,
					CourseID: course.ID,
					Status:   status,
				})
			}
		}
	}
	sort.Slice(timeline, func(i, j int) bool {
		return timeline[i].DueDate.Before(timeline[j].DueDate)
	})
	if len(timeline) > 8 {
		timeline = timeline[:8]
	}
	return timeline
}

func buildAdminHighlights(courses []domain.Course) []Highlight {
	highlights := []Highlight{}
	if len(courses) == 0 {
		return highlights
	}
	sort.Slice(courses, func(i, j int) bool {
		return courseCompletionRate(courses[i]) > courseCompletionRate(courses[j])
	})

	bestCourse := courses[0]
	highlights = append(highlights, Highlight{
		ID:      "highlight-top-course",
		Title:   "Top Performing Course",
		Details: fmt.Sprintf("%s leads with %.1f%% completion", bestCourse.Name, courseCompletionRate(bestCourse)),
		Status:  "success",
	})

	lateCourse := courses[0]
	maxLate := 0
	for _, course := range courses {
		late := lateAssignmentsForCourses([]domain.Course{course})
		if late > maxLate {
			maxLate = late
			lateCourse = course
		}
	}
	if maxLate > 0 {
		highlights = append(highlights, Highlight{
			ID:      "highlight-late-submissions",
			Title:   "Late Submissions Spike",
			Details: fmt.Sprintf("%s has %d late submissions", lateCourse.Name, maxLate),
			Status:  "warning",
		})
	}

	return highlights
}

func buildCoordinatorHighlights(courses []domain.Course) []Highlight {
	if len(courses) == 0 {
		return nil
	}
	sort.Slice(courses, func(i, j int) bool {
		return len(courses[i].Students) > len(courses[j].Students)
	})
	return []Highlight{
		{
			ID:      "highlight-enrollment",
			Title:   "Highest Enrollment",
			Details: fmt.Sprintf("%s hosts %d students", courses[0].Name, len(courses[0].Students)),
			Status:  "info",
		},
	}
}

func buildTeacherHighlights(courses []domain.Course) []Highlight {
	if len(courses) == 0 {
		return nil
	}
	highlights := []Highlight{}
	for _, course := range courses {
		if courseCompletionRate(course) >= 90 {
			highlights = append(highlights, Highlight{
				ID:      "highlight-course-" + course.ID,
				Title:   fmt.Sprintf("%s Engagement", course.Name),
				Details: fmt.Sprintf("Maintaining %.1f%% completion", courseCompletionRate(course)),
				Status:  "success",
			})
		}
	}
	return highlights
}

func buildStudentHighlights(courses []domain.Course, email string) []Highlight {
	highlights := []Highlight{}
	for _, course := range courses {
		progress := 0.0
		for _, student := range course.Students {
			if strings.ToLower(student.Person.Email) == strings.ToLower(email) {
				total := student.Progress.CompletedAssignments + student.Progress.PendingAssignments
				if total > 0 {
					progress = (float64(student.Progress.CompletedAssignments) / float64(total)) * 100
				}
				break
			}
		}
		if progress >= 90 {
			highlights = append(highlights, Highlight{
				ID:      "highlight-progress-" + course.ID,
				Title:   fmt.Sprintf("%s Progress", course.Name),
				Details: "Outstanding completion rate – keep it up!",
				Status:  "success",
			})
		}
	}
	return highlights
}

func buildAdminAlerts(courses []domain.Course) []string {
	alerts := []string{}
	for _, course := range courses {
		if lateAssignmentsForCourses([]domain.Course{course}) > 3 {
			alerts = append(alerts, fmt.Sprintf("Late submission spike detected in %s", course.Name))
		}
	}
	return alerts
}

func delta(value int, baseline int) float64 {
	return float64(value - baseline)
}

func deltaFloat(value float64, baseline float64) float64 {
	return round1(value - baseline)
}

func trend(value int, baseline int) string {
	diff := value - baseline
	switch {
	case diff > 0:
		return "up"
	case diff < 0:
		return "down"
	default:
		return "flat"
	}
}

func trendFloat(value float64, baseline float64) string {
	diff := value - baseline
	switch {
	case diff > 0.5:
		return "up"
	case diff < -0.5:
		return "down"
	default:
		return "flat"
	}
}

func trendInverse(value int, baseline int) string {
	diff := value - baseline
	switch {
	case diff < 0:
		return "up"
	case diff > 0:
		return "down"
	default:
		return "flat"
	}
}

func deltaAndTrend(value float64, baseline float64) (float64, string) {
	delta := round1(value - baseline)
	return delta, trendFloat(value, baseline)
}

func round1(value float64) float64 {
	return mathRound(value, 1)
}

func round2(value float64) float64 {
	return mathRound(value, 2)
}

func mathRound(value float64, precision int) float64 {
	if precision <= 0 {
		return float64(int(value + 0.5))
	}
	multiplier := math.Pow(10, float64(precision))
	return math.Round(value*multiplier) / multiplier
}
