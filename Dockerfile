# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy Python requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend, frontend, models, and other necessary files
COPY backend ./backend
COPY frontend ./frontend
COPY README.md .
COPY test-ball.mp4 .  # optional test file

# Expose port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
