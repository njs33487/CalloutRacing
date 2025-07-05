#!/usr/bin/env python3
"""
Test the new server on port 8001
"""
import requests

def test_endpoints():
    """Test endpoints on port 8001"""
    base_url = "http://localhost:8001"
    
    try:
        # Test root
        response = requests.get(f"{base_url}/")
        print(f"Root Status: {response.status_code}")
        print(f"Root Response: {response.text[:200]}")
        
        # Test health
        response = requests.get(f"{base_url}/health/")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.text}")
        
        # Test API root
        response = requests.get(f"{base_url}/api/")
        print(f"API Root Status: {response.status_code}")
        print(f"API Root Response: {response.text[:200]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing server on port 8001...")
    test_endpoints() 