#!/usr/bin/env python3
"""
Debug subscription status endpoint
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models.payments import Subscription

User = get_user_model()

def debug_subscription_status():
    """Debug the subscription status endpoint"""
    print("🔍 Debugging Subscription Status")
    print("=" * 50)
    
    # Get test user
    user = User.objects.get(email="test@example.com")
    print(f"✅ Found test user: {user.username}")
    
    # Check if Subscription model exists
    try:
        subscription_count = Subscription.objects.count()
        print(f"✅ Subscription model exists, count: {subscription_count}")
        
        # Try to query subscriptions for the user
        user_subscriptions = Subscription.objects.filter(user=user)
        print(f"✅ User subscriptions query successful, count: {user_subscriptions.count()}")
        
        # Try to filter by status
        active_subscriptions = Subscription.objects.filter(
            user=user,
            status__in=['active', 'trialing']
        )
        print(f"✅ Active subscriptions query successful, count: {active_subscriptions.count()}")
        
        # Test the actual view logic
        subscription = Subscription.objects.filter(
            user=user,
            status__in=['active', 'trialing']
        ).first()
        
        if subscription:
            print(f"✅ Found active subscription: {subscription.id}")
            print(f"  - Status: {subscription.status}")
            print(f"  - Period end: {subscription.current_period_end}")
        else:
            print(f"✅ No active subscriptions found (this is expected)")
            
    except Exception as e:
        print(f"❌ Error with Subscription model: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_subscription_status() 