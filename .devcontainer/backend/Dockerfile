# ========================================
# ClassSphere Backend - Multi-Stage Build
# Following CONTAINERS_BEST_PRACTICES.md
# Using Go 1.24 latest (fixes security vulnerabilities)
# ========================================

# ========================================
# Stage 1: Base with Go 1.24
# ========================================
FROM golang:1.24-bookworm AS base

LABEL maintainer="ClassSphere Team"
LABEL description="ClassSphere Backend - Go 1.24 + Echo v4"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    bash \
    make \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ========================================
# Stage 2: Dependencies (cacheable layer)
# ========================================
FROM base AS deps

WORKDIR /app

# Copy only dependency files (better cache)
COPY backend/go.mod backend/go.sum ./

# Download dependencies
RUN go mod download && \
    chmod -R 777 /go

# ========================================
# Stage 3: Development (Dev Containers)
# ========================================
FROM deps AS development

WORKDIR /app

# Install development tools
RUN go install github.com/air-verse/air@v1.52.3 && \
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.61.0 && \
    chmod -R 777 /go

# Note: VS Code Dev Containers handles user creation automatically

# Code will be mounted via volume in runtime

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8080/health || exit 1

# Command for development (hot reload)
CMD ["go", "run", "cmd/api/main.go"]

# ========================================
# Stage 4: Builder (Compilation)
# ========================================
FROM deps AS builder

WORKDIR /app

# Copy source code
COPY backend/ ./

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build \
    -a -installsuffix cgo \
    -ldflags="-w -s" \
    -o /app/classsphere-backend ./cmd/api

# ========================================
# Stage 5: Production (Minimal)
# ========================================
FROM scratch AS production

LABEL maintainer="ClassSphere Team"
LABEL description="ClassSphere Backend - Production"
LABEL version="1.0.0"

# Copy SSL certificates
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/classsphere-backend /app

# Expose port
EXPOSE 8080

# Command
ENTRYPOINT ["/app"]
