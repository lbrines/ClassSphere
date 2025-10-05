#!/usr/bin/env python3
"""Debug JWT token verification"""

import sys
import os
sys.path.append('/home/lbrines/projects/AI/ClassSphere/backend/src')

from jose import jwt, JWTError
from app.core.config import settings

def debug_token(token_str):
    print("=== JWT Token Debug ===")
    print(f"Token: {token_str[:50]}...")

    try:
        # Decode without verification first (using jwt from jose)
        payload = jwt.decode(token_str, key="", options={"verify_signature": False})
        print(f"Payload (unverified): {payload}")

        # Try to decode with verification
        payload_verified = jwt.decode(
            token_str,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        print(f"Payload (verified): {payload_verified}")
        print("✅ Token verification SUCCESS")

    except JWTError as e:
        print(f"❌ JWT Error: {e}")
    except Exception as e:
        print(f"❌ General Error: {e}")

    print(f"\nSettings:")
    print(f"Secret key: {settings.secret_key[:20]}...")
    print(f"Algorithm: {settings.algorithm}")

if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImVtYWlsIjoiYWRtaW5AY2xhc3NzcGhlcmUuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzU5NzAzNTQ2LCJ0eXBlIjoiYWNjZXNzIn0.CU_BwRaE2aScaQwx96HFxmt4cV64715sIv4muKXtfrs"
    debug_token(token)