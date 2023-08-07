FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set APP_ENV environment to Production mode
ENV APP_ENV production

# Set work directory
WORKDIR /app

# Copy project
COPY pyproject.toml poetry.lock /app/
COPY todo_api /app/todo_api/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --only main

# Create a non-root user and switch to that user on production
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "todo_api.main"]