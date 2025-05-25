# Subscription Management Microservice

A robust microservice for managing user subscriptions in a SaaS platform, built with FastAPI and PostgreSQL.

## Features

- User subscription management (create, read, update, cancel)
- Subscription plan management
- JWT-based authentication
- Automatic subscription expiration handling
- RESTful API design
- Clean Architecture implementation
- Scalable and fault-tolerant design

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT
- **Message Queue**: Redis + Celery (for async tasks)
- **Containerization**: Docker

## Prerequisites

- Python 3.9+
- PostgreSQL
- Redis (for async tasks)
- Docker (optional)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
5. Initialize the database:
   ```bash
   alembic upgrade head
   ```
6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /auth/token` - Get JWT token
- `POST /auth/refresh` - Refresh JWT token

### Subscription Management
- `POST /subscriptions` - Create a new subscription
- `GET /subscriptions/{userId}` - Get user's subscription
- `PUT /subscriptions/{userId}` - Update subscription
- `DELETE /subscriptions/{userId}` - Cancel subscription

### Plan Management
- `GET /plans` - Get all available plans
- `POST /plans` - Create a new plan (admin only)
- `PUT /plans/{planId}` - Update a plan (admin only)
- `DELETE /plans/{planId}` - Delete a plan (admin only)

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Docker Support

Build and run with Docker:
```bash
docker-compose up --build
```

## Environment Variables

Required environment variables (see .env.example):
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration
- `REDIS_URL`: Redis connection string

## License

MIT 