from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.subscription import Plan
from app.schemas.subscription import PlanCreate, PlanUpdate

def get(db: Session, id: int) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.id == id).first()

def get_by_name(db: Session, name: str) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.name == name).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Plan]:
    return db.query(Plan).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: PlanCreate) -> Plan:
    db_obj = Plan(
        name=obj_in.name,
        description=obj_in.description,
        price=obj_in.price,
        duration_days=obj_in.duration_days,
        features=obj_in.features
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Plan, obj_in: PlanUpdate
) -> Plan:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Plan:
    obj = db.query(Plan).get(id)
    db.delete(obj)
    db.commit()
    return obj 