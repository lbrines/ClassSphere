# Multi-stage build for Go backend - using custom Go 1.24.7
FROM debian:bookworm-slim AS base

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    bash \
    make \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Go 1.24.7 from local workspace
COPY workspace/tools/go1.24.7.linux-amd64.tar.gz /tmp/
WORKDIR /tmp
RUN rm -rf /usr/local/go && \
    tar -C /usr/local -xzf go1.24.7.linux-amd64.tar.gz && \
    rm go1.24.7.linux-amd64.tar.gz

# Set Go environment
ENV PATH="/usr/local/go/bin:/go/bin:$PATH"
ENV GOPATH="/go"

# Set up workspace
WORKDIR /app

# Install Go tools (skip air for now, will be installed via post-create)
RUN go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest && \
    chmod -R 777 /go

# Default command - use go run directly
CMD ["go", "run", "cmd/api/main.go"]

