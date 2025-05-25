from fastapi import APIRouter
from app.api.v1.endpoints import subscriptions, plans, auth

api_router = APIRouter()
 
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"]) 