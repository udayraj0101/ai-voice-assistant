#!/bin/bash
# RunPod GPU Setup Script

echo "🚀 Setting up AI Voice Assistant on RunPod..."

# Update system
apt-get update -y
apt-get install -y curl wget git

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies  
npm install

# Make scripts executable
chmod +x start_services.py

echo "✅ Setup complete!"
echo "🌐 Run: python start_services.py"
echo "📱 Access: http://[runpod-ip]:3000"