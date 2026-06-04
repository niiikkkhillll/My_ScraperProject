FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000

# Install curl (useful for diagnostics)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements file first for layer caching
COPY outscraper-python/requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium along with its OS-level system dependencies
RUN playwright install --with-deps chromium

# Copy the application source code
COPY outscraper-python/ .

# Expose the server port
EXPOSE 10000

# Start Uvicorn pointing to app.py inside the container root
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
