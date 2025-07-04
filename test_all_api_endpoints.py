#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing for CalloutRacing
Tests all API endpoints systematically
"""
import requests
import json
import time

# Configuration
API_BASE = "http://127.0.0.1:8000/api"
BACKEND_BASE = "http://127.0.0.1:8000"

class APITester:
    def __init__(self):
        self.auth_token = None
        self.test_user = None
        self.test_results = []
        
    def log_result(self, endpoint, status, expected, response_text=""):
        """Log test result"""
        success = status == expected
        status_icon = "✅" if success else "❌"
        self.test_results.append({
            "endpoint": endpoint,
            "status": status,
            "expected": expected,
            "success": success,
            "response": response_text[:200] if response_text else ""
        })
        print(f"{status_icon} {endpoint}: {status} (expected: {expected})")
        if not success and response_text:
            print(f"   Response: {response_text[:100]}...")
    
    def test_public_endpoints(self):
        """Test all public endpoints that don't require authentication"""
        print("=" * 60)
        print("TESTING PUBLIC ENDPOINTS")
        print("=" * 60)
        
        public_endpoints = [
            (f"{BACKEND_BASE}/", "Root endpoint", 200),
            (f"{BACKEND_BASE}/health/", "Health check", 200),
            (f"{API_BASE}/", "API root", 403),  # Requires auth
            (f"{API_BASE}/auth/sso-config/", "SSO config", 200),
        ]
        
        for url, description, expected_status in public_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_authentication_endpoints(self):
        """Test authentication-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING AUTHENTICATION ENDPOINTS")
        print("=" * 60)
        
        # Test registration
        register_data = {
            "username": "api_test_user",
            "email": "api_test@example.com",
            "password": "TestPass123",
            "first_name": "API",
            "last_name": "Test"
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/register/", json=register_data)
            self.log_result("User Registration", response.status_code, 201, response.text)
            
            if response.status_code == 201:
                self.test_user = register_data["username"]
        except Exception as e:
            self.log_result("User Registration", f"ERROR: {str(e)}", 201)
        
        # Test login (should fail due to email verification)
        if self.test_user:
            login_data = {
                "username": self.test_user,
                "password": "TestPass123"
            }
            
            try:
                response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
                self.log_result("Login (unverified)", response.status_code, 401, response.text)
            except Exception as e:
                self.log_result("Login (unverified)", f"ERROR: {str(e)}", 401)
        
        # Test password reset request
        reset_data = {"email": "api_test@example.com"}
        try:
            response = requests.post(f"{API_BASE}/auth/request-password-reset/", json=reset_data)
            self.log_result("Password Reset Request", response.status_code, 200, response.text)
        except Exception as e:
            self.log_result("Password Reset Request", f"ERROR: {str(e)}", 200)
        
        # Test resend verification email
        resend_data = {"email": "api_test@example.com"}
        try:
            response = requests.post(f"{API_BASE}/auth/resend-verification/", json=resend_data)
            self.log_result("Resend Verification Email", response.status_code, 200, response.text)
        except Exception as e:
            self.log_result("Resend Verification Email", f"ERROR: {str(e)}", 200)
    
    def test_user_endpoints(self):
        """Test user-related endpoints (requires authentication)"""
        print("\n" + "=" * 60)
        print("TESTING USER ENDPOINTS (Requires Auth)")
        print("=" * 60)
        
        # Test without authentication
        user_endpoints = [
            (f"{API_BASE}/users/", "Users list", 403),
            (f"{API_BASE}/profiles/", "Profiles list", 403),
            (f"{API_BASE}/auth/profile/", "User profile", 403),
        ]
        
        for url, description, expected_status in user_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_racing_endpoints(self):
        """Test racing-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING RACING ENDPOINTS")
        print("=" * 60)
        
        racing_endpoints = [
            (f"{API_BASE}/racing/tracks/", "Tracks list", 403),
            (f"{API_BASE}/racing/callouts/", "Callouts list", 403),
            (f"{API_BASE}/racing/race-results/", "Race results", 403),
            (f"{API_BASE}/racing/search-users/", "Search users", 403),
            (f"{API_BASE}/racing/callout-stats/", "Callout stats", 403),
        ]
        
        for url, description, expected_status in racing_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_social_endpoints(self):
        """Test social-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING SOCIAL ENDPOINTS")
        print("=" * 60)
        
        social_endpoints = [
            (f"{API_BASE}/social/feed/", "Social feed", 403),
            (f"{API_BASE}/social/trending/", "Trending posts", 403),
            (f"{API_BASE}/social/posts/", "Posts", 403),
            (f"{API_BASE}/social/notifications/", "Notifications", 403),
        ]
        
        for url, description, expected_status in social_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_marketplace_endpoints(self):
        """Test marketplace-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING MARKETPLACE ENDPOINTS")
        print("=" * 60)
        
        marketplace_endpoints = [
            (f"{API_BASE}/marketplace/", "Marketplace list", 403),
        ]
        
        for url, description, expected_status in marketplace_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_hotspot_endpoints(self):
        """Test hotspot-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING HOTSPOT ENDPOINTS")
        print("=" * 60)
        
        hotspot_endpoints = [
            (f"{API_BASE}/hotspots/", "Hotspots list", 403),
        ]
        
        for url, description, expected_status in hotspot_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_event_endpoints(self):
        """Test event-related endpoints"""
        print("\n" + "=" * 60)
        print("TESTING EVENT ENDPOINTS")
        print("=" * 60)
        
        event_endpoints = [
            (f"{API_BASE}/events/", "Events list", 403),
        ]
        
        for url, description, expected_status in event_endpoints:
            try:
                response = requests.get(url, timeout=10)
                self.log_result(description, response.status_code, expected_status, response.text)
            except Exception as e:
                self.log_result(description, f"ERROR: {str(e)}", expected_status)
    
    def test_error_handling(self):
        """Test error handling for various scenarios"""
        print("\n" + "=" * 60)
        print("TESTING ERROR HANDLING")
        print("=" * 60)
        
        # Test invalid registration data
        invalid_register_data = {
            "username": "",  # Empty username
            "email": "invalid_email",  # Invalid email
            "password": "123"  # Weak password
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/register/", json=invalid_register_data)
            self.log_result("Invalid Registration", response.status_code, 400, response.text)
        except Exception as e:
            self.log_result("Invalid Registration", f"ERROR: {str(e)}", 400)
        
        # Test invalid login
        invalid_login_data = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/login/", json=invalid_login_data)
            self.log_result("Invalid Login", response.status_code, 401, response.text)
        except Exception as e:
            self.log_result("Invalid Login", f"ERROR: {str(e)}", 401)
        
        # Test missing fields
        missing_fields_data = {
            "username": "test"
            # Missing email and password
        }
        
        try:
            response = requests.post(f"{API_BASE}/auth/register/", json=missing_fields_data)
            self.log_result("Missing Fields", response.status_code, 400, response.text)
        except Exception as e:
            self.log_result("Missing Fields", f"ERROR: {str(e)}", 400)
    
    def test_cors_and_integration(self):
        """Test CORS and integration features"""
        print("\n" + "=" * 60)
        print("TESTING CORS AND INTEGRATION")
        print("=" * 60)
        
        # Test CORS preflight
        try:
            headers = {
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
            response = requests.options(f"{API_BASE}/auth/register/", headers=headers)
            self.log_result("CORS Preflight", response.status_code, 200, response.text)
        except Exception as e:
            self.log_result("CORS Preflight", f"ERROR: {str(e)}", 200)
        
        # Test CORS actual request
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
            self.log_result("CORS POST Request", response.status_code, 201, response.text)
        except Exception as e:
            self.log_result("CORS POST Request", f"ERROR: {str(e)}", 201)
    
    def generate_summary(self):
        """Generate a summary of all test results"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['endpoint']}: {result['status']} (expected: {result['expected']})")
        
        print("\n" + "=" * 60)
        print("API TESTING COMPLETED")
        print("=" * 60)
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0,
            "results": self.test_results
        }

def main():
    """Main test function"""
    print("COMPREHENSIVE API ENDPOINT TESTING")
    print("=" * 60)
    print(f"API Base: {API_BASE}")
    print(f"Backend Base: {BACKEND_BASE}")
    print("=" * 60)
    
    tester = APITester()
    
    # Run all test suites
    tester.test_public_endpoints()
    tester.test_authentication_endpoints()
    tester.test_user_endpoints()
    tester.test_racing_endpoints()
    tester.test_social_endpoints()
    tester.test_marketplace_endpoints()
    tester.test_hotspot_endpoints()
    tester.test_event_endpoints()
    tester.test_error_handling()
    tester.test_cors_and_integration()
    
    # Generate summary
    summary = tester.generate_summary()
    
    # Save results to file
    with open("api_test_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nResults saved to: api_test_results.json")
    
    if summary["success_rate"] >= 90:
        print("🎉 Excellent! API is working very well!")
    elif summary["success_rate"] >= 80:
        print("✅ Good! API is working well with minor issues.")
    elif summary["success_rate"] >= 70:
        print("⚠️ Fair! API has some issues that need attention.")
    else:
        print("❌ Poor! API has significant issues that need fixing.")

if __name__ == "__main__":
    main() 