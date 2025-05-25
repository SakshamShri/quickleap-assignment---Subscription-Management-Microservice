#!/usr/bin/env python3

def create_env_file():
    """Create a proper .env file with UTF-8 encoding"""
    env_content = """# Database Configuration
DATABASE_URL=postgresql://postgres:1234@localhost:5432/subscription_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-secure-for-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Application Configuration
DEBUG=true
ENVIRONMENT=development
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Created .env file successfully!")

if __name__ == "__main__":
    create_env_file() 