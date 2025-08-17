#!/usr/bin/env python3
"""
Startup script for all AI Voice Assistant services
"""
import subprocess
import time
import os
import sys
from pathlib import Path

def start_service(name, script_path, port):
    """Start a service in a new process"""
    print(f"Starting {name} on port {port}...")
    try:
        process = subprocess.Popen([
            sys.executable, script_path
        ], cwd=os.path.dirname(script_path))
        print(f"✓ {name} started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"✗ Failed to start {name}: {e}")
        return None

def main():
    """Start all services"""
    print("🚀 Starting AI Voice Assistant Services...")
    
    # Get project root
    project_root = Path(__file__).parent
    
    services = [
        ("STT Service", project_root / "stt" / "stt_service.py", 5001),
        ("LLM Service", project_root / "llm" / "llm_service.py", 5002),
        ("TTS Service", project_root / "tts" / "tts_service.py", 5003),
    ]
    
    processes = []
    
    # Start Python services
    for name, script, port in services:
        process = start_service(name, script, port)
        if process:
            processes.append((name, process))
        time.sleep(2)  # Wait between starts
    
    # Start Node.js orchestrator
    print("Starting Node.js Orchestrator...")
    try:
        node_process = subprocess.Popen([
            "node", "orchestrator/index.js"
        ], cwd=project_root)
        processes.append(("Orchestrator", node_process))
        print(f"✓ Orchestrator started (PID: {node_process.pid})")
    except Exception as e:
        print(f"✗ Failed to start Orchestrator: {e}")
    
    print("\n🎉 All services started!")
    print("📱 Open http://localhost:3000 in your browser")
    print("⏹️  Press Ctrl+C to stop all services")
    
    try:
        # Wait for all processes
        for name, process in processes:
            process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        for name, process in processes:
            try:
                process.terminate()
                print(f"✓ Stopped {name}")
            except:
                pass

if __name__ == "__main__":
    main()