FROM golang:1.23-bookworm

# Install all development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    bash \
    make \
    build-essential \
    redis-tools \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Go development tools
# Note: Using compatible versions with Go 1.23
RUN go install github.com/air-verse/air@v1.52.3 && \
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.61.0 && \
    go install golang.org/x/tools/gopls@v0.14.2 && \
    chmod -R 777 /go

# Install Node.js global tools
RUN npm install -g @angular/cli@19

# Set up workspace
WORKDIR /workspace

# Keep container running
CMD ["sleep", "infinity"]

