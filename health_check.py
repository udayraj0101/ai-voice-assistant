#!/usr/bin/env python3
"""
Health check script for AI Voice Assistant services
"""
import requests
import json
import time

def check_service(name, url, timeout=5):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    """Check all services"""
    services = [
        ("STT Service", "http://localhost:5001/docs"),
        ("LLM Service", "http://localhost:5002/docs"),
        ("TTS Service", "http://localhost:5003/docs"),
        ("Orchestrator", "http://localhost:3000"),
    ]
    
    print("🔍 Checking AI Voice Assistant Services...\n")
    
    all_healthy = True
    
    for name, url in services:
        is_healthy, status = check_service(name, url)
        status_icon = "✅" if is_healthy else "❌"
        print(f"{status_icon} {name}: {status}")
        
        if not is_healthy:
            all_healthy = False
    
    print("\n" + "="*50)
    
    if all_healthy:
        print("🎉 All services are healthy!")
        print("🌐 Open http://localhost:3000 to use the assistant")
    else:
        print("⚠️  Some services are not responding")
        print("💡 Try running: python start_services.py")
    
    return 0 if all_healthy else 1

if __name__ == "__main__":
    exit(main())