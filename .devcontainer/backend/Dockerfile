# ========================================
# ClassSphere Backend - Multi-Stage Build
# Following CONTAINERS_BEST_PRACTICES.md
# Using Go 1.23.5 base + downloading Go 1.24 manually
# ========================================

# ========================================
# Stage 1: Base with Go 1.24 downloaded
# ========================================
FROM golang:1.23.5-bookworm AS base

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
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install Go 1.24 from golang.org (using latest available)
# Note: Go 1.24 may not be officially released yet, trying 1.24rc versions or using GOTOOLCHAIN
RUN wget -q https://go.dev/dl/go1.24rc2.linux-amd64.tar.gz -O /tmp/go1.24.tar.gz 2>/dev/null || \
    (echo "Go 1.24 not available, will use GOTOOLCHAIN=auto" && touch /tmp/no-go124)

# Install Go 1.24 if downloaded, otherwise rely on GOTOOLCHAIN
RUN if [ ! -f /tmp/no-go124 ]; then \
        rm -rf /usr/local/go && \
        tar -C /usr/local -xzf /tmp/go1.24.tar.gz && \
        rm /tmp/go1.24.tar.gz; \
    fi

# Set GOTOOLCHAIN to auto as fallback
ENV GOTOOLCHAIN=auto

# ========================================
# Stage 2: Dependencies (cacheable layer)
# ========================================
FROM base AS deps

WORKDIR /app

# Copy only dependency files (better cache)
COPY backend/go.mod backend/go.sum ./

# Download dependencies (Go will auto-download 1.24 toolchain if needed)
RUN go mod download && \
    chmod -R 777 /go

# ========================================
# Stage 3: Development (Dev Containers)
# ========================================
FROM deps AS development

WORKDIR /app

# Install development tools (will use Go 1.24 toolchain automatically)
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
