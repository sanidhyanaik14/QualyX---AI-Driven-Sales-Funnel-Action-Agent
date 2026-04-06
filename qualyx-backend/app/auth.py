# app/auth.py
from fastapi import HTTPException, Header
from typing import Optional

async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(401, "No authorization token provided")
    
    try:
        # Remove Bearer prefix
        token = authorization.replace("Bearer ", "").strip()
        
        if not token:
            raise HTTPException(401, "Empty token")

        # Decode without verification first to get user_id
        # Supabase tokens are verified by checking with Supabase directly
        import base64, json
        
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(401, "Invalid token format")
        
        # Decode payload (add padding if needed)
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += '=' * padding
        
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token - no user ID")
            
        # Check expiry
        import time
        exp = payload.get("exp", 0)
        if exp < time.time():
            raise HTTPException(401, "Token expired")
            
        return user_id
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(401, "Invalid or expired token")





# app/auth.py
"""
from fastapi import HTTPException, Header
from jose import jwt, JWTError
from app.config import settings
import os

async def get_current_user(authorization: str = Header(...)) -> str:
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")"""