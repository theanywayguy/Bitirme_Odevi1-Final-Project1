FROM python:3.13-slim

WORKDIR /app

# Install minimal dependencies + OpenCV libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install PyTorch CPU + other Python dependencies
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Remove build tools to reduce image size
RUN apt-get purge -y build-essential git && apt-get autoremove -y

# Copy project files
COPY . .

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
