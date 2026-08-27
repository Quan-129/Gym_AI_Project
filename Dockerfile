FROM python:3.11-slim

# Install system dependencies for OpenCV and multimedia
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model weights
COPY . .

# Set default port (Hugging Face Spaces uses 7860, Render uses 10000 or $PORT)
ENV PORT=7860
EXPOSE 7860
EXPOSE 8000

# Start server
CMD ["python", "app.py"]
