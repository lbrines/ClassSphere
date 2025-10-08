package repo

import (
	"context"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"google.golang.org/api/classroom/v1"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
)

const (
	// Cache TTL for search results (5 minutes)
	searchCacheTTL = 300
	// Cache key prefix
	searchCachePrefix = "search:"
)

// ClassroomSearchRepository implements search functionality using Google Classroom API.
type ClassroomSearchRepository struct {
	service *classroom.Service
	cache   ports.Cache
}

// NewClassroomSearchRepository creates a new repository for searching Google Classroom data.
func NewClassroomSearchRepository(service *classroom.Service, cache ports.Cache) *ClassroomSearchRepository {
	return &ClassroomSearchRepository{
		service: service,
		cache:   cache,
	}
}

// SearchCourses searches for courses in Google Classroom with caching.
func (r *ClassroomSearchRepository) SearchCourses(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error) {
	if r.service == nil {
		return nil, 0, fmt.Errorf("google classroom service not initialized")
	}

	// Try cache first
	cacheKey := r.buildCacheKey("courses", query, limit, offset)
	if cached, err := r.getFromCache(ctx, cacheKey); err == nil && cached != nil {
		return cached.Results, cached.Total, nil
	}

	// Fetch courses from Google Classroom API
	call := r.service.Courses.List()
	call.PageSize(100) // Fetch more to allow filtering
	
	resp, err := call.Context(ctx).Do()
	if err != nil {
		return nil, 0, fmt.Errorf("fetch courses from google: %w", err)
	}

	// Filter courses by query
	queryLower := strings.ToLower(query)
	var allMatches []domain.SearchResult

	for _, course := range resp.Courses {
		nameLower := strings.ToLower(course.Name)
		descLower := strings.ToLower(course.DescriptionHeading)
		sectionLower := strings.ToLower(course.Section)

		// Check if query matches name, description, or section
		if strings.Contains(nameLower, queryLower) || 
		   strings.Contains(descLower, queryLower) || 
		   strings.Contains(sectionLower, queryLower) {
			
			// Calculate relevance
			relevance := 0.5
			if strings.HasPrefix(nameLower, queryLower) {
				relevance = 1.0
			} else if strings.Contains(nameLower, queryLower) {
				relevance = 0.8
			} else if strings.Contains(descLower, queryLower) {
				relevance = 0.6
			}

			result := domain.SearchResult{
				Type:        domain.SearchEntityCourse,
				ID:          course.Id,
				Title:       course.Name,
				Description: course.DescriptionHeading,
				Meta: map[string]interface{}{
					"section":        course.Section,
					"room":           course.Room,
					"ownerId":        course.OwnerId,
					"courseState":    course.CourseState,
					"enrollmentCode": course.EnrollmentCode,
				},
				Relevance: relevance,
			}

			allMatches = append(allMatches, result)
		}
	}

	// Sort by relevance
	sortByRelevanceSlice(allMatches)

	// Apply pagination
	total := len(allMatches)
	start := offset
	end := offset + limit

	if start >= total {
		return []domain.SearchResult{}, total, nil
	}
	if end > total {
		end = total
	}

	return allMatches[start:end], total, nil
}

// SearchStudents searches for students in Google Classroom courses.
func (r *ClassroomSearchRepository) SearchStudents(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error) {
	if r.service == nil {
		return nil, 0, fmt.Errorf("google classroom service not initialized")
	}

	queryLower := strings.ToLower(query)
	var allMatches []domain.SearchResult

	// First, get all courses
	coursesResp, err := r.service.Courses.List().Context(ctx).Do()
	if err != nil {
		return nil, 0, fmt.Errorf("fetch courses: %w", err)
	}

	// For each course, get students
	for _, course := range coursesResp.Courses {
		studentsResp, err := r.service.Courses.Students.List(course.Id).Context(ctx).Do()
		if err != nil {
			// Skip courses where we can't access students
			continue
		}

		for _, student := range studentsResp.Students {
			profile := student.Profile
			if profile == nil {
				continue
			}

			nameLower := strings.ToLower(profile.Name.FullName)
			emailLower := strings.ToLower(profile.EmailAddress)

			// Check if query matches name or email
			if strings.Contains(nameLower, queryLower) || strings.Contains(emailLower, queryLower) {
				relevance := 0.7
				if strings.HasPrefix(nameLower, queryLower) {
					relevance = 1.0
				} else if strings.HasPrefix(emailLower, queryLower) {
					relevance = 0.9
				}

				result := domain.SearchResult{
					Type:        domain.SearchEntityStudent,
					ID:          student.UserId,
					Title:       profile.Name.FullName,
					Description: profile.EmailAddress,
					Meta: map[string]interface{}{
						"courseId":   course.Id,
						"courseName": course.Name,
						"photoUrl":   profile.PhotoUrl,
					},
					Relevance: relevance,
				}

				allMatches = append(allMatches, result)
			}
		}
	}

	// Remove duplicates (same student in multiple courses)
	uniqueMatches := r.deduplicateStudents(allMatches)
	sortByRelevanceSlice(uniqueMatches)

	// Apply pagination
	total := len(uniqueMatches)
	start := offset
	end := offset + limit

	if start >= total {
		return []domain.SearchResult{}, total, nil
	}
	if end > total {
		end = total
	}

	return uniqueMatches[start:end], total, nil
}

// SearchTeachers searches for teachers in Google Classroom courses.
func (r *ClassroomSearchRepository) SearchTeachers(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error) {
	if r.service == nil {
		return nil, 0, fmt.Errorf("google classroom service not initialized")
	}

	queryLower := strings.ToLower(query)
	var allMatches []domain.SearchResult

	// Get all courses
	coursesResp, err := r.service.Courses.List().Context(ctx).Do()
	if err != nil {
		return nil, 0, fmt.Errorf("fetch courses: %w", err)
	}

	// For each course, get teachers
	for _, course := range coursesResp.Courses {
		teachersResp, err := r.service.Courses.Teachers.List(course.Id).Context(ctx).Do()
		if err != nil {
			// Skip courses where we can't access teachers
			continue
		}

		for _, teacher := range teachersResp.Teachers {
			profile := teacher.Profile
			if profile == nil {
				continue
			}

			nameLower := strings.ToLower(profile.Name.FullName)
			emailLower := strings.ToLower(profile.EmailAddress)

			if strings.Contains(nameLower, queryLower) || strings.Contains(emailLower, queryLower) {
				relevance := 0.7
				if strings.HasPrefix(nameLower, queryLower) {
					relevance = 1.0
				}

				result := domain.SearchResult{
					Type:        domain.SearchEntityTeacher,
					ID:          teacher.UserId,
					Title:       profile.Name.FullName,
					Description: profile.EmailAddress,
					Meta: map[string]interface{}{
						"courseId":   course.Id,
						"courseName": course.Name,
						"photoUrl":   profile.PhotoUrl,
					},
					Relevance: relevance,
				}

				allMatches = append(allMatches, result)
			}
		}
	}

	// Remove duplicates
	uniqueMatches := r.deduplicateTeachers(allMatches)
	sortByRelevanceSlice(uniqueMatches)

	// Apply pagination
	total := len(uniqueMatches)
	start := offset
	end := offset + limit

	if start >= total {
		return []domain.SearchResult{}, total, nil
	}
	if end > total {
		end = total
	}

	return uniqueMatches[start:end], total, nil
}

// SearchAssignments searches for assignments/coursework in Google Classroom.
func (r *ClassroomSearchRepository) SearchAssignments(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error) {
	if r.service == nil {
		return nil, 0, fmt.Errorf("google classroom service not initialized")
	}

	queryLower := strings.ToLower(query)
	var allMatches []domain.SearchResult

	// Get all courses
	coursesResp, err := r.service.Courses.List().Context(ctx).Do()
	if err != nil {
		return nil, 0, fmt.Errorf("fetch courses: %w", err)
	}

	// For each course, get coursework (assignments)
	for _, course := range coursesResp.Courses {
		courseworkResp, err := r.service.Courses.CourseWork.List(course.Id).Context(ctx).Do()
		if err != nil {
			// Skip courses where we can't access coursework
			continue
		}

		for _, work := range courseworkResp.CourseWork {
			titleLower := strings.ToLower(work.Title)
			descLower := strings.ToLower(work.Description)

			if strings.Contains(titleLower, queryLower) || strings.Contains(descLower, queryLower) {
				relevance := 0.6
				if strings.HasPrefix(titleLower, queryLower) {
					relevance = 1.0
				} else if strings.Contains(titleLower, queryLower) {
					relevance = 0.8
				}

				result := domain.SearchResult{
					Type:        domain.SearchEntityAssignment,
					ID:          work.Id,
					Title:       work.Title,
					Description: work.Description,
					Meta: map[string]interface{}{
						"courseId":       course.Id,
						"courseName":     course.Name,
						"state":          work.State,
						"maxPoints":      work.MaxPoints,
						"workType":       work.WorkType,
						"dueDate":        formatDueDate(work.DueDate, work.DueTime),
						"alternateLink":  work.AlternateLink,
						"creatorUserId":  work.CreatorUserId,
					},
					Relevance: relevance,
				}

				allMatches = append(allMatches, result)
			}
		}
	}

	sortByRelevanceSlice(allMatches)

	// Apply pagination
	total := len(allMatches)
	start := offset
	end := offset + limit

	if start >= total {
		return []domain.SearchResult{}, total, nil
	}
	if end > total {
		end = total
	}

	return allMatches[start:end], total, nil
}

// SearchAnnouncements searches for announcements in Google Classroom.
func (r *ClassroomSearchRepository) SearchAnnouncements(ctx context.Context, query string, limit int, offset int) ([]domain.SearchResult, int, error) {
	if r.service == nil {
		return nil, 0, fmt.Errorf("google classroom service not initialized")
	}

	queryLower := strings.ToLower(query)
	var allMatches []domain.SearchResult

	// Get all courses
	coursesResp, err := r.service.Courses.List().Context(ctx).Do()
	if err != nil {
		return nil, 0, fmt.Errorf("fetch courses: %w", err)
	}

	// For each course, get announcements
	for _, course := range coursesResp.Courses {
		announcementsResp, err := r.service.Courses.Announcements.List(course.Id).Context(ctx).Do()
		if err != nil {
			// Skip courses where we can't access announcements
			continue
		}

		for _, announcement := range announcementsResp.Announcements {
			textLower := strings.ToLower(announcement.Text)

			if strings.Contains(textLower, queryLower) {
				relevance := 0.5
				if strings.HasPrefix(textLower, queryLower) {
					relevance = 1.0
				}

				result := domain.SearchResult{
					Type:        domain.SearchEntityAnnouncement,
					ID:          announcement.Id,
					Title:       truncate(announcement.Text, 100),
					Description: announcement.Text,
					Meta: map[string]interface{}{
						"courseId":       course.Id,
						"courseName":     course.Name,
						"state":          announcement.State,
						"alternateLink":  announcement.AlternateLink,
						"creatorUserId":  announcement.CreatorUserId,
						"creationTime":   announcement.CreationTime,
					},
					Relevance: relevance,
				}

				allMatches = append(allMatches, result)
			}
		}
	}

	sortByRelevanceSlice(allMatches)

	// Apply pagination
	total := len(allMatches)
	start := offset
	end := offset + limit

	if start >= total {
		return []domain.SearchResult{}, total, nil
	}
	if end > total {
		end = total
	}

	return allMatches[start:end], total, nil
}

// Helper functions

func (r *ClassroomSearchRepository) deduplicateStudents(results []domain.SearchResult) []domain.SearchResult {
	seen := make(map[string]bool)
	unique := make([]domain.SearchResult, 0)

	for _, result := range results {
		if !seen[result.ID] {
			seen[result.ID] = true
			unique = append(unique, result)
		}
	}

	return unique
}

func (r *ClassroomSearchRepository) deduplicateTeachers(results []domain.SearchResult) []domain.SearchResult {
	seen := make(map[string]bool)
	unique := make([]domain.SearchResult, 0)

	for _, result := range results {
		if !seen[result.ID] {
			seen[result.ID] = true
			unique = append(unique, result)
		}
	}

	return unique
}

func sortByRelevanceSlice(results []domain.SearchResult) {
	// Bubble sort for relevance (descending)
	n := len(results)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			if results[j].Relevance < results[j+1].Relevance {
				results[j], results[j+1] = results[j+1], results[j]
			}
		}
	}
}

func formatDueDate(dueDate *classroom.Date, dueTime *classroom.TimeOfDay) string {
	if dueDate == nil {
		return ""
	}

	year := int(dueDate.Year)
	month := int(dueDate.Month)
	day := int(dueDate.Day)

	var hour, minute int
	if dueTime != nil {
		hour = int(dueTime.Hours)
		minute = int(dueTime.Minutes)
	}

	t := time.Date(year, time.Month(month), day, hour, minute, 0, 0, time.UTC)
	return t.Format(time.RFC3339)
}

func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen-3] + "..."
}

// Cache helper structures

type cachedSearchResults struct {
	Results []domain.SearchResult
	Total   int
}

// buildCacheKey creates a deterministic cache key for search queries.
func (r *ClassroomSearchRepository) buildCacheKey(entity, query string, limit, offset int) string {
	// Create hash of query parameters for consistent keys
	data := fmt.Sprintf("%s:%s:%d:%d", entity, query, limit, offset)
	hash := sha256.Sum256([]byte(data))
	return fmt.Sprintf("%s%s:%x", searchCachePrefix, entity, hash[:8])
}

// getFromCache retrieves cached search results.
func (r *ClassroomSearchRepository) getFromCache(ctx context.Context, key string) (*cachedSearchResults, error) {
	if r.cache == nil {
		return nil, fmt.Errorf("cache not available")
	}

	data, err := r.cache.Get(ctx, key)
	if err != nil || data == nil {
		return nil, err
	}

	var cached cachedSearchResults
	if err := json.Unmarshal(data, &cached); err != nil {
		return nil, err
	}

	return &cached, nil
}

// saveToCache stores search results in cache.
func (r *ClassroomSearchRepository) saveToCache(ctx context.Context, key string, results []domain.SearchResult, total int) {
	if r.cache == nil {
		return
	}

	cached := cachedSearchResults{
		Results: results,
		Total:   total,
	}

	data, err := json.Marshal(cached)
	if err != nil {
		return
	}

	_ = r.cache.Set(ctx, key, data, searchCacheTTL)
}

