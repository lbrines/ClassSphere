# ========================================
# ClassSphere Frontend - Multi-Stage Build
# Following CONTAINERS_BEST_PRACTICES.md
# ========================================

# ========================================
# Stage 1: Dependencies Installation
# ========================================
FROM node:20.18.1-slim AS deps

LABEL maintainer="ClassSphere Team"
LABEL description="ClassSphere Frontend - Angular 19 + TailwindCSS"
LABEL version="1.0.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files (better cache)
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies (cached if package files don't change)
RUN npm ci

# ========================================
# Stage 2: Development (Dev Containers)
# ========================================
FROM node:20.18.1-slim AS development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Angular CLI globally
RUN npm install -g @angular/cli@19

# Copy node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY frontend/package*.json ./

# Note: VS Code Dev Containers handles user creation automatically
# No need to create vscode user manually

# Code will be mounted via volume in runtime

# Expose port
EXPOSE 4200

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:4200 || exit 1

# Command for development (hot reload)
CMD ["npm", "start"]

# ========================================
# Stage 3: Builder
# ========================================
FROM deps AS builder

WORKDIR /app

# Copy source code
COPY frontend/ ./

# Build for production
RUN npm run build

# ========================================
# Stage 4: Production (Nginx) with Runtime Config
# ========================================
FROM nginx:1.27.3-alpine AS production

LABEL maintainer="ClassSphere Team"
LABEL description="ClassSphere Frontend - Production with Runtime Config"
LABEL version="1.0.0"

# Copy build output from builder
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Copy runtime environment generation script
COPY frontend/generate-env.sh /docker-entrypoint.d/00-generate-env.sh

# Make script executable and set proper permissions
RUN chmod +x /docker-entrypoint.d/00-generate-env.sh

# Copy custom nginx configuration (if exists)
# COPY nginx.conf /etc/nginx/nginx.conf

# Create non-root user (nginx-user)
RUN addgroup -g 1001 nginx-user 2>/dev/null || true && \
    adduser -D -u 1001 -G nginx-user nginx-user 2>/dev/null || true && \
    chown -R nginx-user:nginx-user /usr/share/nginx/html && \
    chown -R nginx-user:nginx-user /var/cache/nginx && \
    chown -R nginx-user:nginx-user /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx-user:nginx-user /var/run/nginx.pid

# Environment variables with defaults (can be overridden at runtime)
# This implements 12-Factor App Config principle
ENV API_URL=http://localhost:8080/api/v1

# Switch to root temporarily for entrypoint scripts
USER root

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

EXPOSE 80

# Nginx will run entrypoint scripts in /docker-entrypoint.d/ before starting
CMD ["nginx", "-g", "daemon off;"]
