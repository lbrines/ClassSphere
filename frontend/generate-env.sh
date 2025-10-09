#!/bin/sh
# ==============================================================================
# Runtime Environment Configuration Script
# ==============================================================================
#
# This script generates env.js file with runtime configuration for the Angular
# application. It runs automatically when the Docker container starts, before
# Nginx serves the application.
#
# This implements the 12-Factor App methodology (Config via environment variables)
# and allows a single Docker image to work in multiple environments without
# rebuilding:
#
# - Mock Mode:        API_URL=http://localhost:8080/api/v1
# - Test Mode:        API_URL=http://backend:8080/api/v1
# - Development Mode: API_URL=http://localhost:8080/api/v1
# - Production Mode:  API_URL=https://api.classsphere.example/api/v1
#
# TDD Implementation:
# - Tests: frontend/tests/unit/env-generation.spec.sh
# - Integration: frontend/src/app/core/services/environment.service.ts
#
# Security Considerations:
# - Only exposes API_URL (no secrets)
# - Generated at runtime (not build time)
# - File is publicly accessible (by design, contains public config only)
#
# ==============================================================================

set -e

# Configuration
ENV_JS_PATH="${ENV_JS_PATH:-/usr/share/nginx/html/env.js}"
API_URL="${API_URL:-http://localhost:8080/api/v1}"

# Log for debugging
echo "[generate-env.sh] Generating runtime configuration..."
echo "[generate-env.sh] ENV_JS_PATH: $ENV_JS_PATH"
echo "[generate-env.sh] API_URL: $API_URL"

# Generate env.js file
cat > "$ENV_JS_PATH" <<EOF
/**
 * Runtime Environment Configuration
 * 
 * This file is auto-generated at container startup by generate-env.sh
 * DO NOT EDIT MANUALLY - changes will be overwritten
 * 
 * Configuration is injected via Docker environment variables:
 * - API_URL: Backend API endpoint URL
 * 
 * Usage in Angular:
 * window._env.API_URL
 */
(function(window) {
  window._env = window._env || {};
  
  // API Configuration
  window._env.API_URL = '${API_URL}';
  
  // Environment metadata (for debugging)
  window._env.GENERATED_AT = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")';
  
  // Log configuration (only in development)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('[Runtime Config] API_URL:', window._env.API_URL);
    console.log('[Runtime Config] Generated at:', window._env.GENERATED_AT);
  }
})(this);
EOF

# Verify file was created
if [ ! -f "$ENV_JS_PATH" ]; then
  echo "[generate-env.sh] ERROR: Failed to create $ENV_JS_PATH"
  exit 1
fi

# Log success
echo "[generate-env.sh] ✅ Successfully generated env.js with API_URL=${API_URL}"
echo "[generate-env.sh] File location: $ENV_JS_PATH"

# Display file size for verification
FILE_SIZE=$(wc -c < "$ENV_JS_PATH")
echo "[generate-env.sh] File size: $FILE_SIZE bytes"

exit 0

