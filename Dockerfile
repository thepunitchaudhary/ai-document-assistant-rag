# Use a lightweight, stable Python 3.12 image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and keep logs real-time
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (required for some AI/PDF libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# 🚀 THE FIX: Force CPU-only installation for PyTorch to save ~4GB of downloads
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy the rest of your application code
COPY . .

# Create a non-root user for security best practices
RUN useradd -m appuser
USER appuser

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]