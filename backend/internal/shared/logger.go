package shared

import (
	"log"
	"os"
	"sync"
)

var (
	logger     *log.Logger
	loggerOnce sync.Once
)

// Logger returns a shared logger configured for the current environment.
// TODO: Upgrade to log/slog when Go 1.21+ is available
func Logger() *log.Logger {
	loggerOnce.Do(func() {
		logger = log.New(os.Stdout, "classsphere: ", log.LstdFlags|log.Lshortfile)
	})
	return logger
}
