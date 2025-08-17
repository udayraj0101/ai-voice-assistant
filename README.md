# Real-Time AI Voice Assistant

A fully local, real-time multilingual speech-to-speech AI assistant running on GPU.

## Architecture

- **Orchestrator**: Node.js WebSocket server coordinating services
- **STT**: Whisper Medium for speech-to-text
- **LLM**: LLaMA 3.1 8B quantized for response generation  
- **TTS**: Coqui XTTS for text-to-speech
- **Frontend**: Push-to-talk web interface

## Quick Start

### 1. Setup (RunPod GPU)
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Download Models
Place your models in `./models/` directory:
- LLaMA model files
- Any custom TTS voices (optional)

### 3. Build and Run
```bash
docker-compose up --build
```

### 4. Access Interface
Open browser: `http://your-runpod-ip:3000`

## Requirements

- GPU: ≥48GB VRAM (RTX A6000/A100)
- Docker with NVIDIA runtime
- Models: ~20GB storage

## Usage

1. Hold "Hold to Talk" button
2. Speak your message
3. Release button
4. Wait for AI response (~2-3 seconds)

## Configuration

Edit `docker-compose.yml` to:
- Change model paths
- Adjust GPU allocation
- Modify service ports

## Troubleshooting

- Check GPU access: `nvidia-smi`
- View logs: `docker-compose logs [service]`
- Restart services: `docker-compose restart`