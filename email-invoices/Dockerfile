# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.2

# Copy only the files needed for installing dependencies first
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN poetry install --no-interaction --no-ansi

# Create necessary directories
RUN mkdir -p /app/output /app/logs

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "-m", "email_processor.process_invoices"]

# Default command
CMD ["--config", "/app/config/config.yaml"]
