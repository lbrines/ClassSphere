package app

import "time"

// SummaryMetric powers the KPI cards displayed on dashboards.
type SummaryMetric struct {
	ID     string  `json:"id"`
	Label  string  `json:"label"`
	Value  float64 `json:"value"`
	Delta  float64 `json:"delta"`
	Trend  string  `json:"trend"`
	Format string  `json:"format,omitempty"`
}

// ChartData represents an ApexCharts-compatible data structure.
type ChartData struct {
	ID         string        `json:"id"`
	Title      string        `json:"title"`
	Type       string        `json:"type"`
	Series     []ChartSeries `json:"series"`
	Categories []string      `json:"categories,omitempty"`
}

// ChartSeries represents a chart series with its datapoints.
type ChartSeries struct {
	Name string       `json:"name"`
	Data []ChartPoint `json:"data"`
}

// ChartPoint contains a single data point.
type ChartPoint struct {
	X interface{} `json:"x"`
	Y float64     `json:"y"`
}

// Highlight captures qualitative achievements or alerts.
type Highlight struct {
	ID      string `json:"id"`
	Title   string `json:"title"`
	Details string `json:"details"`
	Status  string `json:"status"`
}

// CourseOverview provides a concise summary for course listings.
type CourseOverview struct {
	ID                  string    `json:"id"`
	Name                string    `json:"name"`
	Section             string    `json:"section"`
	Program             string    `json:"program"`
	PrimaryTeacher      string    `json:"primaryTeacher"`
	Enrollment          int       `json:"enrollment"`
	CompletionRate      float64   `json:"completionRate"`
	UpcomingAssignments int       `json:"upcomingAssignments"`
	LastActivity        time.Time `json:"lastActivity"`
}

// TimelineItem represents upcoming or past events relevant to the dashboard.
type TimelineItem struct {
	ID       string    `json:"id"`
	Title    string    `json:"title"`
	DueDate  time.Time `json:"dueDate"`
	CourseID string    `json:"courseId"`
	Status   string    `json:"status"`
}

// DashboardData is the response payload consumed by the frontend dashboards.
type DashboardData struct {
	Role        string           `json:"role"`
	Mode        string           `json:"mode"`
	GeneratedAt time.Time        `json:"generatedAt"`
	Summary     []SummaryMetric  `json:"summary"`
	Charts      []ChartData      `json:"charts"`
	Highlights  []Highlight      `json:"highlights"`
	Courses     []CourseOverview `json:"courses,omitempty"`
	Timeline    []TimelineItem   `json:"timeline,omitempty"`
	Alerts      []string         `json:"alerts,omitempty"`
}
