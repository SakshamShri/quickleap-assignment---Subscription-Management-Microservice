from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.subscription import Subscription, SubscriptionStatus
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

def get(db: Session, id: int) -> Optional[Subscription]:
    return db.query(Subscription).filter(Subscription.id == id).first()

def get_active_subscription(db: Session, user_id: int) -> Optional[Subscription]:
    return db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()

def create_subscription(
    db: Session, *, obj_in: SubscriptionCreate
) -> Subscription:
    # Get the plan to calculate end date
    plan = db.query(Subscription.plan).filter(
        Subscription.plan_id == obj_in.plan_id
    ).first()
    
    if not plan:
        raise ValueError("Plan not found")
    
    db_obj = Subscription(
        user_id=obj_in.user_id,
        plan_id=obj_in.plan_id,
        status=SubscriptionStatus.ACTIVE,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=plan.duration_days)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_subscription(
    db: Session, *, db_obj: Subscription, obj_in: SubscriptionUpdate
) -> Subscription:
    update_data = obj_in.dict(exclude_unset=True)
    
    if "plan_id" in update_data:
        # Get the new plan to calculate new end date
        new_plan = db.query(Subscription.plan).filter(
            Subscription.plan_id == update_data["plan_id"]
        ).first()
        
        if not new_plan:
            raise ValueError("New plan not found")
        
        # Update end date based on remaining time
        remaining_days = (db_obj.end_date - datetime.utcnow()).days
        db_obj.end_date = datetime.utcnow() + timedelta(days=new_plan.duration_days)
        db_obj.plan_id = update_data["plan_id"]
    
    if "status" in update_data:
        db_obj.status = update_data["status"]
        if update_data["status"] == SubscriptionStatus.CANCELLED:
            db_obj.cancelled_at = datetime.utcnow()
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def cancel_subscription(
    db: Session, *, db_obj: Subscription
) -> Subscription:
    db_obj.status = SubscriptionStatus.CANCELLED
    db_obj.cancelled_at = datetime.utcnow()
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_expired_subscriptions(db: Session) -> list[Subscription]:
    return db.query(Subscription).filter(
        Subscription.status == SubscriptionStatus.ACTIVE,
        Subscription.end_date < datetime.utcnow()
    ).all()

def expire_subscription(db: Session, subscription: Subscription) -> Subscription:
    subscription.status = SubscriptionStatus.EXPIRED
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription 