# Use slim Python base image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies (git, curl, gcc for torch if needed)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# # Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir mlflow[extras]

# Copy application code including my_model/
COPY ./app .

# Expose FastAPI port
EXPOSE 8000

# Set MLflow Tracking URI (points to mlflow container in docker-compose)
ENV MLFLOW_TRACKING_URI=http://mlflow:5000

# Run Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]