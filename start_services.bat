@echo off
echo Starting AI Voice Assistant Services...

REM Start Python services in background
start "STT Service" python stt/stt_service.py
timeout /t 3 /nobreak >nul

start "LLM Service" python llm/llm_service.py
timeout /t 3 /nobreak >nul

start "TTS Service" python tts/tts_service.py
timeout /t 3 /nobreak >nul

REM Start Node.js orchestrator
echo Starting Node.js Orchestrator...
start "Orchestrator" node orchestrator/index.js

echo.
echo All services started!
echo Open http://localhost:3000 in your browser
echo.
pause