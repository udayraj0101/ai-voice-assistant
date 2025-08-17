from fastapi import FastAPI, File, UploadFile
import whisper
import tempfile
import uvicorn
import torch
import os

app = FastAPI()

# Load model with optimizations
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)
model.eval()

# Warm up the model
print("Warming up Whisper model...")
with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
    import numpy as np
    import soundfile as sf
    dummy_audio = np.random.randn(16000).astype(np.float32)
    sf.write(tmp.name, dummy_audio, 16000)
    model.transcribe(tmp.name)
print("Whisper model ready")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()
            
            # Transcribe with optimized settings
            result = model.transcribe(
                tmp.name,
                language="en",  # Set to None for auto-detection
                fp16=torch.cuda.is_available(),
                no_speech_threshold=0.6,
                logprob_threshold=-1.0
            )
            
            os.unlink(tmp.name)
            return {"text": result["text"].strip()}
            
    except Exception as e:
        return {"error": str(e), "text": ""}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
