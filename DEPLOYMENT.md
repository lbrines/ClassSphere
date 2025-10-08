# ClassSphere Deployment Guide

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Environments**: Development, Staging, Production

---

## 🎯 Deployment Options

### Option 1: Dev Containers (Development) ✅ RECOMMENDED

**Use Case**: Local development, team onboarding  
**Setup Time**: 3-5 minutes  
**Requirements**: Docker Desktop + VS Code

See [.devcontainer/README.md](.devcontainer/README.md) for complete guide.

---

### Option 2: Docker Compose (Staging/Production)

**Use Case**: Server deployment, staging environment

#### Quick Deploy

```bash
# 1. Clone repository
git clone <repo-url>
cd ClassSphere

# 2. Configure environment
cp backend/.env.example .env
# Edit .env with production values

# 3. Build production images
docker-compose -f docker-compose.prod.yml build

# 4. Start services
docker-compose -f docker-compose.prod.yml up -d

# 5. Verify health
curl http://localhost:8080/health
```

---

### Option 3: Manual Deployment

**Use Case**: Traditional server, custom setup

See [Manual Deployment](#manual-deployment) section below.

---

## 🔧 Environment Variables

### Required (Production)

```bash
# Application
APP_ENV=production
SERVER_PORT=8080

# JWT Authentication (⚠️ CHANGE IN PRODUCTION)
JWT_SECRET="<generate-secure-random-string-min-32-chars>"
JWT_ISSUER="classsphere"
JWT_EXPIRY_MINUTES=60

# Google OAuth 2.0
GOOGLE_CLIENT_ID="<your-client-id>.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-<your-client-secret>"
GOOGLE_REDIRECT_URL="https://yourdomain.com/auth/callback"

# Google Classroom API
CLASSROOM_MODE="google"  # or "mock" for testing
GOOGLE_CREDENTIALS_FILE="/app/config/google-credentials.json"

# Redis Cache
REDIS_ADDR="redis:6379"
REDIS_PASSWORD="<redis-password>"
REDIS_DB=0
```

### Optional

```bash
# Logging
LOG_LEVEL="info"  # debug, info, warn, error

# CORS
CORS_ALLOWED_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=100
```

---

## 🐳 Docker Production Setup

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: .devcontainer/backend/Dockerfile
      target: production
    image: classsphere-backend:${VERSION:-latest}
    container_name: classsphere-backend-prod
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - APP_ENV=production
      - SERVER_PORT=8080
      - JWT_SECRET=${JWT_SECRET}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - GOOGLE_REDIRECT_URL=${GOOGLE_REDIRECT_URL}
      - CLASSROOM_MODE=${CLASSROOM_MODE:-google}
      - REDIS_ADDR=redis:6379
    volumes:
      - ./google-credentials.json:/app/config/google-credentials.json:ro
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    networks:
      - classsphere-network

  frontend:
    build:
      context: frontend
      dockerfile: Dockerfile.prod
      args:
        - API_URL=http://backend:8080/api/v1
    image: classsphere-frontend:${VERSION:-latest}
    container_name: classsphere-frontend-prod
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 3s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    networks:
      - classsphere-network

  redis:
    image: redis:7-alpine
    container_name: classsphere-redis-prod
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    networks:
      - classsphere-network

networks:
  classsphere-network:
    driver: bridge

volumes:
  redis-data:
    driver: local
```

---

## 🔒 Security Checklist

### Before Production Deployment

- [ ] Change `JWT_SECRET` to cryptographically secure random string (32+ chars)
- [ ] Use real Google OAuth credentials (not dummy values)
- [ ] Set `GOOGLE_REDIRECT_URL` to production domain (HTTPS)
- [ ] Enable Redis password authentication
- [ ] Configure CORS for production domains only
- [ ] Use HTTPS/TLS (nginx reverse proxy or cloud load balancer)
- [ ] Set `APP_ENV=production`
- [ ] Review and rotate all secrets
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting

---

## 📦 Google Cloud Setup

### Prerequisites

1. **Google Cloud Project**
   - Create project at [console.cloud.google.com](https://console.cloud.google.com)
   - Enable Google Classroom API
   - Enable Google OAuth 2.0

2. **OAuth 2.0 Credentials**
   - APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs: `https://yourdomain.com/auth/callback`
   - Copy Client ID and Client Secret

3. **Service Account** (for Classroom API)
   - Create Service Account
   - Grant "Classroom Admin" role
   - Download JSON key file
   - Set `GOOGLE_CREDENTIALS_FILE=/path/to/key.json`

---

## 🚀 Manual Deployment

### Backend

```bash
# 1. Build binary
cd backend
CGO_ENABLED=0 GOOS=linux go build -o classsphere-backend cmd/api/main.go

# 2. Create systemd service
sudo tee /etc/systemd/system/classsphere-backend.service << 'EOF'
[Unit]
Description=ClassSphere Backend API
After=network.target redis.service

[Service]
Type=simple
User=classsphere
WorkingDirectory=/opt/classsphere/backend
EnvironmentFile=/opt/classsphere/backend/.env
ExecStart=/opt/classsphere/backend/classsphere-backend
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable classsphere-backend
sudo systemctl start classsphere-backend

# 4. Check status
sudo systemctl status classsphere-backend
```

### Frontend

```bash
# 1. Build for production
cd frontend
npm run build

# 2. Serve with Nginx
sudo tee /etc/nginx/sites-available/classsphere << 'EOF'
server {
    listen 80;
    server_name yourdomain.com;
    
    root /var/www/classsphere/frontend/dist;
    index index.html;
    
    # Angular routing
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/classsphere /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔍 Health Checks

### Verify Deployment

```bash
# Backend health
curl https://yourdomain.com/health
# Expected: {"status":"ok"}

# Frontend
curl -I https://yourdomain.com
# Expected: 200 OK

# Redis (from server)
redis-cli -h localhost -a "$REDIS_PASSWORD" ping
# Expected: PONG
```

---

## 📊 Monitoring

### Recommended Tools

- **Application**: Prometheus + Grafana
- **Logs**: ELK Stack or Loki
- **APM**: New Relic or DataDog
- **Uptime**: UptimeRobot or StatusCake

### Health Endpoints

- `GET /health` - Basic health check
- Future: `GET /metrics` - Prometheus metrics
- Future: `GET /ready` - Readiness probe

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker images
        run: |
          docker build -f .devcontainer/backend/Dockerfile \
            --target production \
            -t classsphere-backend:${{ github.sha }} .
      
      - name: Run tests
        run: |
          docker run --rm classsphere-backend:${{ github.sha }} \
            go test ./... -v
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push classsphere-backend:${{ github.sha }}
      
      - name: Deploy to server
        run: |
          ssh deploy@server "cd /opt/classsphere && docker-compose pull && docker-compose up -d"
```

---

## 🆘 Troubleshooting

### Container won't start

```bash
# Check logs
docker logs classsphere-backend-prod

# Common issues:
# - Missing environment variables
# - Invalid Google credentials
# - Redis not reachable
```

### High memory usage

```bash
# Check resource usage
docker stats

# Adjust limits in docker-compose.prod.yml
deploy:
  resources:
    limits:
      memory: 4G  # Increase if needed
```

### Database connection errors

```bash
# Verify Redis
docker exec classsphere-redis-prod redis-cli ping

# Restart Redis
docker-compose -f docker-compose.prod.yml restart redis
```

---

## 📚 Additional Resources

- **[Dev Containers](.devcontainer/README.md)** - Development environment
- **[Architecture](ARCHITECTURE.md)** - System design
- **[Security](SECURITY.md)** - Security best practices
- **[API Documentation](API_DOCUMENTATION.md)** - API reference

---

**Version**: 1.0  
**Maintainer**: ClassSphere DevOps Team

