from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.crud import subscription as crud_subscription

@celery_app.task
def check_expired_subscriptions():
    """
    Background task to check and expire subscriptions that have passed their end date.
    """
    db = SessionLocal()
    try:
        expired_subscriptions = crud_subscription.get_expired_subscriptions(db)
        for subscription in expired_subscriptions:
            crud_subscription.expire_subscription(db, subscription)
    finally:
        db.close()

@celery_app.task
def send_subscription_expiry_notification(subscription_id: int):
    """
    Background task to send notification when a subscription is about to expire.
    """
    # TODO: Implement notification sending logic
    pass 