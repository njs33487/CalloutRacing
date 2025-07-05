#!/usr/bin/env python3
"""
Simple test script to check authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_health():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health/")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print("❌ Server is not responding properly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False

def test_registration():
    """Test user registration"""
    data = {
        "username": "testuser123",
        "email": "test123@example.com", 
        "password": "TestPass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"Registration: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful")
            return True
        else:
            print("❌ Registration failed")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    data = {
        "username": "testuser123",
        "password": "TestPass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Login: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful")
            return response.json().get('token')
        else:
            print("❌ Login failed")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_profile(token):
    """Test getting user profile"""
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        print(f"Profile: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Profile access successful")
            return True
        else:
            print("❌ Profile access failed")
            return False
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return False

def main():
    print("Testing CalloutRacing Authentication Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        return
    
    print("\n" + "=" * 50)
    
    # Test 2: Registration
    if not test_registration():
        print("Registration failed, skipping login test")
        return
    
    print("\n" + "=" * 50)
    
    # Test 3: Login
    token = test_login()
    if not token:
        print("Login failed, skipping profile test")
        return
    
    print("\n" + "=" * 50)
    
    # Test 4: Profile access
    test_profile(token)
    
    print("\n" + "=" * 50)
    print("Authentication tests completed!")

if __name__ == "__main__":
    main() 