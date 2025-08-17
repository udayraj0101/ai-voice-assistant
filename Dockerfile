FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements first for better caching
COPY requirements.txt package.json ./
RUN pip install -r requirements.txt
RUN npm install

# Copy application code
COPY . .

# Expose ports
EXPOSE 3000 5001 5002 5003

# Start services
CMD ["python", "start_services.py"]