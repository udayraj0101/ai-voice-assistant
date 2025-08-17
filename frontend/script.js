const startBtn = document.getElementById('start');
const stopBtn = document.getElementById('stop');
const output = document.getElementById('output');
const statusEl = document.getElementById('status');

let ws, audioContext, processor, stream;

startBtn.onclick = async () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusEl.textContent = "Status: Connecting...";

    const wsUrl = window.location.hostname === 'localhost' 
        ? 'ws://localhost:3000' 
        : `ws://${window.location.hostname}:3000`;
    ws = new WebSocket(wsUrl);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        statusEl.textContent = "Status: Connected, listening...";
    };

    ws.onclose = () => {
        statusEl.textContent = "Status: Disconnected";
    };

    ws.onerror = () => {
        statusEl.textContent = "Status: Connection error";
    };

    ws.onmessage = e => {
        const blob = new Blob([e.data], { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        output.src = url;
        output.play();
    };

    stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { 
            sampleRate: 16000,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true
        } 
    });
    
    audioContext = new AudioContext({ sampleRate: 16000 });
    const source = audioContext.createMediaStreamSource(stream);
    processor = audioContext.createScriptProcessor(4096, 1, 1);
    
    processor.onaudioprocess = (e) => {
        if (ws.readyState === WebSocket.OPEN) {
            const inputData = e.inputBuffer.getChannelData(0);
            const buffer = new ArrayBuffer(inputData.length * 4);
            const view = new Float32Array(buffer);
            view.set(inputData);
            ws.send(buffer);
        }
    };
    
    source.connect(processor);
    processor.connect(audioContext.destination);
};

stopBtn.onclick = () => {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    statusEl.textContent = "Status: Idle";

    if (processor) {
        processor.disconnect();
        processor = null;
    }
    
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
    }
};
