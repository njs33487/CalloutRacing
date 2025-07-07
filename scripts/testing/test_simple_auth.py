#!/usr/bin/env python3
"""
Simple Authentication Flow Test

This script tests the basic authentication functionality:
- User registration
- Login
- Session management
"""

import requests
import json
import time
import random
import string
from datetime import datetime

# Configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"

class SimpleAuthTester:
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
            'username': f'simple_test_{timestamp}_{random_suffix}',
            'email': f'simple_test_{timestamp}_{random_suffix}@example.com',
            'password': 'SimpleTest123!',
            'first_name': 'Simple',
            'last_name': 'Tester'
        }
        
    def test_1_backend_health(self):
        """Test if backend is responding"""
        try:
            response = self.session.get(f"{BASE_URL}/auth/csrf/")
            success = response.status_code == 200
            self.log_test("Backend Health Check", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Backend Health Check", False, str(e))
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
            
    def test_3_password_login(self):
        """Test password login"""
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
            
    def test_4_session_management(self):
        """Test session management"""
        if not hasattr(self, 'user_session'):
            self.log_test("Session Management", False, "No user session available")
            return False
            
        try:
            response = self.session.get(f"{BASE_URL}/auth/profile/")
            
            success = response.status_code == 200
            self.log_test("Profile Access", success, f"Status: {response.status_code}")
            
            if success:
                response_data = response.json()
                print(f"   User profile: {response_data.get('username', 'Unknown')}")
                
            return success
        except Exception as e:
            self.log_test("Session Management", False, str(e))
            return False
            
    def test_5_logout(self):
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
        """Run all simple authentication tests"""
        print("Starting Simple Authentication Flow Tests")
        print("=" * 50)
        
        tests = [
            ("Backend Health", self.test_1_backend_health),
            ("User Registration", self.test_2_user_registration),
            ("Password Login", self.test_3_password_login),
            ("Session Management", self.test_4_session_management),
            ("Logout", self.test_5_logout),
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
            print("All simple authentication tests passed!")
        else:
            print("Some tests failed. Check the logs above.")
            
        return passed == total

def main():
    """Main test runner"""
    tester = SimpleAuthTester()
    success = tester.run_all_tests()
    
    # Save test results to file
    with open('simple_auth_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'base_url': BASE_URL,
            'results': tester.test_results,
            'success': success
        }, f, indent=2)
        
    print(f"\nTest results saved to: simple_auth_test_results.json")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 