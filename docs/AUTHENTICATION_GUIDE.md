# Authentication Guide

## Overview
This guide explains how to use the JWT authentication system in ClassSphere.

## Quick Start

### 1. Generate Token
```go
jwtHandler := NewJWTHandler("your-secret-key")
token, err := jwtHandler.GenerateToken("user123", "user@example.com", "student")
```

### 2. Validate Token
```go
claims, err := jwtHandler.ValidateToken(tokenString)
if err != nil {
    // Handle invalid token
}
```

## Security Features
- 24-hour token expiration
- Role-based access control
- NotBefore claim for enhanced security
- Secure secret key handling

## Best Practices
- Always validate tokens on protected routes
- Use HTTPS in production
- Rotate secret keys regularly
- Implement proper error handling

## Troubleshooting
- Check token expiration
- Verify secret key consistency
- Ensure proper role assignment
