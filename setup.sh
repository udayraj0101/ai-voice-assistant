#!/bin/bash

# Setup script for RunPod GPU deployment

echo "Setting up AI Voice Assistant..."

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker
fi

# Install NVIDIA Docker runtime
if ! docker info | grep -q nvidia; then
    echo "Installing NVIDIA Docker runtime..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt update
    sudo apt install -y nvidia-docker2
    sudo systemctl restart docker
fi

# Create models directory
mkdir -p models

echo "Setup complete! Download your models to ./models/ directory"
echo "Then run: docker-compose up --build"