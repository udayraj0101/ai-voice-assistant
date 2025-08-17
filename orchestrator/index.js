require('dotenv').config();
const WebSocket = require('ws');
const fetch = require('node-fetch');
const express = require('express');
const path = require('path');
const { mergeBuffers } = require('./utils');

const STT_HOST = `http://${process.env.STT_HOST}:${process.env.STT_PORT}`;
const LLM_HOST = `http://${process.env.LLM_HOST}:${process.env.LLM_PORT}`;
const TTS_HOST = `http://${process.env.TTS_HOST}:${process.env.TTS_PORT}`;
const PORT = process.env.ORCH_PORT || 3000;

// Serve frontend
const app = express();
app.use(express.static(path.join(__dirname, '../frontend')));
const server = require('http').createServer(app);

const wss = new WebSocket.Server({ server });

wss.on('connection', ws => {
    console.log('Client connected');

    let audioBuffer = [];
    let silenceCounter = 0;
    let isProcessing = false;
    const SILENCE_LIMIT = 15;
    const MIN_AUDIO_LENGTH = 8000;

    ws.on('message', async msg => {
        if (isProcessing) return;
        
        const audioChunk = new Float32Array(msg);
        audioBuffer.push(audioChunk);

        const energy = audioChunk.reduce((sum, sample) => sum + sample * sample, 0) / audioChunk.length;
        const isSpeaking = energy > 0.001;
        
        if (!isSpeaking) silenceCounter++;
        else silenceCounter = 0;

        if (silenceCounter >= SILENCE_LIMIT && audioBuffer.length > MIN_AUDIO_LENGTH) {
            isProcessing = true;
            const combinedAudio = mergeBuffers(audioBuffer);
            audioBuffer = [];
            silenceCounter = 0;

            processAudio(combinedAudio, ws).finally(() => {
                isProcessing = false;
            });
        }
    });

    ws.on('close', () => console.log('Client disconnected'));
});

async function processAudio(audioData, ws) {
    try {
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('file', audioData, { filename: 'audio.wav', contentType: 'audio/wav' });
        
        const sttResp = await fetch(`${STT_HOST}/transcribe`, {
            method: 'POST',
            body: formData
        });
        const sttJson = await sttResp.json();
        const userText = sttJson.text?.trim();
        
        if (!userText || userText.length < 3) return;
        console.log('User:', userText);

        const llmResp = await fetch(`${LLM_HOST}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ prompt: userText })
        });
        const llmJson = await llmResp.json();
        const replyText = llmJson.text?.trim();
        
        if (!replyText) return;
        console.log('Assistant:', replyText);

        const ttsResp = await fetch(`${TTS_HOST}/synthesize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ text: replyText })
        });
        
        if (ttsResp.ok) {
            const audioBuffer = await ttsResp.arrayBuffer();
            ws.send(audioBuffer);
        }

    } catch (err) {
        console.error('Pipeline error:', err);
    }
}

server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`WebSocket server running on ws://localhost:${PORT}`);
});
