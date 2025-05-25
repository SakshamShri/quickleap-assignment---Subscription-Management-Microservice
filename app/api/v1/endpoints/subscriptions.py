from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.subscription import Subscription, SubscriptionStatus
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse
)
from app.crud import subscription as crud_subscription

router = APIRouter()

@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_in: SubscriptionCreate,
    current_user: dict = Depends(deps.get_current_user)
) -> Subscription:
    """
    Create a new subscription for a user.
    """
    # Check if user already has an active subscription
    existing_sub = crud_subscription.get_active_subscription(db, user_id=subscription_in.user_id)
    if existing_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription"
        )
    
    # Create new subscription
    subscription = crud_subscription.create_subscription(db, obj_in=subscription_in)
    return subscription

@router.get("/{user_id}", response_model=SubscriptionResponse)
def get_subscription(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
) -> Subscription:
    """
    Get a user's current subscription.
    """
    subscription = crud_subscription.get_active_subscription(db, user_id=user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    return subscription

@router.put("/{user_id}", response_model=SubscriptionResponse)
def update_subscription(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    subscription_in: SubscriptionUpdate,
    current_user: dict = Depends(deps.get_current_user)
) -> Subscription:
    """
    Update a user's subscription (upgrade/downgrade plan).
    """
    subscription = crud_subscription.get_active_subscription(db, user_id=user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    subscription = crud_subscription.update_subscription(
        db, db_obj=subscription, obj_in=subscription_in
    )
    return subscription

@router.delete("/{user_id}", response_model=SubscriptionResponse)
def cancel_subscription(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: dict = Depends(deps.get_current_user)
) -> Subscription:
    """
    Cancel a user's subscription.
    """
    subscription = crud_subscription.get_active_subscription(db, user_id=user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    subscription = crud_subscription.cancel_subscription(db, db_obj=subscription)
    return subscription 