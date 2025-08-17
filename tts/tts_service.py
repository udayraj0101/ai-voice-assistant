from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
import torch
import tempfile
import os
import uvicorn
import io

app = FastAPI()

# Use fastest TTS model for RunPod
try:
    from TTS.api import TTS
    # Use fastest available model
    tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
    print("TTS model loaded successfully")
except Exception as e:
    print(f"TTS loading error: {e}")
    tts = None

@app.post("/synthesize")
async def synthesize(text: str = Form(...)):
    try:
        if not tts:
            # Return empty audio if TTS fails to load
            return StreamingResponse(io.BytesIO(b''), media_type="audio/wav")
        
        # Limit text length for faster processing
        text = text[:200] if len(text) > 200 else text
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_path = tmp.name
        
        # Generate speech
        tts.tts_to_file(
            text=text, 
            file_path=tmp_path,
            speed=1.2  # Slightly faster speech
        )
        
        # Read and return audio file
        with open(tmp_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return StreamingResponse(
            io.BytesIO(audio_data), 
            media_type="audio/wav",
            headers={"Content-Length": str(len(audio_data))}
        )
        
    except Exception as e:
        print(f"TTS Error: {e}")
        # Return empty audio on error
        return StreamingResponse(io.BytesIO(b''), media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
