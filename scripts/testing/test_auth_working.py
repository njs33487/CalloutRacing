#!/usr/bin/env python3
"""
Test authentication endpoints on the working server (port 8001)
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_registration():
    """Test user registration"""
    data = {
        "username": "testuser456",
        "email": "test456@example.com", 
        "password": "TestPass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.text}")
        
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
        "username": "testuser456",
        "password": "TestPass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
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
        print(f"Profile Status: {response.status_code}")
        print(f"Profile Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Profile access successful")
            return True
        else:
            print("❌ Profile access failed")
            return False
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return False

def test_api_endpoints():
    """Test various API endpoints"""
    print("\n" + "="*50)
    print("Testing API Endpoints")
    print("="*50)
    
    # Test SSO config (public endpoint)
    try:
        response = requests.get(f"{BASE_URL}/auth/sso-config/")
        print(f"SSO Config Status: {response.status_code}")
        print(f"SSO Config Response: {response.text[:200]}")
    except Exception as e:
        print(f"SSO Config Error: {e}")
    
    # Test user search (requires auth)
    try:
        response = requests.get(f"{BASE_URL}/users/")
        print(f"Users List Status: {response.status_code}")
        print(f"Users List Response: {response.text[:200]}")
    except Exception as e:
        print(f"Users List Error: {e}")

def main():
    print("Testing CalloutRacing Authentication Endpoints (Port 8001)")
    print("=" * 60)
    
    # Test 1: Registration
    if not test_registration():
        print("Registration failed, skipping login test")
        return
    
    print("\n" + "=" * 60)
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("Login failed, skipping profile test")
        return
    
    print("\n" + "=" * 60)
    
    # Test 3: Profile access
    test_profile(token)
    
    print("\n" + "=" * 60)
    
    # Test 4: Other API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("Authentication tests completed!")

if __name__ == "__main__":
    main() 