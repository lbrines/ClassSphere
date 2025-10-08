# ========================================
# ClassSphere Workspace - Development Tools
# Following CONTAINERS_BEST_PRACTICES.md
# Using Go 1.23.5 (latest official version)
# ========================================

FROM golang:1.23.5-bookworm

LABEL maintainer="ClassSphere Team"
LABEL description="ClassSphere Workspace - Go 1.23.5 + Node.js 20 + Dev Tools"
LABEL version="1.0.0"

# Enable automatic toolchain download
ENV GOTOOLCHAIN=auto

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    bash \
    make \
    build-essential \
    redis-tools \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Go development tools
RUN go install github.com/air-verse/air@v1.52.3 && \
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.61.0 && \
    go install golang.org/x/tools/gopls@v0.14.2 && \
    chmod -R 777 /go

# Install Node.js global tools
RUN npm install -g @angular/cli@19

# Note: VS Code Dev Containers handles user creation automatically
# No need to create vscode user manually

# Set up workspace
WORKDIR /workspace

# Keep container running
CMD ["sleep", "infinity"]
