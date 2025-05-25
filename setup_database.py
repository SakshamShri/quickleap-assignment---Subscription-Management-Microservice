#!/usr/bin/env python3

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import subprocess
import sys
import os

def create_database():
    """Create the subscription_db database if it doesn't exist"""
    try:
        # Connect to postgres database to create our database
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="1234"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='subscription_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE subscription_db")
            print("✅ Database 'subscription_db' created successfully!")
        else:
            print("✅ Database 'subscription_db' already exists!")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def run_migrations():
    """Run Alembic migrations"""
    try:
        # Run migrations
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print("✅ Database migrations completed successfully!")
            return True
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False

def main():
    print("Setting up database...")
    
    if not create_database():
        sys.exit(1)
    
    if not run_migrations():
        sys.exit(1)
    
    print("✅ Database setup completed successfully!")

if __name__ == "__main__":
    main() 