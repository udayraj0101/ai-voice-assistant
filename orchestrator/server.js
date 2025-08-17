const WebSocket = require('ws');
const express = require('express');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

const STT_URL = process.env.STT_URL || 'http://stt:5000';
const LLM_URL = process.env.LLM_URL || 'http://llm:5001';
const TTS_URL = process.env.TTS_URL || 'http://tts:5002';

wss.on('connection', (ws) => {
  console.log('Client connected');
  let audioBuffer = [];
  let isProcessing = false;
  
  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data);
      
      if (message.type === 'audio_chunk') {
        audioBuffer.push(message.data);
      }
      
      if (message.type === 'audio_end' && !isProcessing) {
        isProcessing = true;
        
        // Combine audio chunks
        const combinedAudio = audioBuffer.join('');
        audioBuffer = [];
        
        if (!combinedAudio) {
          isProcessing = false;
          return;
        }
        
        // Process pipeline concurrently where possible
        processAudioPipeline(ws, combinedAudio).finally(() => {
          isProcessing = false;
        });
      }
    } catch (error) {
      console.error('Error:', error.message);
      ws.send(JSON.stringify({ type: 'error', message: error.message }));
      isProcessing = false;
    }
  });
  
  ws.on('close', () => console.log('Client disconnected'));
});

async function processAudioPipeline(ws, audioData) {
  try {
    // STT
    const formData = new FormData();
    formData.append('audio', Buffer.from(audioData, 'base64'), 'audio.wav');
    
    const sttResponse = await axios.post(`${STT_URL}/transcribe`, formData, {
      headers: formData.getHeaders()
    });
    
    const text = sttResponse.data.text;
    if (!text.trim()) return;
    
    console.log('STT:', text);
    ws.send(JSON.stringify({ type: 'transcript', text }));
    
    // LLM
    const llmResponse = await axios.post(`${LLM_URL}/generate`, { text });
    const response = llmResponse.data.response;
    
    console.log('LLM:', response);
    
    // TTS
    const ttsResponse = await axios.post(`${TTS_URL}/synthesize`, { text: response }, {
      responseType: 'arraybuffer'
    });
    
    ws.send(JSON.stringify({
      type: 'audio_response',
      data: Buffer.from(ttsResponse.data).toString('base64')
    }));
    
  } catch (error) {
    console.error('Pipeline error:', error.message);
    ws.send(JSON.stringify({ type: 'error', message: error.message }));
  }
}

app.use(express.static('../frontend'));

server.listen(3000, () => {
  console.log('Orchestrator running on port 3000');
});