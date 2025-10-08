# ClassSphere Dev Containers

**Status**: ✅ Operational | **Version**: 1.0 | **Last Updated**: 2025-10-07

---

## 🚀 Quick Start (< 5 minutes)

### Prerequisites

- [x] Docker Desktop 4.0+ installed and running
- [x] VS Code with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [x] 8GB RAM minimum available
- [x] Ports 8080, 4200, 6379 available

### Launch Dev Environment

1. **Clone and open the project**:
   ```bash
   git clone <repo-url>
   cd ClassSphere
   code .
   ```

2. **Open in Dev Container**:
   - Press `F1` → "Dev Containers: Reopen in Container"
   - Or click notification: "Reopen in Container"

3. **Wait for setup** (~3-5 minutes first time):
   - All services build automatically
   - Dependencies install automatically
   - Post-create script runs

4. **Verify services are ready**:
   ```bash
   # Backend API
   curl http://localhost:8080/health
   
   # Frontend (open browser)
   http://localhost:4200
   
   # Redis
   redis-cli ping
   ```

✅ **Done!** You're ready to develop.

---

## 📦 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code Dev Container                     │
│                  (classsphere-workspace)                     │
├─────────────────────────────────────────────────────────────┤
│  Tools: Go 1.23, Node 20, Angular CLI, redis-cli, git      │
│  Workspace: /workspace (mounted from host)                   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Backend    │      │   Frontend   │      │    Redis     │
│   Go 1.24.7  │◄─────┤  Angular 19  │      │   7.2.3      │
│   Port 8080  │      │   Port 4200  │      │   Port 6379  │
│   (healthy)  │      │  (compiled)  │      │   (healthy)  │
└──────────────┘      └──────────────┘      └──────────────┘
```

### Services

| Service | Port | Status | Description |
|---------|------|--------|-------------|
| **Backend** | 8080 | ✅ Healthy | Go 1.24.7 + Echo API |
| **Frontend** | 4200 | ✅ Running | Angular 19 + TailwindCSS |
| **Redis** | 6379 | ✅ Healthy | Cache layer |
| **Workspace** | - | ✅ Running | Development tools |

---

## 🛠️ Development Workflow

### Backend Development

```bash
# Navigate to backend
cd /workspace/backend

# Run with hot reload (if Air is configured)
air

# Or run directly
go run cmd/api/main.go

# Run tests
go test ./...

# Check coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Frontend Development

```bash
# Navigate to frontend
cd /workspace/frontend

# Dev server (already running)
npm start

# Run tests
npm test

# E2E tests
npx playwright test

# Build for production
npm run build
```

### Database Operations

```bash
# Connect to Redis CLI
redis-cli

# Or via Docker
docker exec -it classsphere-redis redis-cli

# Common commands
redis-cli ping
redis-cli KEYS '*'
redis-cli FLUSHDB
```

---

## 📝 Common Commands

### Docker Compose Management

```bash
# View all services status
docker-compose -f .devcontainer/docker-compose.yml ps

# View logs (all services)
docker-compose -f .devcontainer/docker-compose.yml logs -f

# View logs (specific service)
docker logs classsphere-backend -f
docker logs classsphere-frontend -f

# Restart a service
docker-compose -f .devcontainer/docker-compose.yml restart backend

# Stop all services
docker-compose -f .devcontainer/docker-compose.yml down

# Rebuild a service
docker-compose -f .devcontainer/docker-compose.yml build backend
docker-compose -f .devcontainer/docker-compose.yml up -d backend
```

### Health Checks

```bash
# Check all services
curl http://localhost:8080/health
curl -I http://localhost:4200
docker exec classsphere-redis redis-cli ping

# Or use the verification script
bash .devcontainer/scripts/verify-health.sh
```

---

## 🔧 Configuration

### Environment Variables

Backend environment variables are defined in `.devcontainer/docker-compose.yml`:

```yaml
- APP_ENV=development
- SERVER_PORT=8080
- JWT_SECRET=development-secret-key
- REDIS_ADDR=redis:6379
- GOOGLE_CLIENT_ID=dummy-client-id-for-development
- GOOGLE_CLIENT_SECRET=dummy-client-secret-for-development
- GOOGLE_REDIRECT_URL=http://localhost:4200/auth/callback
```

To use real Google OAuth credentials:
1. Create `.env` file in project root (ignored by git)
2. Override values in docker-compose or devcontainer.json

### VS Code Extensions

Automatically installed extensions:
- `golang.go` - Go language support
- `angular.ng-template` - Angular template support
- `ms-playwright.playwright` - Playwright testing
- `ms-azuretools.vscode-docker` - Docker support
- `eamodio.gitlens` - Git visualization

### Port Forwarding

Ports are automatically forwarded:
- **8080**: Backend API → Opens with notification
- **4200**: Frontend → Opens in browser automatically
- **6379**: Redis → Silent (internal use)

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8080
sudo lsof -i :4200
sudo lsof -i :6379

# Kill the process
sudo kill -9 <PID>

# Or stop system Redis
sudo systemctl stop redis-server
```

### Issue: Container Won't Start

```bash
# View detailed logs
docker logs classsphere-backend
docker logs classsphere-frontend

# Rebuild from scratch
docker-compose -f .devcontainer/docker-compose.yml down
docker-compose -f .devcontainer/docker-compose.yml build --no-cache
docker-compose -f .devcontainer/docker-compose.yml up -d
```

### Issue: Slow Build Times

```bash
# Clear Docker cache
docker system prune -a --volumes

# Remove only unused volumes
docker volume prune

# Check disk space
docker system df
```

### Issue: Module Not Found (Frontend)

```bash
# Reinstall dependencies
docker exec -it classsphere-frontend sh -c "cd /app && rm -rf node_modules && npm ci"

# Or rebuild frontend
docker-compose -f .devcontainer/docker-compose.yml build frontend
docker-compose -f .devcontainer/docker-compose.yml up -d frontend
```

### Issue: Go Module Errors (Backend)

```bash
# Clear Go module cache
docker exec -it classsphere-backend sh -c "go clean -modcache"

# Re-download modules
docker exec -it classsphere-backend sh -c "cd /app && go mod download"
```

---

## 📊 Performance Tips

### 1. **Use Named Volumes** (Already configured)
- `go-modules`: Persistent Go module cache
- `node-modules-cache`: Persistent npm cache

### 2. **Docker Desktop Resources**
Recommended settings in Docker Desktop:
- **CPUs**: 4+ cores
- **Memory**: 8GB minimum (12GB recommended)
- **Disk**: 20GB+ available

### 3. **File Watching Performance**
Add to `.gitignore` if using Linux:
```
**/node_modules
**/.angular
**/dist
**/coverage
```

---

## 🔒 Security Notes

### Development Credentials

⚠️ **DO NOT USE THESE IN PRODUCTION**:
- `JWT_SECRET`: development-secret-key (change in production)
- `GOOGLE_CLIENT_ID`: dummy-client-id-for-development
- Redis: No authentication (add in production)

### Production Checklist

Before deploying to production:
- [ ] Change all secrets and credentials
- [ ] Enable Redis authentication
- [ ] Use real Google OAuth credentials
- [ ] Configure HTTPS/TLS
- [ ] Set up proper CORS policies
- [ ] Enable rate limiting
- [ ] Configure proper logging

---

## 📚 Additional Resources

- **Master Plan**: `workspace/plan/cd/00_devcontainers_master_plan.md`
- **Completion Report**: `.devcontainer/DIA1_COMPLETADO.md`
- **Backend Docs**: `backend/README.md`
- **Frontend Docs**: `frontend/README.md`
- **Testing Strategy**: `workspace/contracts/09_ClassSphere_testing.md`

---

## 🆘 Getting Help

### Quick Diagnostics

```bash
# Run full diagnostic
bash .devcontainer/scripts/diagnose.sh

# Check Docker status
docker info

# Check services
docker-compose -f .devcontainer/docker-compose.yml ps -a
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Backend unhealthy | Check `GOOGLE_*` env vars are set |
| Frontend not compiling | Run `npm ci` inside container |
| Redis connection refused | Restart Redis container |
| VS Code extensions missing | Rebuild container |
| Hot reload not working | Check file permissions |

### Support

For issues specific to this project:
1. Check `TROUBLESHOOTING.md`
2. Review logs: `docker-compose logs -f`
3. Check GitHub issues
4. Contact team lead

---

## 📈 Metrics & Monitoring

### Build Times
- **First build**: ~3-5 minutes (with downloads)
- **Incremental builds**: < 1 minute (with cache)
- **Hot reload**: < 2 seconds

### Resource Usage
| Service | CPU | Memory | Disk |
|---------|-----|--------|------|
| Backend | 0.5-2.0 cores | 512M-2G | 1.65GB |
| Frontend | 0.25-1.5 cores | 256M-1G | 390MB |
| Redis | 0.1-0.5 cores | 50M-256M | 100MB |
| Workspace | Minimal | Minimal | 2.14GB |
| **Total** | ~1-4 cores | ~1-4GB | ~4.3GB |

---

## 🎓 Learning Resources

### Dev Containers
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker Compose](https://docs.docker.com/compose/)

### Technologies
- [Go Documentation](https://go.dev/doc/)
- [Angular Documentation](https://angular.dev)
- [Echo Framework](https://echo.labstack.com/)
- [TailwindCSS](https://tailwindcss.com/)

---

**Version**: 1.0 | **Last Updated**: 2025-10-07 | **Maintained by**: ClassSphere Dev Team

