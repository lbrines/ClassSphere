package domain

// SearchEntity represents the type of entity to search.
type SearchEntity string

const (
	SearchEntityStudent     SearchEntity = "students"
	SearchEntityTeacher     SearchEntity = "teachers"
	SearchEntityCourse      SearchEntity = "courses"
	SearchEntityAssignment  SearchEntity = "assignments"
	SearchEntityAnnouncement SearchEntity = "announcements"
)

// IsValid checks if the search entity type is valid.
func (se SearchEntity) IsValid() bool {
	switch se {
	case SearchEntityStudent, SearchEntityTeacher, SearchEntityCourse, 
	     SearchEntityAssignment, SearchEntityAnnouncement:
		return true
	default:
		return false
	}
}

// SearchResult represents a unified search result across different entity types.
type SearchResult struct {
	Type        SearchEntity           `json:"type"`
	ID          string                 `json:"id"`
	Title       string                 `json:"title"`
	Description string                 `json:"description,omitempty"`
	Meta        map[string]interface{} `json:"meta,omitempty"`
	Relevance   float64                `json:"relevance"`
}

// SearchQuery represents search parameters.
type SearchQuery struct {
	Query    string         // Search term
	Entities []SearchEntity // Which entities to search
	Role     Role           // User role for filtering
	UserID   string         // User ID for personalized results
	Limit    int            // Max results per entity
}

// SearchResponse contains search results grouped by entity type.
type SearchResponse struct {
	Query   string                   `json:"query"`
	Total   int                      `json:"total"`
	Results map[SearchEntity][]SearchResult `json:"results"`
}

