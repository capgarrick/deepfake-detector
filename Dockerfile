FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy application code
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Create uploads directory
RUN mkdir -p /app/backend/uploads

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Working directory for backend
WORKDIR /app/backend

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
