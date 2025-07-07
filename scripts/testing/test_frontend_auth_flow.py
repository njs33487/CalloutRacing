#!/usr/bin/env python3
"""
Frontend Authentication Flow Test

This script tests the frontend authentication flow by simulating user interactions
with the React app, including:
- Registration flow
- OTP verification
- Login flows
- Session management
- Error handling
"""

import requests
import json
import time
import random
import string
from datetime import datetime
from urllib.parse import urljoin

# Configuration
FRONTEND_URL = "https://calloutracing-frontend-production.up.railway.app"
BACKEND_URL = "https://calloutracing-backend-production.up.railway.app/api"

class FrontendAuthTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'FrontendAuthTester/1.0'
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
            'username': f'frontend_test_{timestamp}_{random_suffix}',
            'email': f'frontend_test_{timestamp}_{random_suffix}@example.com',
            'phone': f'+1{random.randint(1000000000, 9999999999)}',
            'password': 'FrontendTest123!',
            'first_name': 'Frontend',
            'last_name': 'Tester'
        }
        
    def test_1_frontend_health(self):
        """Test if frontend is accessible"""
        try:
            response = self.session.get(FRONTEND_URL)
            success = response.status_code == 200
            self.log_test("Frontend Health Check", success, f"Status: {response.status_code}")
            
            if success:
                print(f"   Frontend accessible at: {FRONTEND_URL}")
                
            return success
        except Exception as e:
            self.log_test("Frontend Health Check", False, str(e))
            return False
            
    def test_2_frontend_landing_page(self):
        """Test landing page accessibility"""
        try:
            response = self.session.get(f"{FRONTEND_URL}/")
            success = response.status_code == 200
            self.log_test("Landing Page", success, f"Status: {response.status_code}")
            
            if success:
                # Check if it's a React app (should contain React-related content)
                content = response.text.lower()
                is_react_app = any(keyword in content for keyword in ['react', 'app', 'script'])
                self.log_test("React App Detection", is_react_app, "React app detected")
                
            return success
        except Exception as e:
            self.log_test("Landing Page", False, str(e))
            return False
            
    def test_3_registration_page(self):
        """Test registration page accessibility"""
        try:
            response = self.session.get(f"{FRONTEND_URL}/signup")
            success = response.status_code == 200
            self.log_test("Registration Page", success, f"Status: {response.status_code}")
            
            if success:
                content = response.text.lower()
                has_signup_form = any(keyword in content for keyword in ['signup', 'register', 'form'])
                self.log_test("Signup Form Detection", has_signup_form, "Signup form detected")
                
            return success
        except Exception as e:
            self.log_test("Registration Page", False, str(e))
            return False
            
    def test_4_login_page(self):
        """Test login page accessibility"""
        try:
            response = self.session.get(f"{FRONTEND_URL}/login")
            success = response.status_code == 200
            self.log_test("Login Page", success, f"Status: {response.status_code}")
            
            if success:
                content = response.text.lower()
                has_login_form = any(keyword in content for keyword in ['login', 'signin', 'form'])
                self.log_test("Login Form Detection", has_login_form, "Login form detected")
                
            return success
        except Exception as e:
            self.log_test("Login Page", False, str(e))
            return False
            
    def test_5_otp_login_page(self):
        """Test OTP login page accessibility"""
        try:
            response = self.session.get(f"{FRONTEND_URL}/otp-login")
            success = response.status_code == 200
            self.log_test("OTP Login Page", success, f"Status: {response.status_code}")
            
            if success:
                content = response.text.lower()
                has_otp_form = any(keyword in content for keyword in ['otp', 'verification', 'code'])
                self.log_test("OTP Form Detection", has_otp_form, "OTP form detected")
                
            return success
        except Exception as e:
            self.log_test("OTP Login Page", False, str(e))
            return False
            
    def test_6_backend_api_connectivity(self):
        """Test backend API connectivity from frontend perspective"""
        try:
            # Test CSRF endpoint
            response = self.session.get(f"{BACKEND_URL}/auth/csrf/")
            success = response.status_code == 200
            self.log_test("Backend API Connectivity", success, f"CSRF Status: {response.status_code}")
            
            if success:
                print(f"   Backend API accessible at: {BACKEND_URL}")
                
            return success
        except Exception as e:
            self.log_test("Backend API Connectivity", False, str(e))
            return False
            
    def test_7_registration_flow_simulation(self):
        """Simulate registration flow"""
        test_data = self.generate_test_data()
        
        try:
            # Step 1: Register user
            response = self.session.post(f"{BACKEND_URL}/auth/register/", json={
                'username': test_data['username'],
                'email': test_data['email'],
                'password': test_data['password'],
                'first_name': test_data['first_name'],
                'last_name': test_data['last_name']
            })
            
            success = response.status_code == 201
            self.log_test("Registration Flow - Create User", success, f"Status: {response.status_code}")
            
            if success:
                self.test_user_data = test_data
                print(f"   Created test user: {test_data['username']}")
                
                # Step 2: Send email OTP
                response = self.session.post(f"{BACKEND_URL}/auth/otp/send/", json={
                    'identifier': test_data['email'],
                    'type': 'email',
                    'purpose': 'signup'
                })
                
                otp_success = response.status_code == 200
                self.log_test("Registration Flow - Email OTP", otp_success, f"Status: {response.status_code}")
                
                # Step 3: Send phone OTP
                response = self.session.post(f"{BACKEND_URL}/auth/otp/send/", json={
                    'identifier': test_data['phone'],
                    'type': 'phone',
                    'purpose': 'signup'
                })
                
                phone_otp_success = response.status_code == 200
                self.log_test("Registration Flow - Phone OTP", phone_otp_success, f"Status: {response.status_code}")
                
            return success
        except Exception as e:
            self.log_test("Registration Flow", False, str(e))
            return False
            
    def test_8_login_flow_simulation(self):
        """Simulate login flow"""
        if not hasattr(self, 'test_user_data'):
            self.log_test("Login Flow", False, "No test user data available")
            return False
            
        try:
            # Step 1: Traditional password login
            response = self.session.post(f"{BACKEND_URL}/auth/login/", json={
                'username': self.test_user_data['username'],
                'password': self.test_user_data['password']
            })
            
            success = response.status_code == 200
            self.log_test("Login Flow - Password Login", success, f"Status: {response.status_code}")
            
            if success:
                self.user_session = response.json()
                print(f"   Login successful for: {self.test_user_data['username']}")
                
                # Step 2: Email OTP login
                response = self.session.post(f"{BACKEND_URL}/auth/email-login/", json={
                    'email': self.test_user_data['email']
                })
                
                email_login_success = response.status_code == 200
                self.log_test("Login Flow - Email OTP", email_login_success, f"Status: {response.status_code}")
                
                # Step 3: Phone OTP login
                response = self.session.post(f"{BACKEND_URL}/auth/phone-login/", json={
                    'phone_number': self.test_user_data['phone']
                })
                
                phone_login_success = response.status_code == 200
                self.log_test("Login Flow - Phone OTP", phone_login_success, f"Status: {response.status_code}")
                
            return success
        except Exception as e:
            self.log_test("Login Flow", False, str(e))
            return False
            
    def test_9_session_management(self):
        """Test session management"""
        if not hasattr(self, 'user_session'):
            self.log_test("Session Management", False, "No user session available")
            return False
            
        try:
            # Test accessing protected endpoint
            response = self.session.get(f"{BACKEND_URL}/auth/profile/")
            
            success = response.status_code == 200
            self.log_test("Session Management - Profile Access", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   User profile accessible: {response_data.get('username', 'Unknown')}")
                
            return success
        except Exception as e:
            self.log_test("Session Management", False, str(e))
            return False
            
    def test_10_error_handling(self):
        """Test error handling in frontend flows"""
        try:
            # Test invalid registration data
            response = self.session.post(f"{BACKEND_URL}/auth/register/", json={
                'username': 'test',
                'email': 'invalid-email',
                'password': 'weak'
            })
            
            success = response.status_code == 400
            self.log_test("Error Handling - Invalid Registration", success, f"Status: {response.status_code}")
            
            # Test invalid login
            response = self.session.post(f"{BACKEND_URL}/auth/login/", json={
                'username': 'nonexistent',
                'password': 'wrong'
            })
            
            login_error_success = response.status_code == 400
            self.log_test("Error Handling - Invalid Login", login_error_success, f"Status: {response.status_code}")
            
            return success and login_error_success
        except Exception as e:
            self.log_test("Error Handling", False, str(e))
            return False
            
    def test_11_logout_flow(self):
        """Test logout flow"""
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/logout/")
            
            success = response.status_code == 200
            self.log_test("Logout Flow", success, f"Status: {response.status_code}")
            
            # Test that session is invalidated
            response = self.session.get(f"{BACKEND_URL}/auth/profile/")
            session_invalidated = response.status_code == 403
            
            self.log_test("Logout Flow - Session Invalidation", session_invalidated, f"Status: {response.status_code}")
            
            return success and session_invalidated
        except Exception as e:
            self.log_test("Logout Flow", False, str(e))
            return False
            
    def test_12_frontend_routing(self):
        """Test frontend routing for auth pages"""
        auth_pages = [
            '/login',
            '/signup',
            '/otp-login',
            '/forgot-password',
            '/reset-password'
        ]
        
        passed = 0
        total = len(auth_pages)
        
        for page in auth_pages:
            try:
                response = self.session.get(f"{FRONTEND_URL}{page}")
                success = response.status_code == 200
                self.log_test(f"Frontend Routing - {page}", success, f"Status: {response.status_code}")
                
                if success:
                    passed += 1
            except Exception as e:
                self.log_test(f"Frontend Routing - {page}", False, str(e))
                
        self.log_test("Frontend Routing Overall", passed == total, f"{passed}/{total} pages accessible")
        return passed == total
        
    def run_all_tests(self):
        """Run all frontend authentication flow tests"""
        print("Starting Frontend Authentication Flow Tests")
        print("=" * 60)
        
        tests = [
            ("Frontend Health", self.test_1_frontend_health),
            ("Landing Page", self.test_2_frontend_landing_page),
            ("Registration Page", self.test_3_registration_page),
            ("Login Page", self.test_4_login_page),
            ("OTP Login Page", self.test_5_otp_login_page),
            ("Backend API Connectivity", self.test_6_backend_api_connectivity),
            ("Registration Flow", self.test_7_registration_flow_simulation),
            ("Login Flow", self.test_8_login_flow_simulation),
            ("Session Management", self.test_9_session_management),
            ("Error Handling", self.test_10_error_handling),
            ("Logout Flow", self.test_11_logout_flow),
            ("Frontend Routing", self.test_12_frontend_routing),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Exception: {str(e)}")
                
        print("\n" + "=" * 60)
        print(f"Frontend Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("All frontend authentication flow tests passed!")
        else:
            print("Some frontend tests failed. Check the logs above.")
            
        return passed == total

def main():
    """Main test runner"""
    tester = FrontendAuthTester()
    success = tester.run_all_tests()
    
    # Save test results to file
    with open('frontend_auth_flow_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'frontend_url': FRONTEND_URL,
            'backend_url': BACKEND_URL,
            'results': tester.test_results,
            'success': success
        }, f, indent=2)
        
    print(f"\n📄 Frontend test results saved to: frontend_auth_flow_test_results.json")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 