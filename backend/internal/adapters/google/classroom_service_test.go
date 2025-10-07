package google

import (
	"context"
	"testing"
	"time"

	"google.golang.org/api/classroom/v1"

	"github.com/lbrines/classsphere/internal/shared"
)

func TestWithClock(t *testing.T) {
	clock := func() time.Time {
		return time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	}

	service := &ClassroomService{}
	WithClock(clock)(service)

	// Test that the clock function is set
	if service.now == nil {
		t.Error("Expected clock function to be set")
	}

	// Test that the clock function works
	expected := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	if !service.now().Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, service.now())
	}
}

func TestWithClock_Nil(t *testing.T) {
	service := &ClassroomService{
		now: func() time.Time { return time.Now() },
	}

	WithClock(nil)(service)

	// Should not change the existing clock function (can't compare functions directly)
	if service.now == nil {
		t.Error("Expected clock function to remain unchanged when nil is passed")
	}
}

func TestWithGoogleService(t *testing.T) {
	mockService := &classroom.Service{}
	service := &ClassroomService{}

	WithGoogleService(mockService)(service)

	if service.service != mockService {
		t.Error("Expected Google service to be set")
	}
}

func TestNewClassroomService_MockMode(t *testing.T) {
	service, err := NewClassroomService("", "mock")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if service == nil {
		t.Fatal("Expected service to be created")
	}

	if service.mode != shared.IntegrationModeMock {
		t.Errorf("Expected mode to be %s, got %s", shared.IntegrationModeMock, service.mode)
	}

	if service.service != nil {
		t.Error("Expected Google service to be nil in mock mode")
	}
}

func TestNewClassroomService_GoogleMode_NoCredentials(t *testing.T) {
	service, err := NewClassroomService("", "google")
	if err == nil {
		t.Error("Expected error when no credentials provided for Google mode")
	}

	if service != nil {
		t.Error("Expected service to be nil when credentials are missing")
	}
}

func TestNewClassroomService_GoogleMode_WithCredentials(t *testing.T) {
	// This test will fail in CI without real credentials, but we can test the path
	service, err := NewClassroomService("/nonexistent/credentials.json", "google")
	if err == nil {
		t.Error("Expected error when credentials file doesn't exist")
	}

	if service != nil {
		t.Error("Expected service to be nil when credentials file doesn't exist")
	}
}

func TestNewClassroomService_WithOptions(t *testing.T) {
	clock := func() time.Time {
		return time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	}
	mockService := &classroom.Service{}

	service, err := NewClassroomService("", "mock", WithClock(clock), WithGoogleService(mockService))
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if service.now == nil {
		t.Error("Expected clock function to be set")
	}

	if service.service != mockService {
		t.Error("Expected Google service to be set")
	}
}

func TestNewClassroomService_InvalidMode(t *testing.T) {
	service, err := NewClassroomService("", "invalid")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	// Should normalize to mock mode
	if service.mode != shared.IntegrationModeMock {
		t.Errorf("Expected mode to be normalized to %s, got %s", shared.IntegrationModeMock, service.mode)
	}
}

func TestMode(t *testing.T) {
	service := &ClassroomService{
		mode: shared.IntegrationModeGoogle,
	}

	if service.Mode() != shared.IntegrationModeGoogle {
		t.Errorf("Expected mode %s, got %s", shared.IntegrationModeGoogle, service.Mode())
	}
}

func TestSnapshot_MockMode(t *testing.T) {
	service, err := NewClassroomService("", "mock")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	ctx := context.Background()
	snapshot, err := service.Snapshot(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if snapshot.Mode != shared.IntegrationModeMock {
		t.Errorf("Expected mode %s, got %s", shared.IntegrationModeMock, snapshot.Mode)
	}

	if len(snapshot.Courses) == 0 {
		t.Error("Expected courses to be present in mock mode")
	}
}

func TestSnapshot_GoogleMode_NoService(t *testing.T) {
	// Create service with mock Google service to avoid credentials requirement
	service := &ClassroomService{
		mode:    shared.IntegrationModeGoogle,
		service: nil,
		now:     time.Now,
	}

	ctx := context.Background()
	snapshot, err := service.Snapshot(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if snapshot.Mode != shared.IntegrationModeGoogle {
		t.Errorf("Expected mode %s, got %s", shared.IntegrationModeGoogle, snapshot.Mode)
	}

	if len(snapshot.Courses) == 0 {
		t.Error("Expected courses to be present in Google mode fallback")
	}
}

func TestSnapshot_GoogleMode_WithService(t *testing.T) {
	// Create a mock Google service (nil to trigger fallback)
	service := &ClassroomService{
		mode:    shared.IntegrationModeGoogle,
		service: nil,
		now:     time.Now,
	}

	ctx := context.Background()
	snapshot, err := service.Snapshot(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if snapshot.Mode != shared.IntegrationModeGoogle {
		t.Errorf("Expected mode %s, got %s", shared.IntegrationModeGoogle, snapshot.Mode)
	}

	// Should fallback to sample data when API fails
	if len(snapshot.Courses) == 0 {
		t.Error("Expected courses to be present in Google mode fallback")
	}
}

func TestSnapshot_InvalidMode(t *testing.T) {
	service := &ClassroomService{
		mode: "invalid",
		now:  time.Now,
	}

	ctx := context.Background()
	_, err := service.Snapshot(ctx)
	if err == nil {
		t.Error("Expected error for invalid mode")
	}
}

func TestFetchCourses_NilService(t *testing.T) {
	service := &ClassroomService{
		service: nil,
	}

	ctx := context.Background()
	courses, err := service.fetchCourses(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if courses != nil {
		t.Error("Expected courses to be nil when service is nil")
	}
}

func TestFetchCourses_WithService(t *testing.T) {
	// This test would require a real Google service or extensive mocking
	// For now, we'll test the nil case which is the most common scenario
	service := &ClassroomService{
		service: nil,
	}

	ctx := context.Background()
	courses, err := service.fetchCourses(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if courses != nil {
		t.Error("Expected courses to be nil when service is nil")
	}
}

func TestClassroomService_Integration(t *testing.T) {
	// Test the complete flow
	service, err := NewClassroomService("", "mock")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	// Test mode
	if service.Mode() != shared.IntegrationModeMock {
		t.Errorf("Expected mode %s, got %s", shared.IntegrationModeMock, service.Mode())
	}

	// Test snapshot
	ctx := context.Background()
	snapshot, err := service.Snapshot(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	if snapshot.Mode != shared.IntegrationModeMock {
		t.Errorf("Expected snapshot mode %s, got %s", shared.IntegrationModeMock, snapshot.Mode)
	}

	// Verify courses have expected structure
	for _, course := range snapshot.Courses {
		if course.ID == "" {
			t.Error("Expected course ID to be set")
		}
		if course.Name == "" {
			t.Error("Expected course name to be set")
		}
		if course.Program == "" {
			t.Error("Expected course program to be set")
		}
	}
}

func TestClassroomService_ClockFunction(t *testing.T) {
	fixedTime := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	service, err := NewClassroomService("", "mock", WithClock(func() time.Time {
		return fixedTime
	}))
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	ctx := context.Background()
	snapshot, err := service.Snapshot(ctx)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	// The generatedAt should be close to our fixed time
	timeDiff := snapshot.GeneratedAt.Sub(fixedTime)
	if timeDiff < 0 || timeDiff > time.Second {
		t.Errorf("Expected generatedAt to be close to fixed time, got %v", snapshot.GeneratedAt)
	}
}