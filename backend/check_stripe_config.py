#!/usr/bin/env python3
"""
Check Stripe configuration
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.conf import settings

def check_stripe_config():
    """Check Stripe configuration"""
    print("🔍 Checking Stripe Configuration")
    print("=" * 50)
    
    # Check environment variables
    stripe_key_env = os.environ.get('STRIPE_SECRET_KEY')
    print(f"Environment STRIPE_SECRET_KEY: {'✅ Set' if stripe_key_env else '❌ Not set'}")
    if stripe_key_env:
        print(f"  - Length: {len(stripe_key_env)} characters")
    
    # Check Django settings
    stripe_key_settings = getattr(settings, 'STRIPE_SECRET_KEY', None)
    print(f"Django settings STRIPE_SECRET_KEY: {'✅ Set' if stripe_key_settings else '❌ Not set'}")
    if stripe_key_settings:
        print(f"  - Length: {len(stripe_key_settings)} characters")
    
    # Check if it's the dummy key
    if stripe_key_settings and 'sk_test_' in stripe_key_settings:
        print("✅ Valid Stripe test key detected")
    elif stripe_key_settings and 'sk_live_' in stripe_key_settings:
        print("✅ Valid Stripe live key detected")
    elif stripe_key_settings:
        print("⚠️ Stripe key format unknown")
    else:
        print("❌ No valid Stripe key found")
    
    # Check other Stripe settings
    print(f"\nOther Stripe Settings:")
    print(f"  - STRIPE_PUBLISHABLE_KEY: {'✅ Set' if getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None) else '❌ Not set'}")
    print(f"  - STRIPE_WEBHOOK_SECRET: {'✅ Set' if getattr(settings, 'STRIPE_WEBHOOK_SECRET', None) else '❌ Not set'}")
    print(f"  - FRONTEND_URL: {getattr(settings, 'FRONTEND_URL', '❌ Not set')}")

if __name__ == "__main__":
    check_stripe_config() 