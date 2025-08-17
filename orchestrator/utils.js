function mergeBuffers(chunks) {
    const totalLength = chunks.reduce((acc, c) => acc + c.length, 0);
    const result = new Float32Array(totalLength);
    let offset = 0;
    chunks.forEach(c => {
        result.set(c, offset);
        offset += c.length;
    });
    return Buffer.from(result.buffer);
}

function createWavHeader(sampleRate, numChannels, bitsPerSample, dataLength) {
    const buffer = new ArrayBuffer(44);
    const view = new DataView(buffer);
    
    const writeString = (offset, string) => {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    };
    
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + dataLength, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numChannels * bitsPerSample / 8, true);
    view.setUint16(32, numChannels * bitsPerSample / 8, true);
    view.setUint16(34, bitsPerSample, true);
    writeString(36, 'data');
    view.setUint32(40, dataLength, true);
    
    return new Uint8Array(buffer);
}

module.exports = { mergeBuffers, createWavHeader };
