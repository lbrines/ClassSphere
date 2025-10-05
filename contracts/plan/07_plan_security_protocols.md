---
title: "ClassSphere - Protocolos de Seguridad"
version: "1.0"
type: "security_protocols"
date: "2025-10-05"
---

# Protocolos de Seguridad

## Principio de Cero Confianza

### Verificación Obligatoria
- Todo código generado por IA debe ser revisado
- Comprensión completa del código antes de merge
- Revisión de seguridad en cada PR

## Escaneo Automático

### SAST (Static Application Security Testing)
```bash
# Go security scan
gosec ./...

# Angular security scan
npm audit
```

### SCA (Software Composition Analysis)
```bash
# Check dependencies
go list -m all | nancy sleuth

# Frontend dependencies
npm audit --production
```

### Secrets Detection
```bash
# Detect exposed secrets
trufflehog filesystem . --json

# Pre-commit hook
git secrets --scan
```

### Container Security
```bash
# Trivy scan
trivy image classsphere-backend:latest
trivy image classsphere-frontend:latest
```

## Prompt Engineering de Seguridad

### Prompts Seguros
```
"Genera un formulario de login con:
- Validación de entrada
- Limitación de tasa
- Hash de contraseñas (bcrypt)
- Protección CSRF
- Headers de seguridad"
```

## Pipeline de Seguridad CI/CD

```yaml
security:
  - SAST scan
  - Dependency check
  - Secrets detection
  - Container scan
  - DAST (staging)
```

## Checklist de Seguridad

- [ ] SAST: 0 vulnerabilidades críticas
- [ ] SCA: 0 dependencias vulnerables
- [ ] Secrets: 0 credenciales expuestas
- [ ] Containers: 0 vulnerabilidades críticas
- [ ] Headers: Todos los headers de seguridad
- [ ] HTTPS: Forzado en producción
- [ ] Auth: JWT + OAuth 2.0
- [ ] CORS: Configurado correctamente

---

**Regla**: Escanear todo. Sin excepciones.
