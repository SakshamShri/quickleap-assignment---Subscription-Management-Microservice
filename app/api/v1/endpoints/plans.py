from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.subscription import Plan
from app.schemas.subscription import PlanCreate, PlanUpdate, PlanInDB
from app.crud import plan as crud_plan

router = APIRouter()

@router.get("/", response_model=List[PlanInDB])
def get_plans(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(deps.get_current_user)
) -> List[Plan]:
    """
    Retrieve all available subscription plans.
    """
    plans = crud_plan.get_multi(db, skip=skip, limit=limit)
    return plans

@router.post("/", response_model=PlanInDB, status_code=status.HTTP_201_CREATED)
def create_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_in: PlanCreate,
    current_user: dict = Depends(deps.get_current_admin_user)
) -> Plan:
    """
    Create a new subscription plan (admin only).
    """
    plan = crud_plan.create(db, obj_in=plan_in)
    return plan

@router.put("/{plan_id}", response_model=PlanInDB)
def update_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_id: int,
    plan_in: PlanUpdate,
    current_user: dict = Depends(deps.get_current_admin_user)
) -> Plan:
    """
    Update a subscription plan (admin only).
    """
    plan = crud_plan.get(db, id=plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    plan = crud_plan.update(db, db_obj=plan, obj_in=plan_in)
    return plan

@router.delete("/{plan_id}", response_model=PlanInDB)
def delete_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_id: int,
    current_user: dict = Depends(deps.get_current_admin_user)
) -> Plan:
    """
    Delete a subscription plan (admin only).
    """
    plan = crud_plan.get(db, id=plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    plan = crud_plan.remove(db, id=plan_id)
    return plan 