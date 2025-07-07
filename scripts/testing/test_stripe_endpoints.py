#!/usr/bin/env python3
"""
Test script for Stripe endpoints
"""
import requests
import json
import os
import sys
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient

User = get_user_model()

class StripeEndpointTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.client = APIClient()
        self.test_user = None
        self.session = requests.Session()
        self.csrf_token = None
        
    def setup_test_user(self):
        """Create a test user and get authentication token"""
        try:
            # Create test user
            self.test_user, created = User.objects.get_or_create(
                email="test@example.com",
                defaults={
                    'username': 'testuser123',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_active': True
                }
            )
            
            if created:
                self.test_user.set_password('testpass123')
                self.test_user.save()
                print(f"✅ Created test user: {self.test_user.email}")
            else:
                print(f"✅ Using existing test user: {self.test_user.email}")
            
            # Get CSRF token first
            csrf_response = self.session.get(f"{self.base_url}/api/auth/csrf/")
            if csrf_response.status_code == 200:
                self.csrf_token = csrf_response.cookies.get('csrftoken')
                print(f"✅ CSRF token obtained")
            else:
                print(f"⚠️ Could not get CSRF token: {csrf_response.status_code}")
            
            # Login using session authentication
            login_data = {
                'username': 'testuser123',
                'password': 'testpass123'
            }
            
            # Include CSRF token in headers and cookies
            headers = {'Content-Type': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                self.session.cookies.set('csrftoken', self.csrf_token)
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login/",
                json=login_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"✅ Session authentication successful")
            else:
                print(f"❌ Login failed: {response.text}")
                return False
            
        except Exception as e:
            print(f"❌ Error setting up test user: {e}")
            return False
        return True
    
    def test_subscription_plans(self):
        """Test subscription plans endpoint"""
        print("\n🔍 Testing Subscription Plans Endpoint")
        print("=" * 50)
        
        try:
            # Test without authentication
            response = requests.get(f"{self.base_url}/api/subscriptions/plans/")
            print(f"Without auth - Status: {response.status_code}")
            if response.status_code == 401:
                print("✅ Correctly requires authentication")
            else:
                print(f"Response: {response.text[:200]}")
            
            # Test with authentication
            response = self.session.get(f"{self.base_url}/api/subscriptions/plans/")
            print(f"With auth - Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Plans returned: {len(data)} plans")
                    for plan in data:
                        if isinstance(plan, dict):
                            print(f"  - {plan.get('name', 'Unknown')}: ${plan.get('price', 0)}")
                        else:
                            print(f"  - Plan: {plan}")
                except json.JSONDecodeError:
                    print(f"⚠️ Response is not JSON: {response.text[:200]}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing subscription plans: {e}")
    
    def test_create_checkout_session(self):
        """Test creating a checkout session"""
        print("\n🔍 Testing Create Checkout Session")
        print("=" * 50)
        
        try:
            data = {
                'price_id': 'price_test_123',
                'success_url': 'http://localhost:3000/success',
                'cancel_url': 'http://localhost:3000/cancel'
            }
            
            # Include CSRF token in headers and cookies
            headers = {'Content-Type': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                self.session.cookies.set('csrftoken', self.csrf_token)
            
            response = self.session.post(
                f"{self.base_url}/api/subscriptions/create-checkout-session/",
                json=data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Checkout session created")
                print(f"  - Session ID: {data.get('sessionId', 'N/A')[:20]}...")
                print(f"  - URL: {data.get('url', 'N/A')[:50]}...")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing checkout session: {str(e)}")
    
    def test_webhook_endpoint(self):
        """Test webhook endpoint"""
        print("\n🔍 Testing Webhook Endpoint")
        print("=" * 50)
        
        try:
            # Test webhook endpoint (should accept POST requests)
            test_payload = {
                'type': 'checkout.session.completed',
                'data': {
                    'object': {
                        'id': 'cs_test_123',
                        'customer': 'cus_test_123',
                        'subscription': 'sub_test_123'
                    }
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/subscriptions/stripe-webhook/",
                json=test_payload,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code in [200, 400, 422]:  # Acceptable responses
                print(f"✅ Webhook endpoint responding")
                print(f"  - Response: {response.text[:100]}...")
            else:
                print(f"❌ Unexpected status: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing webhook: {str(e)}")
    
    def test_marketplace_listings(self):
        """Test marketplace listings endpoint"""
        print("\n🔍 Testing Marketplace Listings")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{self.base_url}/api/marketplace-listings/")
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Marketplace listings returned: {len(data.get('results', []))} listings")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing marketplace listings: {str(e)}")
    
    def test_create_payment_intent(self):
        """Test creating a payment intent for marketplace"""
        print("\n🔍 Testing Create Payment Intent")
        print("=" * 50)
        
        try:
            # Include CSRF token in headers and cookies
            headers = {'Content-Type': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                self.session.cookies.set('csrftoken', self.csrf_token)
            
            # Note: This endpoint requires an item_id in the URL
            response = self.session.post(
                f"{self.base_url}/api/marketplace/items/1/create-payment-intent/",
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Payment intent created")
                client_secret = data.get('clientSecret', 'N/A')
                print(f"  - Client Secret: {client_secret[:10]}...{client_secret[-4:] if len(client_secret) > 14 else 'N/A'}")
                print(f"  - Amount: ${data.get('amount', 0)}")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing payment intent: {str(e)}")
    
    def test_customer_portal(self):
        """Test customer portal session creation"""
        print("\n🔍 Testing Customer Portal")
        print("=" * 50)
        
        try:
            data = {
                'return_url': 'http://localhost:3000/account'
            }
            
            # Include CSRF token in headers and cookies
            headers = {'Content-Type': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                self.session.cookies.set('csrftoken', self.csrf_token)
            
            response = self.session.post(
                f"{self.base_url}/api/subscriptions/create-portal-session/",
                json=data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Customer portal session created")
                url = data.get('url', 'N/A')
                print(f"  - URL: {url[:50]}...")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing customer portal: {str(e)}")
    
    def test_subscription_status(self):
        """Test subscription status endpoint"""
        print("\n🔍 Testing Subscription Status")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{self.base_url}/api/subscriptions/status/")
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Subscription status returned")
                print(f"  - Has subscription: {data.get('has_active_subscription', False)}")
                if data.get('subscription'):
                    print(f"  - Status: {data['subscription'].get('status', 'N/A')}")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing subscription status: {str(e)}")
    
    def test_connect_account_creation(self):
        """Test Stripe Connect account creation"""
        print("\n🔍 Testing Connect Account Creation")
        print("=" * 50)
        
        try:
            # Include CSRF token in headers and cookies
            headers = {'Content-Type': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                self.session.cookies.set('csrftoken', self.csrf_token)
            
            response = self.session.post(
                f"{self.base_url}/api/connect/create-account/",
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Connect account created")
                account_id = data.get('account_id', 'N/A')
                print(f"  - Account ID: {account_id[:10]}...{account_id[-4:] if len(account_id) > 14 else 'N/A'}")
            else:
                print(f"❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing connect account creation: {str(e)}")
    
    def run_all_tests(self):
        """Run all Stripe endpoint tests"""
        print("🚀 Starting Stripe Endpoint Tests")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {self.base_url}")
        
        # Setup test user
        if not self.setup_test_user():
            print("❌ Failed to setup test user. Exiting.")
            return
        
        # Run all tests
        self.test_subscription_plans()
        self.test_create_checkout_session()
        self.test_webhook_endpoint()
        self.test_marketplace_listings()
        self.test_create_payment_intent()
        self.test_customer_portal()
        self.test_subscription_status()
        self.test_connect_account_creation()
        
        print("\n" + "=" * 60)
        print("✅ Stripe endpoint testing completed!")
        print("Note: Some endpoints may fail if Stripe is not properly configured.")
        print("Check the responses above for details.")

if __name__ == "__main__":
    tester = StripeEndpointTester()
    tester.run_all_tests() 