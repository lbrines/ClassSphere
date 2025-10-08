# 🐛 ClassSphere Dev Containers - Troubleshooting Guide

**Last Updated**: 2025-10-07 | **Version**: 1.0

---

## Table of Contents

1. [Container Startup Issues](#container-startup-issues)
2. [Port Conflicts](#port-conflicts)
3. [Build Failures](#build-failures)
4. [Service Health Problems](#service-health-problems)
5. [Performance Issues](#performance-issues)
6. [VS Code Integration](#vs-code-integration)
7. [Network & Connectivity](#network--connectivity)
8. [Volume & Storage](#volume--storage)

---

## Container Startup Issues

### ❌ Problem: Container exits immediately

**Symptoms**:
```
Error: dependency failed to start: container classsphere-backend exited (1)
```

**Solutions**:

1. **Check logs for the specific service**:
   ```bash
   docker logs classsphere-backend
   docker logs classsphere-frontend
   ```

2. **Common causes and fixes**:

   **Missing environment variables**:
   ```bash
   # Check if all required env vars are set
   docker exec classsphere-backend env | grep GOOGLE
   
   # Should show:
   # GOOGLE_CLIENT_ID=...
   # GOOGLE_CLIENT_SECRET=...
   # GOOGLE_REDIRECT_URL=...
   ```

   **Go module issues**:
   ```bash
   # Clear and re-download modules
   docker exec classsphere-backend go clean -modcache
   docker exec classsphere-backend go mod download
   ```

   **Frontend compilation errors**:
   ```bash
   # Check for TypeScript errors
   docker logs classsphere-frontend | grep "ERROR"
   
   # Reinstall dependencies
   docker exec classsphere-frontend sh -c "rm -rf node_modules && npm ci"
   ```

### ❌ Problem: Workspace container won't start

**Symptoms**:
```
Container classsphere-workspace is unhealthy
```

**Solutions**:

```bash
# Check dependencies
docker-compose -f .devcontainer/docker-compose.yml ps

# Ensure backend and redis are healthy first
docker logs classsphere-workspace

# Rebuild if necessary
docker-compose -f .devcontainer/docker-compose.yml build workspace
docker-compose -f .devcontainer/docker-compose.yml up -d workspace
```

---

## Port Conflicts

### ❌ Problem: Port already in use

**Symptoms**:
```
Error: failed to bind host port for 0.0.0.0:8080:192.168.16.2:8080/tcp: address already in use
Error: failed to bind host port for 0.0.0.0:6379:192.168.16.2:6379/tcp: address already in use
```

**Solutions**:

1. **Find what's using the port**:
   ```bash
   # Check specific port
   sudo lsof -i :8080
   sudo lsof -i :4200
   sudo lsof -i :6379
   
   # Or use netstat
   sudo netstat -tulpn | grep :8080
   ```

2. **Kill the process**:
   ```bash
   # Get PID from lsof output, then:
   sudo kill -9 <PID>
   ```

3. **Common culprits**:

   **System Redis on port 6379**:
   ```bash
   # Stop system Redis
   sudo systemctl stop redis-server
   
   # Disable auto-start
   sudo systemctl disable redis-server
   ```

   **Other Docker containers**:
   ```bash
   # Stop all containers
   docker stop $(docker ps -q)
   
   # Or remove specific ones
   docker stop <container-name>
   docker rm <container-name>
   ```

   **Change port mapping** (if needed):
   Edit `.devcontainer/docker-compose.yml`:
   ```yaml
   ports:
     - "8081:8080"  # Map to different host port
   ```

---

## Build Failures

### ❌ Problem: Docker build fails with "no space left on device"

**Solutions**:

```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a --volumes

# Remove specific items
docker image prune -a
docker volume prune
docker container prune
```

### ❌ Problem: Go build fails with version error

**Symptoms**:
```
go: go.mod requires go >= 1.24.0 (running go 1.23.12)
```

**Solutions**:

1. **Verify Go 1.24.7 is in workspace/tools/**:
   ```bash
   ls -lh workspace/tools/go1.24.7.linux-amd64.tar.gz
   ```

2. **Rebuild backend with correct context**:
   ```bash
   cd /home/lbrines/projects/AI/ClassSphere
   docker-compose -f .devcontainer/docker-compose.yml build --no-cache backend
   ```

### ❌ Problem: npm ci fails in frontend

**Symptoms**:
```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /app/package-lock.json
```

**Solutions**:

```bash
# Ensure package-lock.json exists
ls -la frontend/package-lock.json

# If missing, generate it
cd frontend
npm install  # This creates package-lock.json

# Then rebuild
docker-compose -f .devcontainer/docker-compose.yml build frontend
```

---

## Service Health Problems

### ❌ Problem: Backend health check fails

**Symptoms**:
```
Container classsphere-backend is unhealthy
```

**Diagnosis**:

```bash
# Check health endpoint
curl http://localhost:8080/health

# Check logs
docker logs classsphere-backend --tail 50

# Check if curl is installed in container
docker exec classsphere-backend which curl
```

**Common Issues**:

1. **Server not listening on correct port**:
   ```bash
   # Check SERVER_PORT env var
   docker exec classsphere-backend env | grep SERVER_PORT
   
   # Should be 8080
   ```

2. **Missing dependencies**:
   ```bash
   # Verify curl is installed
   docker exec classsphere-backend curl --version
   
   # If not, add to Dockerfile:
   RUN apt-get update && apt-get install -y curl
   ```

3. **Application crashes on startup**:
   ```bash
   # Check for panic or fatal errors
   docker logs classsphere-backend | grep -E "(panic|fatal|error)"
   ```

### ❌ Problem: Frontend not responding

**Symptoms**:
- Port 4200 connection refused
- Health check fails

**Solutions**:

```bash
# Check if Angular compiled successfully
docker logs classsphere-frontend | grep "Application bundle generation complete"

# Check if dev server is listening
docker exec classsphere-frontend netstat -tlnp | grep 4200

# If compilation fails, check for errors
docker logs classsphere-frontend | grep "ERROR"

# Restart frontend
docker-compose -f .devcontainer/docker-compose.yml restart frontend
```

### ❌ Problem: Redis connection refused

**Symptoms**:
```
dial tcp 127.0.0.1:6379: connect: connection refused
```

**Solutions**:

```bash
# Test Redis directly
docker exec classsphere-redis redis-cli ping

# Should return: PONG

# Check Redis logs
docker logs classsphere-redis

# Verify backend can reach Redis
docker exec classsphere-backend redis-cli -h redis ping
```

---

## Performance Issues

### ⚠️ Problem: Slow container startup

**Solutions**:

1. **Enable BuildKit** (faster builds):
   ```bash
   export DOCKER_BUILDKIT=1
   export COMPOSE_DOCKER_CLI_BUILD=1
   ```

2. **Increase Docker Desktop resources**:
   - Docker Desktop → Settings → Resources
   - CPUs: 4+ cores recommended
   - Memory: 8GB minimum, 12GB recommended
   - Swap: 2GB+

3. **Use cached volumes** (already configured):
   - `go-modules`: Caches Go dependencies
   - `node-modules-cache`: Caches npm packages

### ⚠️ Problem: Hot reload is slow (> 2s)

**Backend (Go)**:

```bash
# Check if Air is configured
docker exec classsphere-backend which air

# Verify .air.toml exists
docker exec classsphere-backend ls -la /app/.air.toml

# Check Air logs
docker logs classsphere-backend | grep -A 10 "watching"
```

**Frontend (Angular)**:

```bash
# Check if HMR is enabled
docker logs classsphere-frontend | grep "HMR"

# Should see: "Component HMR has been enabled"

# If not enabled, check angular.json:
docker exec classsphere-frontend cat angular.json | grep hmr
```

### ⚠️ Problem: High memory usage

**Diagnosis**:

```bash
# Check memory usage per container
docker stats --no-stream

# Check host memory
free -h

# Check Docker Desktop memory limit
docker info | grep -i memory
```

**Solutions**:

1. **Set resource limits** (already configured in docker-compose.yml):
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 2G
   ```

2. **Restart containers periodically**:
   ```bash
   docker-compose -f .devcontainer/docker-compose.yml restart
   ```

---

## VS Code Integration

### ❌ Problem: Dev Container won't open

**Symptoms**:
- "Failed to connect" error
- Container starts but VS Code can't attach

**Solutions**:

1. **Check Dev Containers extension**:
   ```
   Extensions → Dev Containers → Version 0.380+
   ```

2. **Rebuild container**:
   - `F1` → "Dev Containers: Rebuild Container"

3. **Check logs**:
   - `F1` → "Dev Containers: Show Container Log"

4. **Reset extension**:
   ```bash
   # On host machine
   rm -rf ~/.vscode/extensions/ms-vscode-remote.remote-containers-*
   code --install-extension ms-vscode-remote.remote-containers
   ```

### ❌ Problem: Extensions not installing

**Solutions**:

```bash
# Check devcontainer.json syntax
cat .devcontainer/devcontainer.json | jq

# Manually install extensions
code --install-extension golang.go
code --install-extension angular.ng-template

# Or rebuild container
F1 → "Dev Containers: Rebuild Container Without Cache"
```

### ❌ Problem: Terminal not connecting to workspace

**Symptoms**:
- Terminal opens but shows host shell, not container

**Solutions**:

1. **Reopen in container**:
   - `F1` → "Dev Containers: Reopen in Container"

2. **Check remoteUser in devcontainer.json**:
   ```json
   "remoteUser": "vscode"
   ```

3. **Check workspace mount**:
   ```bash
   docker exec classsphere-workspace pwd
   # Should return: /workspace
   ```

---

## Network & Connectivity

### ❌ Problem: Services can't communicate

**Symptoms**:
- Backend can't connect to Redis
- Frontend can't reach backend API

**Solutions**:

1. **Verify all services are on same network**:
   ```bash
   docker network inspect devcontainer_classsphere-network
   
   # Should show all 4 containers
   ```

2. **Test connectivity between services**:
   ```bash
   # From backend to Redis
   docker exec classsphere-backend ping -c 3 redis
   
   # From workspace to backend
   docker exec classsphere-workspace curl http://backend:8080/health
   ```

3. **Check docker-compose network configuration**:
   ```yaml
   networks:
     classsphere-network:
       driver: bridge
   ```

### ❌ Problem: Can't access services from host

**Solutions**:

```bash
# Check port mappings
docker-compose -f .devcontainer/docker-compose.yml ps

# Should show:
# 0.0.0.0:8080->8080/tcp
# 0.0.0.0:4200->4200/tcp
# 0.0.0.0:6379->6379/tcp

# Test from host
curl http://localhost:8080/health
curl http://localhost:4200
redis-cli -h localhost ping
```

---

## Volume & Storage

### ❌ Problem: Changes not persisting

**Symptoms**:
- Go modules re-download every time
- npm install runs on every restart

**Solutions**:

1. **Verify volumes exist**:
   ```bash
   docker volume ls | grep devcontainer
   
   # Should show:
   # devcontainer_go-modules
   # devcontainer_node-modules-cache
   ```

2. **Check volume mounts**:
   ```bash
   docker inspect classsphere-backend | grep -A 10 Mounts
   docker inspect classsphere-frontend | grep -A 10 Mounts
   ```

3. **Recreate volumes if corrupted**:
   ```bash
   docker-compose -f .devcontainer/docker-compose.yml down -v
   docker volume rm devcontainer_go-modules devcontainer_node-modules-cache
   docker-compose -f .devcontainer/docker-compose.yml up -d
   ```

### ❌ Problem: Permission denied errors

**Symptoms**:
```
EACCES: permission denied, open '/app/file'
```

**Solutions**:

```bash
# Check file ownership in container
docker exec classsphere-frontend ls -la /app

# Fix permissions
docker exec --user root classsphere-frontend chown -R node:node /app

# Or for backend
docker exec --user root classsphere-backend chown -R root:root /app
```

---

## Emergency Recovery

### 🚨 Nuclear Option: Complete Reset

If nothing else works:

```bash
# 1. Stop everything
docker-compose -f .devcontainer/docker-compose.yml down -v

# 2. Remove all project containers
docker ps -a | grep classsphere | awk '{print $1}' | xargs docker rm -f

# 3. Remove all project images
docker images | grep devcontainer | awk '{print $3}' | xargs docker rmi -f

# 4. Remove volumes
docker volume rm devcontainer_go-modules devcontainer_node-modules-cache

# 5. Clean Docker system
docker system prune -a --volumes

# 6. Rebuild from scratch
docker-compose -f .devcontainer/docker-compose.yml build --no-cache
docker-compose -f .devcontainer/docker-compose.yml up -d

# 7. Wait for services to become healthy
sleep 30
docker-compose -f .devcontainer/docker-compose.yml ps
```

---

## Getting Additional Help

### Diagnostic Script

Run the full diagnostic:

```bash
bash .devcontainer/scripts/diagnose.sh
```

### Collect Logs for Support

```bash
# Collect all logs
docker-compose -f .devcontainer/docker-compose.yml logs > devcontainer-logs.txt

# Include system info
docker info >> devcontainer-logs.txt
docker version >> devcontainer-logs.txt
docker-compose version >> devcontainer-logs.txt
```

### Useful Commands

```bash
# Show all containers (including stopped)
docker ps -a

# Show disk usage
docker system df -v

# Show container resource usage
docker stats

# Inspect specific container
docker inspect classsphere-backend | jq

# Execute shell in container
docker exec -it classsphere-backend /bin/bash
docker exec -it classsphere-frontend sh
```

---

## Known Issues

### 1. TailwindCSS v4 Compatibility

**Issue**: TailwindCSS v4 breaks Angular 19 build.

**Workaround**: Pin to v3.4.0 in `package.json`:
```json
"tailwindcss": "^3.4.0"
```

### 2. Air Version Compatibility

**Issue**: Latest Air requires Go 1.25+.

**Solution**: Using Air v1.52.3 (compatible with Go 1.23).

### 3. Go 1.24.7 Not in Docker Hub

**Issue**: Go 1.24 not officially released yet.

**Solution**: Using custom build from `workspace/tools/go1.24.7.linux-amd64.tar.gz`.

---

## Prevention Tips

### Before Starting Work

```bash
# 1. Ensure Docker is running
docker info

# 2. Check available resources
docker system df

# 3. Verify services are healthy
docker-compose -f .devcontainer/docker-compose.yml ps

# 4. Pull latest changes
git pull origin main

# 5. Rebuild if needed
docker-compose -f .devcontainer/docker-compose.yml build
```

### Best Practices

1. ✅ **Commit often** - In case you need to rollback
2. ✅ **Check logs regularly** - `docker-compose logs -f`
3. ✅ **Monitor resources** - `docker stats`
4. ✅ **Update regularly** - Keep Docker Desktop updated
5. ✅ **Clean periodically** - `docker system prune`

---

**Last Updated**: 2025-10-07 | **Version**: 1.0
**Contributions**: Submit issues or improvements to the team

