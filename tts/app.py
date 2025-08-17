from flask import Flask, request, send_file
from TTS.api import TTS
import tempfile
import os

app = Flask(__name__)

# Load TTS model on startup
print("Loading Coqui XTTS model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
print("TTS model loaded")

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        data = request.json
        text = data['text']
        
        # Create temp file for audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            # Synthesize speech
            tts.tts_to_file(
                text=text,
                file_path=tmp.name,
                speaker_wav=None,  # Use default voice
                language="en"
            )
            
            return send_file(tmp.name, mimetype='audio/wav')
            
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)