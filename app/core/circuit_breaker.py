from enum import Enum
from datetime import datetime, timedelta
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

class CircuitState(Enum):
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"      # Failing, reject requests
    HALF_OPEN = "HALF_OPEN"  # Testing if service is back

class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        reset_timeout: int = 60,
        half_open_timeout: int = 30
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.half_open_timeout = half_open_timeout
        self._state_key = f"circuit:{name}:state"
        self._failure_count_key = f"circuit:{name}:failures"
        self._last_failure_key = f"circuit:{name}:last_failure"

    def _get_state(self) -> CircuitState:
        state = redis_client.get(self._state_key)
        if not state:
            return CircuitState.CLOSED
        return CircuitState(state.decode())

    def _set_state(self, state: CircuitState) -> None:
        redis_client.set(self._state_key, state.value)

    def _increment_failures(self) -> None:
        redis_client.incr(self._failure_count_key)
        redis_client.set(self._last_failure_key, datetime.utcnow().isoformat())

    def _reset_failures(self) -> None:
        redis_client.delete(self._failure_count_key)
        redis_client.delete(self._last_failure_key)

    def _get_failure_count(self) -> int:
        count = redis_client.get(self._failure_count_key)
        return int(count) if count else 0

    def _should_try_reset(self) -> bool:
        last_failure = redis_client.get(self._last_failure_key)
        if not last_failure:
            return True
        
        last_failure_time = datetime.fromisoformat(last_failure.decode())
        return datetime.utcnow() - last_failure_time > timedelta(seconds=self.reset_timeout)

    async def __call__(self, func, *args, **kwargs):
        current_state = self._get_state()

        if current_state == CircuitState.OPEN:
            if self._should_try_reset():
                self._set_state(CircuitState.HALF_OPEN)
            else:
                raise Exception(f"Circuit breaker {self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            
            if current_state == CircuitState.HALF_OPEN:
                self._set_state(CircuitState.CLOSED)
                self._reset_failures()
            
            return result

        except Exception as e:
            if current_state == CircuitState.HALF_OPEN:
                self._set_state(CircuitState.OPEN)
            else:
                self._increment_failures()
                if self._get_failure_count() >= self.failure_threshold:
                    self._set_state(CircuitState.OPEN)
            
            raise e

# Example usage:
# @circuit_breaker("payment_service")
# async def process_payment(...):
#     ... 