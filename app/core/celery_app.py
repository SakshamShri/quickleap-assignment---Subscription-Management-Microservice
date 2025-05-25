from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "subscription_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.subscription"]
)

celery_app.conf.task_routes = {
    "app.tasks.subscription.*": {"queue": "subscription"}
}

celery_app.conf.beat_schedule = {
    "check-expired-subscriptions": {
        "task": "app.tasks.subscription.check_expired_subscriptions",
        "schedule": 3600.0,  # Run every hour
    }
} 