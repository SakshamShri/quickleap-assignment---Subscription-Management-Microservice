from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute

    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Create a key for this IP
        key = f"rate_limit:{client_ip}"
        
        # Get current count
        current = redis_client.get(key)
        
        if current is None:
            # First request
            redis_client.setex(key, 60, 1)
        elif int(current) >= self.requests_per_minute:
            # Rate limit exceeded
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        else:
            # Increment counter
            redis_client.incr(key)
        
        # Process the request
        response = await call_next(request)
        return response

rate_limiter = RateLimiter() 