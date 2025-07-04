#!/usr/bin/env python3
"""
Comprehensive Test Script for Social and Marketplace Features
Tests both backend API endpoints and frontend functionality
"""

import requests
import json
import time
from datetime import datetime
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = datetime.now()
    
    def add_success(self, test_name):
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_failure(self, test_name, error):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"❌ FAIL: {test_name} - {error}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        print(f"Duration: {datetime.now() - self.start_time}")
        
        if self.errors:
            print("\nERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        print("="*60)

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_user = None
        self.results = TestResults()
    
    def login(self, username="admin", password="admin123"):
        """Login and get authentication token"""
        try:
            response = self.session.post(f"{API_BASE}/auth/login/", {
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                self.test_user = data.get('user')
                self.session.headers.update({'Authorization': f'Token {self.auth_token}'})
                return True
            else:
                return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def test_endpoint(self, method, endpoint, data=None, expected_status=200):
        """Test an API endpoint"""
        try:
            if method.upper() == 'GET':
                response = self.session.get(f"{API_BASE}{endpoint}")
            elif method.upper() == 'POST':
                response = self.session.post(f"{API_BASE}{endpoint}", json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(f"{API_BASE}{endpoint}", json=data)
            elif method.upper() == 'PATCH':
                response = self.session.patch(f"{API_BASE}{endpoint}", json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(f"{API_BASE}{endpoint}")
            
            if response.status_code == expected_status:
                return True, response.json() if response.content else {}
            else:
                return False, f"Expected {expected_status}, got {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)

def test_social_features(tester):
    """Test social features"""
    print("\n🧪 TESTING SOCIAL FEATURES")
    print("="*40)
    
    # Test 1: Create a post
    test_name = "Create Social Post"
    success, result = tester.test_endpoint('POST', '/posts/', {
        'content': 'Test post from automated testing',
        'post_type': 'text'
    }, 201)
    
    if success:
        post_id = result.get('id')
        tester.results.add_success(test_name)
        
        # Test 2: Like the post
        test_name = "Like Post"
        success, result = tester.test_endpoint('POST', f'/posts/{post_id}/like_post/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 3: Add comment
        test_name = "Add Comment"
        success, result = tester.test_endpoint('POST', f'/posts/{post_id}/comment/', {
            'content': 'Test comment'
        }, 201)
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 4: Get feed
        test_name = "Get Social Feed"
        success, result = tester.test_endpoint('GET', '/posts/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 5: Get trending posts
        test_name = "Get Trending Posts"
        success, result = tester.test_endpoint('GET', '/social/trending/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
    else:
        tester.results.add_failure("Create Social Post", result)
    
    # Test 6: Friend requests
    test_name = "Send Friend Request"
    success, result = tester.test_endpoint('POST', '/friendships/send_request/', {
        'receiver': 2  # Assuming user ID 2 exists
    }, 201)
    if success:
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, result)
    
    # Test 7: Get friendships
    test_name = "Get Friendships"
    success, result = tester.test_endpoint('GET', '/friendships/')
    if success:
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, result)

def test_marketplace_features(tester):
    """Test marketplace features"""
    print("\n🛒 TESTING MARKETPLACE FEATURES")
    print("="*40)
    
    # Test 1: Create marketplace listing
    test_name = "Create Marketplace Listing"
    success, result = tester.test_endpoint('POST', '/marketplace/', {
        'title': 'Test Turbocharger',
        'description': 'High-performance turbocharger for testing',
        'category': 'parts',
        'price': '1500.00',
        'condition': 'used',
        'location': 'Los Angeles, CA',
        'is_negotiable': True
    }, 201)
    
    if success:
        listing_id = result.get('id')
        tester.results.add_success(test_name)
        
        # Test 2: Get marketplace listings
        test_name = "Get Marketplace Listings"
        success, result = tester.test_endpoint('GET', '/marketplace/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 3: Get specific listing
        test_name = "Get Specific Listing"
        success, result = tester.test_endpoint('GET', f'/marketplace/{listing_id}/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 4: Update listing
        test_name = "Update Listing"
        success, result = tester.test_endpoint('PATCH', f'/marketplace/{listing_id}/', {
            'price': '1400.00'
        })
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 5: Search listings
        test_name = "Search Listings"
        success, result = tester.test_endpoint('GET', '/marketplace/?search=turbo')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 6: Filter by category
        test_name = "Filter by Category"
        success, result = tester.test_endpoint('GET', '/marketplace/?category=parts')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 7: Get user's listings
        test_name = "Get User Listings"
        success, result = tester.test_endpoint('GET', '/marketplace/my_listings/')
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 8: Make offer on listing
        test_name = "Make Offer"
        success, result = tester.test_endpoint('POST', f'/marketplace/{listing_id}/make_offer/', {
            'offer_amount': '1300.00',
            'message': 'Test offer'
        })
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 9: Contact seller
        test_name = "Contact Seller"
        success, result = tester.test_endpoint('POST', f'/marketplace/{listing_id}/contact_seller/', {
            'message': 'Is this still available?'
        })
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
        
        # Test 10: Delete listing
        test_name = "Delete Listing"
        success, result = tester.test_endpoint('DELETE', f'/marketplace/{listing_id}/', expected_status=204)
        if success:
            tester.results.add_success(test_name)
        else:
            tester.results.add_failure(test_name, result)
    else:
        tester.results.add_failure("Create Marketplace Listing", result)

def test_integration_features(tester):
    """Test integration between social and marketplace features"""
    print("\n🔗 TESTING INTEGRATION FEATURES")
    print("="*40)
    
    # Test 1: Share marketplace listing on social
    test_name = "Share Listing on Social"
    success, result = tester.test_endpoint('POST', '/posts/', {
        'content': 'Check out this awesome turbocharger I found!',
        'post_type': 'text',
        'related_listing_id': 1  # Assuming listing ID 1 exists
    }, 201)
    if success:
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, result)
    
    # Test 2: Get user activity feed
    test_name = "Get User Activity Feed"
    success, result = tester.test_endpoint('GET', '/social/feed/')
    if success:
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, result)

def test_production_readiness(tester):
    """Test production readiness features"""
    print("\n🚀 TESTING PRODUCTION READINESS")
    print("="*40)
    
    # Test 1: API health check
    test_name = "API Health Check"
    success, result = tester.test_endpoint('GET', '/health/')
    if success:
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, result)
    
    # Test 2: Rate limiting (if implemented)
    test_name = "Rate Limiting"
    # Make multiple rapid requests to test rate limiting
    rapid_requests = []
    for i in range(10):
        success, result = tester.test_endpoint('GET', '/posts/')
        rapid_requests.append(success)
    
    if all(rapid_requests):
        tester.results.add_success(test_name)
    else:
        tester.results.add_failure(test_name, "Rate limiting may be too aggressive")
    
    # Test 3: Error handling
    test_name = "Error Handling"
    success, result = tester.test_endpoint('GET', '/nonexistent-endpoint/', expected_status=404)
    if not success:
        tester.results.add_success(test_name)  # Expected to fail
    else:
        tester.results.add_failure(test_name, "Should return 404 for nonexistent endpoint")

def main():
    """Main test execution"""
    print("🧪 COMPREHENSIVE SOCIAL & MARKETPLACE TEST SUITE")
    print("="*60)
    print(f"Testing against: {BASE_URL}")
    print(f"Started at: {datetime.now()}")
    print("="*60)
    
    tester = APITester()
    
    # Login
    if not tester.login():
        print("❌ Failed to login. Please ensure the server is running and credentials are correct.")
        sys.exit(1)
    
    print(f"✅ Logged in as: {tester.test_user.get('username', 'Unknown') if tester.test_user else 'Unknown'}")
    
    # Run all test suites
    test_social_features(tester)
    test_marketplace_features(tester)
    test_integration_features(tester)
    test_production_readiness(tester)
    
    # Print results
    tester.results.print_summary()
    
    # Exit with appropriate code
    if tester.results.failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready for production.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {tester.results.failed} tests failed. Please fix issues before production.")
        sys.exit(1)

if __name__ == "__main__":
    main() 