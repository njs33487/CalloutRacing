#!/usr/bin/env python3
"""
Test email verification flow
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_email_verification_flow():
    """Test the complete email verification flow"""
    
    # Step 1: Register a new user
    print("Step 1: Registering new user...")
    data = {
        "username": "verifieduser",
        "email": "verified@example.com", 
        "password": "TestPass123",
        "first_name": "Verified",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Registration successful")
        else:
            print("❌ Registration failed")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Try to login (should fail due to email verification)
    print("\nStep 2: Attempting login (should fail)...")
    login_data = {
        "username": "verifieduser",
        "password": "TestPass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 401 and "email_verification_required" in response.text:
            print("✅ Login correctly blocked due to email verification requirement")
        else:
            print("❌ Unexpected login response")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: Test resend verification email
    print("\nStep 3: Testing resend verification email...")
    resend_data = {"email": "verified@example.com"}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/resend-verification/", json=resend_data)
        print(f"Resend Status: {response.status_code}")
        print(f"Resend Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Resend verification email successful")
        else:
            print("❌ Resend verification email failed")
    except Exception as e:
        print(f"❌ Resend error: {e}")
    
    # Step 4: Test SSO config (public endpoint)
    print("\nStep 4: Testing SSO config...")
    try:
        response = requests.get(f"{BASE_URL}/auth/sso-config/")
        print(f"SSO Config Status: {response.status_code}")
        print(f"SSO Config Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SSO config endpoint working")
        else:
            print("❌ SSO config endpoint failed")
    except Exception as e:
        print(f"❌ SSO config error: {e}")

def test_password_reset_flow():
    """Test password reset flow"""
    print("\n" + "="*50)
    print("Testing Password Reset Flow")
    print("="*50)
    
    # Step 1: Request password reset
    print("Step 1: Requesting password reset...")
    reset_data = {"email": "verified@example.com"}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/request-password-reset/", json=reset_data)
        print(f"Password Reset Request Status: {response.status_code}")
        print(f"Password Reset Request Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Password reset request successful")
        else:
            print("❌ Password reset request failed")
    except Exception as e:
        print(f"❌ Password reset request error: {e}")

def main():
    print("Testing Email Verification and Password Reset Flow")
    print("=" * 60)
    
    test_email_verification_flow()
    test_password_reset_flow()
    
    print("\n" + "=" * 60)
    print("Email verification tests completed!")

if __name__ == "__main__":
    main() 