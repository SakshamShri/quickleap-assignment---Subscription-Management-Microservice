from typing import Any, Optional
import json
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

class Cache:
    def __init__(self, default_timeout: int = 300):  # 5 minutes default
        self.default_timeout = default_timeout

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """Set value in cache"""
        timeout = timeout or self.default_timeout
        redis_client.setex(
            key,
            timeout,
            json.dumps(value)
        )

    def delete(self, key: str) -> None:
        """Delete value from cache"""
        redis_client.delete(key)

    def clear_pattern(self, pattern: str) -> None:
        """Clear all keys matching pattern"""
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)

cache = Cache()

# Cache decorator
def cached(timeout: Optional[int] = None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # If not in cache, call function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(key, result, timeout)
            return result
        return wrapper
    return decorator 