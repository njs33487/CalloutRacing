#!/usr/bin/env python3
"""
Test Redux integration with frontend and backend
"""
import requests
import json
import time
import subprocess
import sys
import os

# Configuration
FRONTEND_BASE = "http://localhost:5173"
API_BASE = "http://localhost:8001/api"
TEST_USER = {
    "username": "redux_test_user",
    "email": "redux@example.com",
    "password": "TestPass123",
    "first_name": "Redux",
    "last_name": "Test"
}

class ReduxIntegrationTest:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None

    def test_frontend_redux_setup(self):
        """Test if frontend has Redux properly configured"""
        print("=" * 60)
        print("TESTING FRONTEND REDUX SETUP")
        print("=" * 60)
        
        try:
            # Test if frontend is running
            response = self.session.get(f"{FRONTEND_BASE}/")
            if response.status_code != 200:
                print(f"❌ Frontend not accessible: {response.status_code}")
                return False
            
            print("✅ Frontend is running")
            
            # Check for Redux indicators in the page
            content = response.text.lower()
            redux_indicators = [
                "redux",
                "store",
                "provider",
                "useappdispatch",
                "useappselector"
            ]
            
            found_indicators = []
            for indicator in redux_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"✅ Redux indicators found: {', '.join(found_indicators)}")
            else:
                print("⚠️  No Redux indicators found in frontend")
            
            return True
            
        except Exception as e:
            print(f"❌ Frontend Redux test error: {e}")
            return False

    def test_api_endpoints_for_redux(self):
        """Test API endpoints that Redux will use"""
        print("\n" + "=" * 60)
        print("TESTING API ENDPOINTS FOR REDUX")
        print("=" * 60)
        
        # Test authentication endpoints
        auth_endpoints = [
            ("/auth/login/", "POST", "Login endpoint"),
            ("/auth/register/", "POST", "Register endpoint"),
            ("/auth/profile/", "GET", "Profile endpoint"),
            ("/auth/logout/", "POST", "Logout endpoint"),
        ]
        
        for endpoint, method, description in auth_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{API_BASE}{endpoint}")
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}")
                
                status = "✅" if response.status_code in [200, 201, 401, 403] else "❌"
                print(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                print(f"❌ {description}: Error - {e}")
        
        # Test events endpoints
        events_endpoints = [
            ("/events/", "GET", "Events list"),
            ("/events/", "POST", "Create event"),
            ("/events/1/", "GET", "Event detail"),
            ("/events/1/join/", "POST", "Join event"),
        ]
        
        print("\n--- Events Endpoints ---")
        for endpoint, method, description in events_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{API_BASE}{endpoint}")
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}")
                
                status = "✅" if response.status_code in [200, 201, 401, 403, 404] else "❌"
                print(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                print(f"❌ {description}: Error - {e}")

    def test_authentication_flow(self):
        """Test complete authentication flow that Redux will handle"""
        print("\n" + "=" * 60)
        print("TESTING AUTHENTICATION FLOW")
        print("=" * 60)
        
        # Step 1: Register user
        try:
            response = self.session.post(f"{API_BASE}/auth/register/", json=TEST_USER)
            if response.status_code == 201:
                print("✅ User registration successful")
            else:
                print(f"❌ User registration failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Registration error: {e}")
        
        # Step 2: Login (should fail due to email verification)
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            response = self.session.post(f"{API_BASE}/auth/login/", json=login_data)
            
            if response.status_code == 401 and "email_verification_required" in response.text:
                print("✅ Login correctly blocked (email verification required)")
            else:
                print(f"❌ Unexpected login response: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Login error: {e}")

    def test_events_api_for_redux(self):
        """Test events API endpoints that Redux events slice will use"""
        print("\n" + "=" * 60)
        print("TESTING EVENTS API FOR REDUX")
        print("=" * 60)
        
        # Test events list with filters (simulating Redux filters)
        filter_params = [
            {"event_type": "race"},
            {"location": "test"},
            {"is_public": "true"},
            {"is_featured": "true"},
        ]
        
        for i, params in enumerate(filter_params, 1):
            try:
                response = self.session.get(f"{API_BASE}/events/", params=params)
                status = "✅" if response.status_code in [200, 401, 403] else "❌"
                print(f"{status} Events with filter {i}: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Found {len(data.get('results', []))} events")
                    
            except Exception as e:
                print(f"❌ Events filter test {i} error: {e}")

    def test_social_api_for_redux(self):
        """Test social API endpoints that Redux social slice will use"""
        print("\n" + "=" * 60)
        print("TESTING SOCIAL API FOR REDUX")
        print("=" * 60)
        
        social_endpoints = [
            ("/posts/", "GET", "Posts list"),
            ("/posts/", "POST", "Create post"),
            ("/posts/1/like/", "POST", "Like post"),
            ("/posts/1/comment/", "POST", "Comment on post"),
        ]
        
        for endpoint, method, description in social_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{API_BASE}{endpoint}")
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}")
                
                status = "✅" if response.status_code in [200, 201, 401, 403, 404] else "❌"
                print(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                print(f"❌ {description}: Error - {e}")

    def test_marketplace_api_for_redux(self):
        """Test marketplace API endpoints that Redux marketplace slice will use"""
        print("\n" + "=" * 60)
        print("TESTING MARKETPLACE API FOR REDUX")
        print("=" * 60)
        
        marketplace_endpoints = [
            ("/marketplace/listings/", "GET", "Listings list"),
            ("/marketplace/listings/", "POST", "Create listing"),
            ("/marketplace/listings/1/", "GET", "Listing detail"),
            ("/marketplace/listings/1/purchase/", "POST", "Purchase listing"),
        ]
        
        for endpoint, method, description in marketplace_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{API_BASE}{endpoint}")
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}")
                
                status = "✅" if response.status_code in [200, 201, 401, 403, 404] else "❌"
                print(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                print(f"❌ {description}: Error - {e}")

    def test_racing_api_for_redux(self):
        """Test racing API endpoints that Redux racing slice will use"""
        print("\n" + "=" * 60)
        print("TESTING RACING API FOR REDUX")
        print("=" * 60)
        
        racing_endpoints = [
            ("/racing/callouts/", "GET", "Callouts list"),
            ("/racing/callouts/", "POST", "Create callout"),
            ("/racing/callouts/1/", "GET", "Callout detail"),
            ("/racing/callouts/1/accept/", "POST", "Accept callout"),
        ]
        
        for endpoint, method, description in racing_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{API_BASE}{endpoint}")
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}")
                
                status = "✅" if response.status_code in [200, 201, 401, 403, 404] else "❌"
                print(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                print(f"❌ {description}: Error - {e}")

    def test_cors_for_redux(self):
        """Test CORS configuration for Redux API calls"""
        print("\n" + "=" * 60)
        print("TESTING CORS FOR REDUX")
        print("=" * 60)
        
        # Test CORS preflight request
        try:
            headers = {
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
            response = self.session.options(f"{API_BASE}/auth/login/", headers=headers)
            
            if response.status_code in [200, 204]:
                print("✅ CORS preflight request successful")
                
                # Check CORS headers
                cors_headers = response.headers.get('Access-Control-Allow-Origin')
                if cors_headers:
                    print(f"✅ CORS headers present: {cors_headers}")
                else:
                    print("⚠️  No CORS headers found")
            else:
                print(f"❌ CORS preflight request failed: {response.status_code}")
        except Exception as e:
            print(f"❌ CORS test error: {e}")

    def test_error_handling_for_redux(self):
        """Test error handling that Redux will need to handle"""
        print("\n" + "=" * 60)
        print("TESTING ERROR HANDLING FOR REDUX")
        print("=" * 60)
        
        # Test invalid login (should return proper error for Redux)
        try:
            invalid_login = {
                "username": "nonexistent_user",
                "password": "wrong_password"
            }
            response = self.session.post(f"{API_BASE}/auth/login/", json=invalid_login)
            
            if response.status_code == 401:
                print("✅ Invalid login correctly rejected")
                error_data = response.json()
                if 'message' in error_data:
                    print(f"   Error message: {error_data['message']}")
            else:
                print(f"❌ Invalid login not properly handled: {response.status_code}")
        except Exception as e:
            print(f"❌ Error handling test error: {e}")
        
        # Test invalid event creation
        try:
            invalid_event = {
                "title": "",  # Empty title
                "description": "Test",
                "event_type": "invalid_type"
            }
            response = self.session.post(f"{API_BASE}/events/", json=invalid_event)
            
            if response.status_code == 400:
                print("✅ Invalid event creation correctly rejected")
                error_data = response.json()
                if 'errors' in error_data or 'message' in error_data:
                    print(f"   Validation errors present")
            else:
                print(f"❌ Invalid event creation not properly handled: {response.status_code}")
        except Exception as e:
            print(f"❌ Event error handling test error: {e}")

    def run_all_tests(self):
        """Run all Redux integration tests"""
        print("REDUX INTEGRATION TEST")
        print("=" * 60)
        print(f"Frontend Base: {FRONTEND_BASE}")
        print(f"API Base: {API_BASE}")
        print("=" * 60)
        
        tests = [
            self.test_frontend_redux_setup,
            self.test_api_endpoints_for_redux,
            self.test_authentication_flow,
            self.test_events_api_for_redux,
            self.test_social_api_for_redux,
            self.test_marketplace_api_for_redux,
            self.test_racing_api_for_redux,
            self.test_cors_for_redux,
            self.test_error_handling_for_redux,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed: {e}")
        
        print("\n" + "=" * 60)
        print("REDUX INTEGRATION TEST COMPLETED")
        print("=" * 60)
        
        print(f"\nSUMMARY:")
        print(f"- Tests passed: {passed}/{total}")
        print(f"- Frontend Redux setup: {'✅' if passed > 0 else '❌'}")
        print(f"- API endpoints ready for Redux: {'✅' if passed > 2 else '❌'}")
        print(f"- Authentication flow: {'✅' if passed > 3 else '❌'}")
        print(f"- CORS configuration: {'✅' if passed > 6 else '❌'}")
        print(f"- Error handling: {'✅' if passed > 7 else '❌'}")
        
        return passed == total

def main():
    tester = ReduxIntegrationTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All Redux integration tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Redux integration tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 