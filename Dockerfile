# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Install PostgreSQL client library for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up entrypoint to load environment variables
COPY .env /app/.env
RUN chmod +x /app/.env

# Expose port 8000
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
