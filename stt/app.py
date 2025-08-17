from flask import Flask, request, jsonify
import whisper
import tempfile
import os
import numpy as np

app = Flask(__name__)

# Load Whisper model on startup
print("Loading Whisper Medium model...")
model = whisper.load_model("medium")
print("Whisper model loaded")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        audio_file = request.files['audio']
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            audio_file.save(tmp.name)
            
            # Transcribe with faster settings
            result = model.transcribe(
                tmp.name,
                language='en',  # Set language for speed
                fp16=True,      # Use half precision
                beam_size=1,    # Faster beam search
                best_of=1       # Single candidate
            )
            
            # Cleanup
            os.unlink(tmp.name)
            
            return jsonify({'text': result['text']})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)