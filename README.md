# Real-Time AI Voice Assistant

A real-time, multilingual AI voice assistant that provides speech-to-speech conversation capabilities using local models.

## Features

- 🎤 **Continuous Listening**: No push-to-talk required
- 🗣️ **Real-time Response**: < 2-3 seconds latency
- 🌍 **Multilingual Support**: Primarily Hindi and English
- 🏠 **Local Processing**: All models run locally
- 🌐 **Web Interface**: Browser-based with live audio

## Architecture

```
[Browser] <--WebSocket--> [Node.js Orchestrator] <--HTTP--> [Python Services]
                                |
                                |---> STT (Whisper)
                                |---> LLM (DialoGPT)
                                |---> TTS (Coqui TTS)
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- CUDA-capable GPU (recommended)
- 8GB+ RAM

### Installation

1. **Clone and navigate to project**:
```bash
cd ai_voice_assistant
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**:
```bash
npm install
```

### Running the Application

#### Option 1: Automatic Startup (Recommended)

**Windows:**
```bash
start_services.bat
```

**Linux/Mac:**
```bash
python start_services.py
```

#### Option 2: Manual Startup

1. **Start Python services** (in separate terminals):
```bash
# Terminal 1 - STT Service
python stt/stt_service.py

# Terminal 2 - LLM Service  
python llm/llm_service.py

# Terminal 3 - TTS Service
python tts/tts_service.py
```

2. **Start Node.js Orchestrator**:
```bash
# Terminal 4 - Orchestrator
npm start
```

3. **Open browser**: Navigate to `http://localhost:3000`

## Usage

1. Click **Start** to begin conversation
2. Speak naturally - the system detects pauses automatically
3. Listen to AI responses through your speakers
4. Click **Stop** to end the session

## Configuration

Edit `.env` file to customize:

```env
STT_HOST=localhost
STT_PORT=5001
LLM_HOST=localhost
LLM_PORT=5002
TTS_HOST=localhost
TTS_PORT=5003
ORCH_PORT=3000
```

## Performance Optimization

### For Better Latency:
- Use GPU acceleration (CUDA)
- Reduce audio chunk sizes
- Use faster models (trade-off with quality)

### For Better Quality:
- Use larger Whisper models (`large` instead of `medium`)
- Use more sophisticated LLM models
- Adjust TTS voice settings

## Deployment on RunPod

1. **Create RunPod instance** with:
   - GPU: RTX A6000 48GB+ recommended
   - Template: PyTorch 2.0+
   - Ports: 3000, 5001, 5002, 5003

2. **Upload project files**

3. **Install dependencies**:
```bash
pip install -r requirements.txt
npm install
```

4. **Update `.env`** with RunPod IP:
```env
STT_HOST=0.0.0.0
LLM_HOST=0.0.0.0
TTS_HOST=0.0.0.0
```

5. **Start services**:
```bash
python start_services.py
```

6. **Access via browser**: `http://[runpod-ip]:3000`

## Troubleshooting

### Common Issues:

**Audio not working:**
- Check browser microphone permissions
- Ensure HTTPS for production (required for microphone access)

**High latency:**
- Verify GPU acceleration is working
- Check network connectivity between services
- Reduce model sizes

**Services not starting:**
- Check port availability
- Verify Python/Node.js versions
- Install missing dependencies

### Debug Mode:

Enable verbose logging by setting environment variable:
```bash
export DEBUG=1
```

## Model Customization

### STT (Speech-to-Text):
- Current: Whisper Medium
- Alternatives: `tiny`, `base`, `small`, `large`
- Languages: Auto-detect or specify in `stt_service.py`

### LLM (Language Model):
- Current: DialoGPT Medium
- Alternatives: GPT-2, LLaMA, custom fine-tuned models
- Modify in `llm_service.py`

### TTS (Text-to-Speech):
- Current: Coqui TTS
- Alternatives: Festival, eSpeak, cloud APIs
- Voice customization in `tts_service.py`

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check troubleshooting section
- Review logs in service terminals
- Open GitHub issue with details