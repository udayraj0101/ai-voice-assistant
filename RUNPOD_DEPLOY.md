# RunPod GPU Deployment Guide

## 1. Create RunPod Instance

**Recommended Configuration:**
- **GPU**: RTX A6000 48GB or RTX 4090 24GB
- **Template**: PyTorch 2.0+ with CUDA 12.1
- **Storage**: 50GB+ 
- **Ports**: 3000, 5001, 5002, 5003

## 2. Upload Files

Upload entire project folder to RunPod instance:
```bash
# Zip project locally
zip -r ai_voice_assistant.zip ai_voice_assistant/

# Upload via RunPod file manager or:
scp -r ai_voice_assistant/ root@[runpod-ip]:/workspace/
```

## 3. Setup & Run

**Option A: Automated Setup**
```bash
cd /workspace/ai_voice_assistant
chmod +x runpod_setup.sh
./runpod_setup.sh
python start_services.py
```

**Option B: Docker**
```bash
cd /workspace/ai_voice_assistant
docker build -t voice-assistant .
docker run -p 3000:3000 -p 5001:5001 -p 5002:5002 -p 5003:5003 --gpus all voice-assistant
```

**Option C: Manual**
```bash
cd /workspace/ai_voice_assistant
pip install -r requirements.txt
npm install
python start_services.py
```

## 4. Access Application

Open browser: `http://[runpod-ip]:3000`

## 5. Troubleshooting

**Check services:**
```bash
python health_check.py
```

**View logs:**
```bash
# Check individual service logs in terminal outputs
```

**GPU Usage:**
```bash
nvidia-smi
```

## 6. Performance Tips

- Use RTX A6000 48GB for best performance
- Enable all ports in RunPod network settings
- Use HTTPS proxy for production microphone access