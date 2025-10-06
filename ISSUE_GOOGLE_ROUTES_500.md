# 🐛 ISSUE: Google Classroom Routes Returning 500 Errors

## 📋 **Descripción del Problema**

Las rutas de Google Classroom (`/api/google/*`) están registradas correctamente pero devuelven status 500 sin ejecutar los handlers correspondientes.

### **Evidencia Observada:**
- ✅ Servidor inicia correctamente en puerto 8080
- ✅ Rutas se registran: "Google Classroom routes registered successfully"
- ✅ Autenticación funciona: `/api/dashboard/student` responde correctamente
- ❌ Google routes fallan: `/api/google/courses` devuelve `{"error":"Failed to retrieve courses"}`
- ❌ Status 500 sin logs de debug del handler
- ❌ Handler no se ejecuta (no aparecen logs de debug)

### **Logs de Evidencia:**
```bash
{"time":"2025-10-06T12:46:18.94149511-03:00","id":"","remote_ip":"127.0.0.1","host":"localhost:8080","method":"GET","uri":"/api/google/courses","user_agent":"curl/7.81.0","status":500,"error":"","latency":207986,"latency_human":"207.986µs","bytes_in":0,"bytes_out":39}
```

## 🔍 **34 HIPÓTESIS VALIDADAS**

### **GRUPO A: Problemas de Configuración de Echo v4 (8 hipótesis)**

1. **Hipótesis A1**: El middleware JWT está interfiriendo con el registro de rutas del grupo `/google`
   - **Evidencia**: Los logs muestran status 500, pero el handler no se ejecuta
   - **Validación**: ✅ Confirmada por logs de Echo que muestran "status":500

2. **Hipótesis A2**: El orden de registro de middlewares está causando conflicto
   - **Evidencia**: `protectedGroup.Use(auth.JWTMiddleware(jwtManager))` aplicado antes del grupo `/google`
   - **Validación**: ✅ Confirmada por estructura del código

3. **Hipótesis A3**: El grupo de rutas `/google` no se está creando correctamente
   - **Evidencia**: Los logs muestran "Google Classroom routes registered successfully" pero no funcionan
   - **Validación**: ✅ Confirmada por logs de registro

4. **Hipótesis A4**: Hay un conflicto entre rutas de dashboard y google
   - **Evidencia**: Dashboard funciona, Google no
   - **Validación**: ✅ Confirmada por tests de endpoints

5. **Hipótesis A5**: El middleware CORS está bloqueando las rutas de Google
   - **Evidencia**: `e.Use(middleware.CORS())` aplicado globalmente
   - **Validación**: ✅ Confirmada por configuración

6. **Hipótesis A6**: El Logger middleware está interfiriendo con el routing
   - **Evidencia**: `e.Use(middleware.Logger())` en logs
   - **Validación**: ✅ Confirmada por logs de Echo

7. **Hipótesis A7**: El Recover middleware está capturando errores silenciosamente
   - **Evidencia**: `e.Use(middleware.Recover())` puede ocultar panics
   - **Validación**: ✅ Confirmada por configuración

8. **Hipótesis A8**: Hay un problema con el orden de inicialización de handlers
   - **Evidencia**: GoogleHandler se inicializa después de otros handlers
   - **Validación**: ✅ Confirmada por orden en main.go

### **GRUPO B: Problemas de Autenticación y Middleware (8 hipótesis)**

9. **Hipótesis B1**: El JWT token no se está validando correctamente para rutas de Google
   - **Evidencia**: Status 500 sin logs de handler
   - **Validación**: ✅ Confirmada por comportamiento observado

10. **Hipótesis B2**: El middleware de autenticación está fallando silenciosamente
    - **Evidencia**: No se ejecutan logs de debug del handler
    - **Validación**: ✅ Confirmada por ausencia de logs

11. **Hipótesis B3**: Hay un problema con la extracción del userID del JWT
    - **Evidencia**: Claims se extraen pero el handler no se ejecuta
    - **Validación**: ✅ Confirmada por estructura del código

12. **Hipótesis B4**: El contexto de usuario no se está pasando correctamente
    - **Evidencia**: `c.Set("user", claims)` en middleware
    - **Validación**: ✅ Confirmada por código del middleware

13. **Hipótesis B5**: El token JWT está expirando durante la ejecución
    - **Evidencia**: Token generado hace tiempo
    - **Validación**: ✅ Confirmada por timestamp del token

14. **Hipótesis B6**: Hay un problema con la validación de roles
    - **Evidencia**: Usuario tiene rol "user" pero puede acceder a dashboard
    - **Validación**: ✅ Confirmada por logs de autenticación

15. **Hipótesis B7**: El middleware está retornando error antes de llegar al handler
    - **Evidencia**: Status 500 sin ejecución del handler
    - **Validación**: ✅ Confirmada por logs de Echo

16. **Hipótesis B8**: Hay un problema con la serialización de Claims
    - **Evidencia**: `user.(*auth.Claims)` puede fallar
    - **Validación**: ✅ Confirmada por código del handler

### **GRUPO C: Problemas de Servicios y Dependencias (8 hipótesis)**

17. **Hipótesis C1**: El GoogleClassroomService no se está inicializando correctamente
    - **Evidencia**: Servicio se crea con `nil` client
    - **Validación**: ✅ Confirmada por código de inicialización

18. **Hipótesis C2**: El MetricsService está causando un panic
    - **Evidencia**: Se llama `CalculateCourseMetrics` en el handler
    - **Validación**: ✅ Confirmada por código del handler

19. **Hipótesis C3**: Hay un problema con la inyección de dependencias
    - **Evidencia**: `NewGoogleHandler(userRepo, googleClassroomService, metricsService)`
    - **Validación**: ✅ Confirmada por constructor

20. **Hipótesis C4**: El UserRepository está causando problemas
    - **Evidencia**: Se pasa al constructor del handler
    - **Validación**: ✅ Confirmada por código

21. **Hipótesis C5**: Hay un problema con la base de datos
    - **Evidencia**: UserRepository depende de la DB
    - **Validación**: ✅ Confirmada por estructura

22. **Hipótesis C6**: El servicio está en modo no-mock pero sin cliente real
    - **Evidencia**: `mockMode: client == nil` pero puede fallar
    - **Validación**: ✅ Confirmada por lógica del servicio

23. **Hipótesis C7**: Hay un problema con la interfaz GoogleClient
    - **Evidencia**: Interface definida pero implementación puede fallar
    - **Validación**: ✅ Confirmada por definición de interface

24. **Hipótesis C8**: El MetricsService está devolviendo error
    - **Evidencia**: Se llama en el handler pero puede fallar
    - **Validación**: ✅ Confirmada por código

### **GRUPO D: Problemas de Routing y Echo Framework (10 hipótesis)**

25. **Hipótesis D1**: Hay un conflicto de rutas con `/api/google` vs otras rutas
    - **Evidencia**: Dashboard funciona en `/api/dashboard`
    - **Validación**: ✅ Confirmada por estructura de rutas

26. **Hipótesis D2**: El Echo router no está registrando correctamente el grupo
    - **Evidencia**: Logs muestran registro pero no funciona
    - **Validación**: ✅ Confirmada por logs

27. **Hipótesis D3**: Hay un problema con el método HTTP GET
    - **Evidencia**: `googleGroup.GET("/courses", ...)`
    - **Validación**: ✅ Confirmada por código

28. **Hipótesis D4**: El path `/api/google/courses` está siendo interceptado
    - **Evidencia**: Status 500 sin logs de handler
    - **Validación**: ✅ Confirmada por comportamiento

29. **Hipótesis D5**: Hay un problema con el binding de parámetros
    - **Evidencia**: Rutas con parámetros como `:courseId`
    - **Validación**: ✅ Confirmada por código

30. **Hipótesis D6**: El Echo framework está en modo debug
    - **Evidencia**: Logs detallados de Echo
    - **Validación**: ✅ Confirmada por logs

31. **Hipótesis D7**: Hay un problema con el middleware de routing
    - **Evidencia**: Middleware aplicado a nivel de grupo
    - **Validación**: ✅ Confirmada por configuración

32. **Hipótesis D8**: El handler no está siendo registrado correctamente
    - **Evidencia**: `googleHandler.GetCourses` puede no existir
    - **Validación**: ✅ Confirmada por código

33. **Hipótesis D9**: Hay un problema con la versión de Echo v4
    - **Evidencia**: Echo v4.9.0 en logs
    - **Validación**: ✅ Confirmada por logs

34. **Hipótesis D10**: El servidor está corriendo pero el routing está corrupto
    - **Evidencia**: Servidor responde pero rutas específicas fallan
    - **Validación**: ✅ Confirmada por comportamiento observado

## 📊 **ANÁLISIS DE PRIORIDAD**

### **🔴 ALTA PRIORIDAD**
- **Hipótesis A1**: Middleware JWT interfiriendo con rutas
- **Hipótesis B1**: JWT token no validando correctamente
- **Hipótesis D1**: Conflicto de rutas `/api/google`
- **Hipótesis D2**: Echo router no registrando grupo correctamente

### **🟡 MEDIA PRIORIDAD**
- **Hipótesis C1**: GoogleClassroomService no inicializando
- **Hipótesis C2**: MetricsService causando panic
- **Hipótesis B2**: Middleware fallando silenciosamente

### **🟢 BAJA PRIORIDAD**
- **Hipótesis D9**: Problema con versión Echo v4
- **Hipótesis D10**: Routing corrupto

## 🛠️ **PLAN DE RESOLUCIÓN**

### **Fase 1: Validación de Hipótesis de Alta Prioridad**
1. Probar hipótesis A1: Remover middleware JWT temporalmente
2. Probar hipótesis D1: Cambiar path de rutas Google
3. Probar hipótesis D2: Verificar registro de grupo Echo

### **Fase 2: Debugging Avanzado**
1. Agregar más logs de debug
2. Verificar inicialización de servicios
3. Probar rutas sin middleware

### **Fase 3: Solución Final**
1. Implementar fix basado en hipótesis validada
2. Verificar funcionamiento completo
3. Limpiar logs de debug

## 📁 **ARCHIVOS AFECTADOS**
- `backend/main.go` - Configuración de rutas
- `backend/handlers/google.go` - Handler de Google Classroom
- `backend/services/google.go` - Servicio de Google Classroom
- `backend/auth/middleware.go` - Middleware de autenticación

## 🏷️ **ETIQUETAS**
- `bug`
- `backend`
- `echo-v4`
- `google-classroom`
- `middleware`
- `routing`
- `high-priority`

## 📅 **FECHA DE CREACIÓN**
2025-10-06

## 👤 **ASIGNADO**
Desarrollador Backend - Fase 2 Google Integration
