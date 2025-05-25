#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.subscription import Plan
from app.core.security import get_password_hash
from app.db.base_class import Base

# Database URL with correct password
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/subscription_db"

def create_test_users():
    """Create test users and plans"""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create test user
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if not existing_user:
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=get_password_hash("testpassword"),
                is_active=True
            )
            db.add(test_user)
            print("✅ Created test user: test@example.com / testpassword")
        else:
            print("✅ Test user already exists: test@example.com")
        
        # Create admin user
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not existing_admin:
            admin_user = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("adminpassword"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            print("✅ Created admin user: admin@example.com / adminpassword")
        else:
            print("✅ Admin user already exists: admin@example.com")
        
        # Create test plans
        existing_basic = db.query(Plan).filter(Plan.name == "Basic").first()
        if not existing_basic:
            basic_plan = Plan(
                name="Basic",
                description="Basic subscription plan",
                price=9.99,
                duration_days=30
            )
            db.add(basic_plan)
            print("✅ Created Basic plan")
        else:
            print("✅ Basic plan already exists")
            
        existing_premium = db.query(Plan).filter(Plan.name == "Premium").first()
        if not existing_premium:
            premium_plan = Plan(
                name="Premium",
                description="Premium subscription plan",
                price=19.99,
                duration_days=30
            )
            db.add(premium_plan)
            print("✅ Created Premium plan")
        else:
            print("✅ Premium plan already exists")
        
        db.commit()
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test users: {e}")
        return False

if __name__ == "__main__":
    success = create_test_users()
    sys.exit(0 if success else 1) 