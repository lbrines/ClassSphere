#!/bin/bash

# ClassSphere Services Startup Script
# Garantiza que los servicios inicien en puertos 3000 y 8000
# Limpia cache y libera puertos si es necesario

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para limpiar puertos
cleanup_ports() {
    print_status "Limpiando puertos 3000 y 8000..."
    
    # Matar procesos en puerto 3000
    if netstat -tlnp 2>/dev/null | grep ":3000 " > /dev/null 2>&1; then
        print_warning "Matando procesos en puerto 3000..."
        netstat -tlnp 2>/dev/null | grep ":3000 " | awk '{print $7}' | cut -d'/' -f1 | xargs -r kill -9
        sleep 2
    elif lsof -ti:3000 > /dev/null 2>&1; then
        print_warning "Matando procesos en puerto 3000..."
        lsof -ti:3000 | xargs -r kill -9
        sleep 2
    fi
    
    # Matar procesos en puerto 8000
    if netstat -tlnp 2>/dev/null | grep ":8000 " > /dev/null 2>&1; then
        print_warning "Matando procesos en puerto 8000..."
        netstat -tlnp 2>/dev/null | grep ":8000 " | awk '{print $7}' | cut -d'/' -f1 | xargs -r kill -9
        sleep 2
    elif lsof -ti:8000 > /dev/null 2>&1; then
        print_warning "Matando procesos en puerto 8000..."
        lsof -ti:8000 | xargs -r kill -9
        sleep 2
    fi
    
    # Matar procesos específicos por nombre
    print_status "Matando procesos de uvicorn y next..."
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "next dev" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    sleep 3
    print_success "Puertos limpiados"
}

# Función para limpiar cache del frontend
cleanup_frontend_cache() {
    print_status "Limpiando cache del frontend..."
    
    if [ -d "frontend" ]; then
        cd frontend
        
        # Limpiar cache de Next.js
        if [ -d ".next" ]; then
            print_warning "Eliminando .next cache..."
            rm -rf .next
        fi
        
        # Limpiar node_modules si existe
        if [ -d "node_modules" ]; then
            print_warning "Eliminando node_modules..."
            rm -rf node_modules
        fi
        
        # Reinstalar dependencias
        print_status "Reinstalando dependencias del frontend..."
        npm install --silent
        
        cd ..
        print_success "Cache del frontend limpiado"
    else
        print_warning "Directorio frontend no encontrado"
    fi
}

# Función para verificar si un puerto está libre
check_port() {
    local port=$1
    if netstat -tlnp 2>/dev/null | grep ":$port " > /dev/null 2>&1; then
        return 1  # Puerto ocupado
    elif lsof -ti:$port > /dev/null 2>&1; then
        return 1  # Puerto ocupado
    else
        return 0  # Puerto libre
    fi
}

# Función para esperar a que un servicio esté listo
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Esperando a que $service_name esté listo..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            print_success "$service_name está listo!"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name no respondió después de $max_attempts segundos"
    return 1
}

# Función para iniciar backend
start_backend() {
    print_status "Iniciando backend en puerto 8000..."
    
    if [ ! -d "backend" ]; then
        print_error "Directorio backend no encontrado"
        exit 1
    fi
    
    cd backend
    
    # Verificar si el puerto está libre
    if ! check_port 8000; then
        print_error "Puerto 8000 está ocupado. Limpiando..."
        cleanup_ports
        if ! check_port 8000; then
            print_error "No se pudo liberar el puerto 8000"
            exit 1
        fi
    fi
    
    # Iniciar backend en background
    print_status "Iniciando uvicorn..."
    nohup python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    cd ..
    
    # Esperar a que el backend esté listo
    if wait_for_service "http://localhost:8000/api/v1/health/" "Backend"; then
        print_success "Backend iniciado exitosamente (PID: $BACKEND_PID)"
        return 0
    else
        print_error "Backend falló al iniciar"
        return 1
    fi
}

# Función para iniciar frontend
start_frontend() {
    print_status "Iniciando frontend en puerto 3000..."
    
    if [ ! -d "frontend" ]; then
        print_error "Directorio frontend no encontrado"
        exit 1
    fi
    
    cd frontend
    
    # Verificar si el puerto está libre
    if ! check_port 3000; then
        print_error "Puerto 3000 está ocupado. Limpiando..."
        cleanup_ports
        if ! check_port 3000; then
            print_error "No se pudo liberar el puerto 3000"
            exit 1
        fi
    fi
    
    # Iniciar frontend en background
    print_status "Iniciando Next.js..."
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    cd ..
    
    # Esperar a que el frontend esté listo
    if wait_for_service "http://localhost:3000/" "Frontend"; then
        print_success "Frontend iniciado exitosamente (PID: $FRONTEND_PID)"
        return 0
    else
        print_error "Frontend falló al iniciar"
        return 1
    fi
}

# Función para mostrar estado de los servicios
show_status() {
    print_status "Estado de los servicios:"
    echo ""
    
    # Backend
    if check_port 8000; then
        print_error "Backend: NO CORRIENDO (puerto 8000 libre)"
    else
        print_success "Backend: CORRIENDO (puerto 8000 ocupado)"
        if curl -s "http://localhost:8000/api/v1/health/" > /dev/null 2>&1; then
            print_success "Backend: RESPONDIENDO"
        else
            print_error "Backend: NO RESPONDE"
        fi
    fi
    
    echo ""
    
    # Frontend
    if check_port 3000; then
        print_error "Frontend: NO CORRIENDO (puerto 3000 libre)"
    else
        print_success "Frontend: CORRIENDO (puerto 3000 ocupado)"
        if curl -s "http://localhost:3000/" > /dev/null 2>&1; then
            print_success "Frontend: RESPONDIENDO"
        else
            print_error "Frontend: NO RESPONDE"
        fi
    fi
}

# Función para detener servicios
stop_services() {
    print_status "Deteniendo servicios..."
    cleanup_ports
    print_success "Servicios detenidos"
}

# Función principal
main() {
    echo "=========================================="
    echo "  ClassSphere Services Startup Script"
    echo "=========================================="
    echo ""
    
    # Verificar argumentos
    case "${1:-start}" in
        "start")
            print_status "Iniciando servicios..."
            cleanup_ports
            cleanup_frontend_cache
            
            if start_backend && start_frontend; then
                echo ""
                print_success "¡Todos los servicios iniciados exitosamente!"
                echo ""
                show_status
                echo ""
                print_status "Logs disponibles en:"
                print_status "  Backend: backend.log"
                print_status "  Frontend: frontend.log"
                echo ""
                print_status "URLs:"
                print_status "  Frontend: http://localhost:3000"
                print_status "  Backend: http://localhost:8000"
                print_status "  Health: http://localhost:8000/api/v1/health/"
            else
                print_error "Falló al iniciar los servicios"
                exit 1
            fi
            ;;
        "stop")
            stop_services
            ;;
        "status")
            show_status
            ;;
        "restart")
            stop_services
            sleep 2
            $0 start
            ;;
        "clean")
            cleanup_ports
            cleanup_frontend_cache
            print_success "Limpieza completada"
            ;;
        *)
            echo "Uso: $0 {start|stop|status|restart|clean}"
            echo ""
            echo "Comandos:"
            echo "  start   - Iniciar servicios (por defecto)"
            echo "  stop    - Detener servicios"
            echo "  status  - Mostrar estado de servicios"
            echo "  restart - Reiniciar servicios"
            echo "  clean   - Limpiar cache y puertos"
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
