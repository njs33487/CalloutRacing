#!/usr/bin/env python3
"""
Comprehensive Authentication Flow Test

This script tests the complete authentication flow including:
- User registration
- Email/Phone OTP verification
- Login with OTP
- Session management
- Error handling
"""

import requests
import json
import time
import random
import string
from datetime import datetime

# Configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"
# BASE_URL = "http://localhost:8000/api"  # For local testing

class AuthFlowTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "PASS" if success else "FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': timestamp
        })
        
    def generate_test_data(self):
        """Generate unique test data"""
        timestamp = int(time.time())
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        return {
            'username': f'testuser_{timestamp}_{random_suffix}',
            'email': f'testuser_{timestamp}_{random_suffix}@example.com',
            'phone': f'+1{random.randint(1000000000, 9999999999)}',
            'password': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
    def test_1_csrf_token(self):
        """Test CSRF token retrieval"""
        try:
            response = self.session.get(f"{BASE_URL}/auth/csrf/")
            success = response.status_code == 200
            self.log_test("CSRF Token Retrieval", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("CSRF Token Retrieval", False, str(e))
            return False
            
    def test_2_user_registration(self):
        """Test user registration"""
        test_data = self.generate_test_data()
        try:
            response = self.session.post(f"{BASE_URL}/auth/register/", json={
                'username': test_data['username'],
                'email': test_data['email'],
                'password': test_data['password'],
                'first_name': test_data['first_name'],
                'last_name': test_data['last_name']
            })
            
            success = response.status_code == 201
            self.log_test("User Registration", success, f"Status: {response.status_code}")
            
            if success:
                self.test_user_data = test_data
                print(f"   Created user: {test_data['username']}")
                
            return success
        except Exception as e:
            self.log_test("User Registration", False, str(e))
            return False
            
    def test_3_email_otp_send(self):
        """Test email OTP sending"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Email OTP Send", False, "No test user data available")
            return False
            
        try:
            response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                'identifier': self.test_user_data['email'],
                'type': 'email',
                'purpose': 'signup'
            })
            
            success = response.status_code == 200
            self.log_test("Email OTP Send", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   OTP sent to: {self.test_user_data['email']}")
                print(f"   Response: {response_data.get('message', 'No message')}")
                
            return success
        except Exception as e:
            self.log_test("Email OTP Send", False, str(e))
            return False
            
    def test_4_phone_otp_send(self):
        """Test phone OTP sending"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Phone OTP Send", False, "No test user data available")
            return False
            
        try:
            response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                'identifier': self.test_user_data['phone'],
                'type': 'phone',
                'purpose': 'signup'
            })
            
            success = response.status_code == 200
            self.log_test("Phone OTP Send", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   OTP sent to: {self.test_user_data['phone']}")
                print(f"   Response: {response_data.get('message', 'No message')}")
                
            return success
        except Exception as e:
            self.log_test("Phone OTP Send", False, str(e))
            return False
            
    def test_5_otp_verification_simulation(self):
        """Test OTP verification (simulated)"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("OTP Verification", False, "No test user data available")
            return False
            
        # Simulate OTP verification (in real scenario, user would enter the code)
        test_otp = "123456"
        
        try:
            # Test email OTP verification
            response = self.session.post(f"{BASE_URL}/auth/otp/verify/", json={
                'identifier': self.test_user_data['email'],
                'otp_code': test_otp,
                'type': 'email',
                'purpose': 'signup'
            })
            
            # This should fail with invalid OTP, but the endpoint should be accessible
            success = response.status_code in [200, 400]  # 400 is expected for invalid OTP
            self.log_test("Email OTP Verification Endpoint", success, f"Status: {response.status_code}")
            
            # Test phone OTP verification
            response = self.session.post(f"{BASE_URL}/auth/otp/verify/", json={
                'identifier': self.test_user_data['phone'],
                'otp_code': test_otp,
                'type': 'phone',
                'purpose': 'signup'
            })
            
            success = response.status_code in [200, 400]  # 400 is expected for invalid OTP
            self.log_test("Phone OTP Verification Endpoint", success, f"Status: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test("OTP Verification", False, str(e))
            return False
            
    def test_6_login_with_password(self):
        """Test traditional password login"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Password Login", False, "No test user data available")
            return False
            
        try:
            response = self.session.post(f"{BASE_URL}/auth/login/", json={
                'username': self.test_user_data['username'],
                'password': self.test_user_data['password']
            })
            
            success = response.status_code == 200
            self.log_test("Password Login", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   Login successful for: {self.test_user_data['username']}")
                self.user_session = response_data
                
            return success
        except Exception as e:
            self.log_test("Password Login", False, str(e))
            return False
            
    def test_7_email_otp_login(self):
        """Test email OTP login flow"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Email OTP Login", False, "No test user data available")
            return False
            
        try:
            # Step 1: Send OTP for login
            response = self.session.post(f"{BASE_URL}/auth/email-login/", json={
                'email': self.test_user_data['email']
            })
            
            success = response.status_code == 200
            self.log_test("Email OTP Login - Send OTP", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   Login OTP sent to: {self.test_user_data['email']}")
                
            return success
        except Exception as e:
            self.log_test("Email OTP Login", False, str(e))
            return False
            
    def test_8_phone_otp_login(self):
        """Test phone OTP login flow"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Phone OTP Login", False, "No test user data available")
            return False
            
        try:
            # Step 1: Send OTP for login
            response = self.session.post(f"{BASE_URL}/auth/phone-login/", json={
                'phone_number': self.test_user_data['phone']
            })
            
            success = response.status_code == 200
            self.log_test("Phone OTP Login - Send OTP", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   Login OTP sent to: {self.test_user_data['phone']}")
                
            return success
        except Exception as e:
            self.log_test("Phone OTP Login", False, str(e))
            return False
            
    def test_9_rate_limiting(self):
        """Test rate limiting for OTP requests"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Rate Limiting", False, "No test user data available")
            return False
            
        try:
            # Make multiple rapid requests to test rate limiting
            responses = []
            for i in range(6):  # Should hit rate limit after 5 attempts
                response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                    'identifier': self.test_user_data['email'],
                    'type': 'email',
                    'purpose': 'login'
                })
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay between requests
                
            # Check if rate limiting is working
            rate_limited = 429 in responses
            success = rate_limited or len([r for r in responses if r == 200]) <= 5
            
            self.log_test("Rate Limiting", success, f"Responses: {responses}")
            return success
        except Exception as e:
            self.log_test("Rate Limiting", False, str(e))
            return False
            
    def test_10_error_handling(self):
        """Test error handling for invalid requests"""
        try:
            # Test invalid email format
            response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                'identifier': 'invalid-email',
                'type': 'email',
                'purpose': 'login'
            })
            
            success = response.status_code == 400
            self.log_test("Invalid Email Format", success, f"Status: {response.status_code}")
            
            # Test invalid phone format
            response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                'identifier': '123',
                'type': 'phone',
                'purpose': 'login'
            })
            
            success = response.status_code == 400
            self.log_test("Invalid Phone Format", success, f"Status: {response.status_code}")
            
            # Test non-existent user
            response = self.session.post(f"{BASE_URL}/auth/otp/send/", json={
                'identifier': 'nonexistent@example.com',
                'type': 'email',
                'purpose': 'login'
            })
            
            success = response.status_code == 404
            self.log_test("Non-existent User", success, f"Status: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test("Error Handling", False, str(e))
            return False
            
    def test_11_session_management(self):
        """Test session management after login"""
        if not hasattr(self, 'user_session'):
            self.log_test("Session Management", False, "No user session available")
            return False
            
        try:
            # Test accessing protected endpoint
            response = self.session.get(f"{BASE_URL}/auth/profile/")
            
            success = response.status_code == 200
            self.log_test("Protected Endpoint Access", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   User profile: {response_data.get('username', 'Unknown')}")
                
            return success
        except Exception as e:
            self.log_test("Session Management", False, str(e))
            return False
            
    def test_12_logout(self):
        """Test logout functionality"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/logout/")
            
            success = response.status_code == 200
            self.log_test("Logout", success, f"Status: {response.status_code}")
            
            # Test that session is invalidated
            response = self.session.get(f"{BASE_URL}/auth/profile/")
            session_invalidated = response.status_code == 403
            
            self.log_test("Session Invalidation", session_invalidated, f"Status: {response.status_code}")
            
            return success and session_invalidated
        except Exception as e:
            self.log_test("Logout", False, str(e))
            return False
            
    def run_all_tests(self):
        """Run all authentication flow tests"""
        print("Starting Authentication Flow Tests")
        print("=" * 50)
        
        tests = [
            ("CSRF Token", self.test_1_csrf_token),
            ("User Registration", self.test_2_user_registration),
            ("Email OTP Send", self.test_3_email_otp_send),
            ("Phone OTP Send", self.test_4_phone_otp_send),
            ("OTP Verification Endpoints", self.test_5_otp_verification_simulation),
            ("Password Login", self.test_6_login_with_password),
            ("Email OTP Login", self.test_7_email_otp_login),
            ("Phone OTP Login", self.test_8_phone_otp_login),
            ("Rate Limiting", self.test_9_rate_limiting),
            ("Error Handling", self.test_10_error_handling),
            ("Session Management", self.test_11_session_management),
            ("Logout", self.test_12_logout),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Exception: {str(e)}")
                
        print("\n" + "=" * 50)
        print(f"Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("All authentication flow tests passed!")
        else:
            print("Some tests failed. Check the logs above.")
            
        return passed == total

def main():
    """Main test runner"""
    tester = AuthFlowTester()
    success = tester.run_all_tests()
    
    # Save test results to file
    with open('auth_flow_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'base_url': BASE_URL,
            'results': tester.test_results,
            'success': success
        }, f, indent=2)
        
    print(f"\n📄 Test results saved to: auth_flow_test_results.json")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 