# Todo API FastAPI

This project implements a Todo API using FastAPI with PostgreSQL, SQLAlchemy for ORM, Alembic for migrations, and JWT for authentication.

## Table of Contents

- [Development](#development)
	- [Configuration](#configuration)
    - [Setup](#setup)
    - [Testing](#testing)
    - [Linting](#linting)
    - [Type Checking](#type-checking)
    - [URL](#url)
- [Deployment](#deployment)
	- [Build Production Image](#build-production-image)
    - [Run Docker Container](#run-docker-container)
- [License](#license)


## Development

### Configuration

Copy the `.env.example` file to a new file named `.env`, and then set the environment configuration in the `.env` file.
```bash
cp .env.example .env
```

### Setup
1. Using Docker Compose to initialize the project:
```bash
docker compose up -d
```

2. Start a terminal session in the app container
```bash
docker compose exec app bash
```

3. Install dependencies for development
```bash
poetry install
```

4. Run migrations
```bash
alembic upgrade head
```

5. Start the server for development
```bash
poetry run dev
```

### Testing
Run the test suite using:
```bash
pytest -v
```

### Linting
Check code quality with:
```bash
flake8 .
```

### Type Checking
Perform type checking with:
```bash
mypy .
```

### URL
- **Swagger:** [http://localhost:8000/swagger](http://localhost:8000/swagger)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Deployment

### Build Production Image
```bash
docker build -t todo-api-fastapi:1.0.0 .
```

### Run Docker Container
```bash
docker run --name todo-api-fastapi -p 8000:8000 --env-file .env -d todo-api-fastapi:1.0.0
```

## License

Distributed under the MIT License. See [LICENSE](../LICENSE) for more information.