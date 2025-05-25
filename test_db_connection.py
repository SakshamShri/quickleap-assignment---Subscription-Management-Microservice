#!/usr/bin/env python3

import psycopg2
import sys

def test_db_connection():
    """Test database connection with correct password"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="subscription_db",
            user="postgres",
            password="1234"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1) 