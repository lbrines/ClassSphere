"""
Security Middleware

CRITICAL OBJECTIVES:
- Add security headers to all responses
- Configure CORS properly
- Implement request validation
- Add security logging

DEPENDENCIES:
- fastapi
- fastapi.middleware.cors
- logging
"""

import logging
from typing import Callable, Optional
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

from src.app.core.config import get_settings

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """
    Security middleware for adding security headers and CORS configuration
    """
    
    def __init__(self, app: FastAPI = None):
        """
        Initialize security middleware
        
        Args:
            app: FastAPI application instance
        """
        self.app = app
        self.settings = get_settings()
        
        if app:
            self._setup_middleware(app)
    
    def _setup_middleware(self, app: FastAPI):
        """
        Setup all security middleware
        
        Args:
            app: FastAPI application instance
        """
        # CORS Middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=[
                "Accept",
                "Accept-Language",
                "Content-Language",
                "Content-Type",
                "Authorization",
                "X-Requested-With",
                "X-CSRF-Token",
                "X-API-Key"
            ],
            expose_headers=["X-Rate-Limit-Remaining", "X-Rate-Limit-Reset"]
        )
        
        # Trusted Host Middleware
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=self.settings.allowed_hosts
        )
        
        # Security Headers Middleware
        @app.middleware("http")
        async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
            """
            Add security headers to all responses
            """
            start_time = time.time()
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
            
            # Add HSTS header for HTTPS
            if request.url.scheme == "https":
                response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            
            # Add CSP header
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none';"
            )
            
            # Add request timing
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            # Log security events
            await self._log_security_event(request, response, process_time)
            
            return response
        
        # Request validation middleware
        @app.middleware("http")
        async def request_validation_middleware(request: Request, call_next: Callable) -> Response:
            """
            Validate incoming requests for security
            """
            # Check for suspicious patterns
            if await self._is_suspicious_request(request):
                logger.warning(f"Suspicious request detected: {request.client.host} - {request.url}")
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Request blocked for security reasons"}
                )
            
            # Check request size
            if request.headers.get("content-length"):
                content_length = int(request.headers.get("content-length", 0))
                if content_length > 10 * 1024 * 1024:  # 10MB limit
                    logger.warning(f"Large request detected: {content_length} bytes from {request.client.host}")
                    return JSONResponse(
                        status_code=413,
                        content={"detail": "Request too large"}
                    )
            
            return await call_next(request)
    
    async def _is_suspicious_request(self, request: Request) -> bool:
        """
        Check if request appears suspicious
        
        Args:
            request: FastAPI request object
            
        Returns:
            True if request is suspicious
        """
        # Check for SQL injection patterns
        suspicious_patterns = [
            "union select",
            "drop table",
            "delete from",
            "insert into",
            "update set",
            "script>",
            "<script",
            "javascript:",
            "onload=",
            "onerror="
        ]
        
        # Check URL path
        url_str = str(request.url).lower()
        for pattern in suspicious_patterns:
            if pattern in url_str:
                return True
        
        # Check query parameters
        for param_name, param_value in request.query_params.items():
            param_str = str(param_value).lower()
            for pattern in suspicious_patterns:
                if pattern in param_str:
                    return True
        
        # Check for excessive path traversal
        if ".." in str(request.url.path):
            return True
        
        return False
    
    async def _log_security_event(self, request: Request, response: Response, process_time: float):
        """
        Log security-related events
        
        Args:
            request: FastAPI request object
            response: FastAPI response object
            process_time: Request processing time
        """
        # Log failed authentication attempts
        if response.status_code == 401:
            logger.warning(f"Authentication failed: {request.client.host} - {request.url}")
        
        # Log authorization failures
        if response.status_code == 403:
            logger.warning(f"Authorization failed: {request.client.host} - {request.url}")
        
        # Log rate limiting
        if response.status_code == 429:
            logger.warning(f"Rate limit exceeded: {request.client.host} - {request.url}")
        
        # Log suspicious activity
        if response.status_code == 400:
            logger.warning(f"Bad request: {request.client.host} - {request.url}")
        
        # Log slow requests
        if process_time > 5.0:  # 5 seconds
            logger.warning(f"Slow request: {process_time:.2f}s - {request.client.host} - {request.url}")

def setup_security_middleware(app: FastAPI) -> None:
    """
    Setup security middleware for FastAPI app
    
    Args:
        app: FastAPI application instance
    """
    security_middleware = SecurityMiddleware(app)
    logger.info("Security middleware configured successfully")

# Security utility functions
def validate_origin(origin: str) -> bool:
    """
    Validate request origin
    
    Args:
        origin: Request origin
        
    Returns:
        True if origin is allowed
    """
    settings = get_settings()
    return origin in settings.cors_origins

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent XSS
    
    Args:
        input_str: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not input_str:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', 'script', 'javascript']
    
    sanitized = input_str
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def get_client_ip(request: Request) -> str:
    """
    Get client IP address from request
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client IP address
    """
    # Check for forwarded headers
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct client IP
    return request.client.host if request.client else "unknown"