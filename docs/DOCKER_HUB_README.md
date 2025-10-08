# ClassSphere - Educational Dashboard Platform

[![Docker Pulls Backend](https://img.shields.io/docker/pulls/lbrines/classsphere-backend)](https://hub.docker.com/r/lbrines/classsphere-backend)
[![Docker Pulls Frontend](https://img.shields.io/docker/pulls/lbrines/classsphere-frontend)](https://hub.docker.com/r/lbrines/classsphere-frontend)
[![Docker Image Size](https://img.shields.io/docker/image-size/lbrines/classsphere-backend/latest)](https://hub.docker.com/r/lbrines/classsphere-backend)

Educational platform with Google Classroom integration providing role-based dashboards for admins, coordinators, teachers, and students.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Download docker-compose.yml
curl -O https://raw.githubusercontent.com/username/ClassSphere/main/docker-compose.production.yml

# Start all services
docker-compose -f docker-compose.production.yml up -d

# Access application
# Frontend: http://localhost
# Backend API: http://localhost:8080/api/v1
```

### Individual Containers

**Backend**:
```bash
docker run -d \
  -p 8080:8080 \
  -e JWT_SECRET="your-secret-key-min-32-chars" \
  -e REDIS_ADDR="redis:6379" \
  -e CLASSROOM_MODE="mock" \
  --name classsphere-backend \
  lbrines/classsphere-backend:latest
```

**Frontend**:
```bash
docker run -d \
  -p 80:80 \
  --name classsphere-frontend \
  lbrines/classsphere-frontend:latest
```

**Redis** (Cache):
```bash
docker run -d \
  -p 6379:6379 \
  --name classsphere-redis \
  redis:7.2.3-alpine
```

## 📦 Available Images

### Backend (Go 1.24 + Echo v4)

**Image**: `lbrines/classsphere-backend`

**Tags**:
- `latest` - Latest stable release
- `1.0.0` - Specific version
- `production` - Production-ready build
- `sha-abc123` - Git commit builds

**Architecture**: linux/amd64

### Frontend (Angular 19 + Nginx)

**Image**: `lbrines/classsphere-frontend`

**Tags**:
- `latest` - Latest stable release
- `1.0.0` - Specific version
- `production` - Production-ready build
- `sha-abc123` - Git commit builds

**Architecture**: linux/amd64

## ⚙️ Configuration

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET` | ✅ Yes | - | JWT signing key (min 32 chars) |
| `GOOGLE_CLIENT_ID` | ✅ Yes | - | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | ✅ Yes | - | Google OAuth secret |
| `GOOGLE_REDIRECT_URL` | ✅ Yes | - | OAuth redirect URL |
| `SERVER_PORT` | No | `8080` | Server port |
| `REDIS_ADDR` | No | `localhost:6379` | Redis connection |
| `CLASSROOM_MODE` | No | `mock` | Mode: `mock` or `google` |
| `JWT_EXPIRY_MINUTES` | No | `60` | Token expiry time |
| `JWT_ISSUER` | No | `classsphere` | JWT issuer |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_URL` | No | `http://backend:8080/api/v1` | Backend API URL |

## 🐳 Docker Compose Example

**docker-compose.production.yml**:

```yaml
version: '3.8'

services:
  backend:
    image: lbrines/classsphere-backend:latest
    container_name: classsphere-backend
    ports:
      - "8080:8080"
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - GOOGLE_REDIRECT_URL=${GOOGLE_REDIRECT_URL}
      - REDIS_ADDR=redis:6379
      - CLASSROOM_MODE=google
    depends_on:
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    image: lbrines/classsphere-frontend:latest
    container_name: classsphere-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 3s
      retries: 3

  redis:
    image: redis:7.2.3-alpine
    container_name: classsphere-redis
    ports:
      - "6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

networks:
  default:
    name: classsphere-network
```

**.env file**:

```bash
JWT_SECRET=your-production-secret-key-with-at-least-32-characters
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-YourSecretHere
GOOGLE_REDIRECT_URL=https://yourdomain.com/auth/callback
```

## 📋 Exposed Ports

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Frontend | 80 | HTTP | Web interface |
| Backend | 8080 | HTTP | REST API |
| Redis | 6379 | TCP | Cache |

## 🔍 Health Checks

**Backend**:
```bash
curl http://localhost:8080/health
# Expected: {"status": "ok"}
```

**Frontend**:
```bash
curl -I http://localhost:80
# Expected: HTTP/1.1 200 OK
```

**Redis**:
```bash
docker exec classsphere-redis redis-cli ping
# Expected: PONG
```

## 🎓 Demo Users

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@classsphere.edu` | `admin123` |
| Coordinator | `coordinator@classsphere.edu` | `coord123` |
| Teacher | `teacher@classsphere.edu` | `teach123` |
| Student | `student@classsphere.edu` | `stud123` |

**Note**: Change these credentials in production!

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files with real credentials
2. **JWT Secret**: Use strong, randomly generated secret (min 32 chars)
3. **HTTPS**: Use reverse proxy (nginx/Traefik) with SSL in production
4. **Firewall**: Restrict Redis port (6379) to internal network only
5. **Updates**: Regularly update images for security patches

## 📊 Monitoring

**View Logs**:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Resource Usage**:
```bash
docker stats classsphere-backend classsphere-frontend classsphere-redis
```

## 🛠️ Troubleshooting

### Backend won't start

**Check logs**:
```bash
docker logs classsphere-backend
```

**Common issues**:
- Missing `JWT_SECRET` environment variable
- Invalid Google OAuth credentials
- Redis connection failed

### Frontend shows API errors

**Verify backend is running**:
```bash
curl http://localhost:8080/health
```

**Check network connectivity**:
```bash
docker exec classsphere-frontend ping backend
```

### Database/Redis connection issues

**Verify Redis is running**:
```bash
docker exec classsphere-redis redis-cli ping
```

**Check network**:
```bash
docker network ls
docker network inspect classsphere-network
```

## 🔄 Updates

**Pull latest images**:
```bash
docker-compose pull
docker-compose up -d
```

**Specific version**:
```bash
# In docker-compose.yml, change:
# image: lbrines/classsphere-backend:latest
# to:
# image: lbrines/classsphere-backend:1.0.0
```

## 📚 Additional Resources

- **GitHub Repository**: https://github.com/username/ClassSphere
- **Documentation**: https://github.com/username/ClassSphere/tree/main/docs
- **API Documentation**: https://github.com/username/ClassSphere/blob/main/API_DOCUMENTATION.md
- **Issue Tracker**: https://github.com/username/ClassSphere/issues

## 🤝 Support

For questions or issues:
- Open an issue on GitHub
- Email: support@classsphere.edu
- Documentation: See repository README

## 📄 License

[License Information]

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-08  
**Maintained by**: ClassSphere Development Team

**Pull Images**:
```bash
docker pull lbrines/classsphere-backend:latest
docker pull lbrines/classsphere-frontend:latest
```

**Total Size**: ~150MB (Backend) + ~50MB (Frontend) + ~32MB (Redis) = ~232MB

