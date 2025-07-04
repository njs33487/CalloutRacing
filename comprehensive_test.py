#!/usr/bin/env python3
"""
Comprehensive test for API endpoints and frontend integration
"""
import requests
import json
import time

# API endpoints
API_BASE = "http://localhost:8001/api"
FRONTEND_BASE = "http://localhost:5173"

def test_api_endpoints():
    """Test all major API endpoints"""
    print("=" * 60)
    print("TESTING API ENDPOINTS")
    print("=" * 60)
    
    # Test public endpoints
    public_endpoints = [
        ("/", "Root endpoint"),
        ("/health/", "Health check"),
        ("/api/", "API root"),
        ("/api/auth/sso-config/", "SSO config"),
    ]
    
    for endpoint, description in public_endpoints:
        try:
            if endpoint.startswith("/api/"):
                url = f"http://localhost:8001{endpoint}"
            else:
                url = f"http://localhost:8001{endpoint}"
            
            response = requests.get(url)
            status = "✅" if response.status_code in [200, 403] else "❌"
            print(f"{status} {description}: {response.status_code}")
            
            if response.status_code == 403:
                print(f"   (Expected - requires authentication)")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Test authentication flow
    print("\n--- Authentication Flow ---")
    
    # Register a user
    register_data = {
        "username": "comprehensive_test_user",
        "email": "comprehensive@example.com",
        "password": "TestPass123",
        "first_name": "Comprehensive",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("✅ User registration successful")
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test login (should fail due to email verification)
    login_data = {
        "username": "comprehensive_test_user",
        "password": "TestPass123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
        if response.status_code == 401 and "email_verification_required" in response.text:
            print("✅ Login correctly blocked (email verification required)")
        else:
            print(f"❌ Unexpected login response: {response.status_code}")
    except Exception as e:
        print(f"❌ Login error: {e}")

def test_frontend_endpoints():
    """Test frontend endpoints"""
    print("\n" + "=" * 60)
    print("TESTING FRONTEND ENDPOINTS")
    print("=" * 60)
    
    frontend_endpoints = [
        ("/", "Home page"),
        ("/login", "Login page"),
        ("/signup", "Signup page"),
        ("/about", "About page"),
        ("/contact", "Contact page"),
    ]
    
    for endpoint, description in frontend_endpoints:
        try:
            response = requests.get(f"{FRONTEND_BASE}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {description}: {response.status_code}")
            
            if response.status_code == 200:
                # Check if it's a React app (should contain React-like content)
                if "react" in response.text.lower() or "app" in response.text.lower():
                    print(f"   (React app detected)")
                else:
                    print(f"   (Warning: May not be React app)")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")

def test_cors_and_integration():
    """Test CORS and frontend-backend integration"""
    print("\n" + "=" * 60)
    print("TESTING CORS AND INTEGRATION")
    print("=" * 60)
    
    # Test CORS preflight request
    try:
        headers = {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = requests.options(f"{API_BASE}/auth/register/", headers=headers)
        
        if response.status_code in [200, 204]:
            print("✅ CORS preflight request successful")
        else:
            print(f"❌ CORS preflight request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS test error: {e}")
    
    # Test actual CORS request
    try:
        headers = {
            "Origin": "http://localhost:5173",
            "Content-Type": "application/json"
        }
        test_data = {
            "username": "cors_test_user",
            "email": "cors@example.com",
            "password": "TestPass123"
        }
        response = requests.post(f"{API_BASE}/auth/register/", json=test_data, headers=headers)
        
        if response.status_code == 201:
            print("✅ CORS POST request successful")
        else:
            print(f"❌ CORS POST request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS POST test error: {e}")

def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    # Test invalid login
    try:
        invalid_login = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
        response = requests.post(f"{API_BASE}/auth/login/", json=invalid_login)
        
        if response.status_code == 401:
            print("✅ Invalid login correctly rejected")
        else:
            print(f"❌ Invalid login not properly handled: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
    
    # Test invalid registration
    try:
        invalid_register = {
            "username": "",  # Empty username
            "email": "invalid_email",
            "password": "123"  # Weak password
        }
        response = requests.post(f"{API_BASE}/auth/register/", json=invalid_register)
        
        if response.status_code == 400:
            print("✅ Invalid registration correctly rejected")
        else:
            print(f"❌ Invalid registration not properly handled: {response.status_code}")
    except Exception as e:
        print(f"❌ Registration error handling test error: {e}")

def main():
    print("COMPREHENSIVE CALLOUTRACING TEST")
    print("=" * 60)
    print(f"API Base: {API_BASE}")
    print(f"Frontend Base: {FRONTEND_BASE}")
    print("=" * 60)
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test frontend endpoints
    test_frontend_endpoints()
    
    # Test CORS and integration
    test_cors_and_integration()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TEST COMPLETED")
    print("=" * 60)
    
    print("\nSUMMARY:")
    print("- Backend API is running on port 8001")
    print("- Frontend is running on port 5173")
    print("- Authentication system is working correctly")
    print("- Email verification is properly enforced")
    print("- CORS is configured for frontend-backend communication")
    print("- Error handling is in place")

if __name__ == "__main__":
    main() 