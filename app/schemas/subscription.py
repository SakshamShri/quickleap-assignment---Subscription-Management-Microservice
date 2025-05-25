from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.subscription import SubscriptionStatus

class PlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    duration_days: int = Field(gt=0)
    features: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    duration_days: Optional[int] = Field(default=None, gt=0)

class PlanInDB(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = None
    status: Optional[SubscriptionStatus] = None

class SubscriptionInDB(SubscriptionBase):
    id: int
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    cancelled_at: Optional[datetime] = None
    plan: PlanInDB

    class Config:
        from_attributes = True

class SubscriptionResponse(SubscriptionInDB):
    pass 