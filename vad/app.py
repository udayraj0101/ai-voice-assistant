from flask import Flask, request, jsonify
import numpy as np
import librosa

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_voice():
    try:
        audio_file = request.files['audio']
        
        # Load audio
        audio_data, sr = librosa.load(audio_file, sr=16000)
        
        # Simple energy-based VAD
        energy = np.sum(audio_data ** 2)
        threshold = 0.01  # Adjust based on testing
        
        has_voice = energy > threshold
        
        return jsonify({
            'has_voice': has_voice,
            'energy': float(energy)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)