#!/usr/bin/env python3
"""
Simple test to isolate the health endpoint issue
"""
import requests

def test_health_direct():
    """Test health endpoint directly"""
    try:
        response = requests.get("http://localhost:8000/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root Status: {response.status_code}")
        print(f"Root Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing endpoints...")
    print("=" * 30)
    
    print("Testing root endpoint:")
    test_root()
    
    print("\nTesting health endpoint:")
    test_health_direct() 