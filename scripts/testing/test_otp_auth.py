#!/usr/bin/env python3
"""
OTP Authentication Test Script

This script tests the OTP authentication flow including:
- Sending OTP to phone/email
- Verifying OTP codes
- Phone/email login endpoints
"""

import requests
import json
import time
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_section(title):
    """Print a section header."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_result(success, message, data=None):
    """Print test result."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    if data:
        print(f"   Data: {json.dumps(data, indent=2)}")

def test_send_phone_otp():
    """Test sending OTP to phone number."""
    print_section("Testing Phone OTP Send")
    
    # Test data
    test_phone = "+12345678901"
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/send/",
            json={
                "identifier": test_phone,
                "type": "phone"
            },
            headers={"Content-Type": "application/json"}
        )
        
        success = response.status_code == 200
        data = response.json() if response.content else None
        
        print_result(success, f"Send OTP to phone {test_phone}", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_send_email_otp():
    """Test sending OTP to email."""
    print_section("Testing Email OTP Send")
    
    # Test data
    test_email = "test@example.com"
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/send/",
            json={
                "identifier": test_email,
                "type": "email"
            },
            headers={"Content-Type": "application/json"}
        )
        
        success = response.status_code == 200
        data = response.json() if response.content else None
        
        print_result(success, f"Send OTP to email {test_email}", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_phone_login():
    """Test phone login endpoint."""
    print_section("Testing Phone Login")
    
    test_phone = "+12345678901"
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/phone-login/",
            json={"phone_number": test_phone},
            headers={"Content-Type": "application/json"}
        )
        
        success = response.status_code == 200
        data = response.json() if response.content else None
        
        print_result(success, f"Phone login for {test_phone}", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_email_login():
    """Test email login endpoint."""
    print_section("Testing Email Login")
    
    test_email = "test@example.com"
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/email-login/",
            json={"email": test_email},
            headers={"Content-Type": "application/json"}
        )
        
        success = response.status_code == 200
        data = response.json() if response.content else None
        
        print_result(success, f"Email login for {test_email}", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_verify_otp(identifier, otp_code, otp_type):
    """Test OTP verification."""
    print_section(f"Testing OTP Verification ({otp_type})")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/verify/",
            json={
                "identifier": identifier,
                "otp_code": otp_code,
                "type": otp_type
            },
            headers={"Content-Type": "application/json"}
        )
        
        success = response.status_code == 200
        data = response.json() if response.content else None
        
        print_result(success, f"Verify OTP for {identifier}", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_invalid_otp():
    """Test invalid OTP verification."""
    print_section("Testing Invalid OTP")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/verify/",
            json={
                "identifier": "+12345678901",
                "otp_code": "000000",
                "type": "phone"
            },
            headers={"Content-Type": "application/json"}
        )
        
        # Should fail with invalid OTP
        success = response.status_code == 400
        data = response.json() if response.content else None
        
        print_result(success, "Invalid OTP should be rejected", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_invalid_phone_format():
    """Test invalid phone number format."""
    print_section("Testing Invalid Phone Format")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/send/",
            json={
                "identifier": "invalid-phone",
                "type": "phone"
            },
            headers={"Content-Type": "application/json"}
        )
        
        # Should fail with invalid format
        success = response.status_code == 400
        data = response.json() if response.content else None
        
        print_result(success, "Invalid phone format should be rejected", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_invalid_email_format():
    """Test invalid email format."""
    print_section("Testing Invalid Email Format")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/otp/send/",
            json={
                "identifier": "invalid-email",
                "type": "email"
            },
            headers={"Content-Type": "application/json"}
        )
        
        # Should fail with invalid format
        success = response.status_code == 400
        data = response.json() if response.content else None
        
        print_result(success, "Invalid email format should be rejected", data)
        return success, data
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def main():
    """Run all OTP authentication tests."""
    print("🚀 Starting OTP Authentication Tests")
    print(f"Testing against: {BASE_URL}")
    
    # Test invalid formats first
    test_invalid_phone_format()
    test_invalid_email_format()
    
    # Test OTP sending
    test_send_phone_otp()
    test_send_email_otp()
    
    # Test login endpoints
    test_phone_login()
    test_email_login()
    
    # Test invalid OTP
    test_invalid_otp()
    
    # Note: To test actual OTP verification, you need to:
    # 1. Create a user with phone/email in the database
    # 2. Send OTP to get the code from logs
    # 3. Use that code to test verification
    
    print_section("Test Summary")
    print("📝 Note: To test actual OTP verification:")
    print("1. Create a user with phone/email in the database")
    print("2. Send OTP and check the console logs for the code")
    print("3. Use that code to test the verify endpoint")
    print("\n🔍 Check the backend console for OTP codes in development mode")

if __name__ == "__main__":
    main() 