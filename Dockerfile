FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Install lightweight PyTorch CPU-only (~150MB instead of 4GB CUDA)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2. Install web and vision dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy source code and weights
COPY . .

# Environment variables to optimize memory and enforce UTF-8 for Vietnamese characters
ENV PORT=10000
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV YOLO_CONFIG_DIR=/tmp/Ultralytics
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

EXPOSE 10000

CMD ["python", "app.py"]
