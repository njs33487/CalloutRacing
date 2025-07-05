"""
Secure Secret Store for CalloutRacing

This module provides a secure way to store and access sensitive credentials
like API keys, database passwords, and other secrets.

IMPORTANT: Never commit actual secret values to version control.
Use environment variables or secure secret management services in production.
"""

import os
import base64
from cryptography.fernet import Fernet
from django.conf import settings
from decouple import config

class SecretStore:
    """Secure secret store for sensitive credentials."""
    
    def __init__(self):
        # In production, use a proper secret management service
        # For development, we'll use environment variables
        self._encryption_key = self._get_encryption_key()
        self._fernet = Fernet(self._encryption_key) if self._encryption_key else None
    
    def _get_encryption_key(self):
        """Get encryption key from environment or generate one."""
        key = config('ENCRYPTION_KEY', default=None)
        if not key:
            # Generate a new key for development
            key = Fernet.generate_key()
            print(f"⚠️  Generated new encryption key. Add to .env: ENCRYPTION_KEY={key.decode()}")
        return key if isinstance(key, bytes) else key.encode()
    
    def _encrypt(self, value: str) -> str:
        """Encrypt a string value."""
        if not self._fernet:
            return value
        return self._fernet.encrypt(value.encode()).decode()
    
    def _decrypt(self, encrypted_value: str) -> str:
        """Decrypt an encrypted string value."""
        if not self._fernet:
            return encrypted_value
        return self._fernet.decrypt(encrypted_value.encode()).decode()
    
    def get_stripe_secret_key(self) -> str:
        """Get Stripe secret key securely."""
        # For live keys, always use environment variables
        key = config('STRIPE_SECRET_KEY', default='')
        
        if not key:
            raise ValueError("STRIPE_SECRET_KEY not found in environment variables")
        
        # Validate key format
        if not key.startswith(('sk_test_', 'sk_live_')):
            raise ValueError("Invalid Stripe secret key format")
        
        return key
    
    def get_stripe_publishable_key(self) -> str:
        """Get Stripe publishable key."""
        return config('STRIPE_PUBLISHABLE_KEY', default='')
    
    def get_stripe_webhook_secret(self) -> str:
        """Get Stripe webhook secret."""
        return config('STRIPE_WEBHOOK_SECRET', default='')
    
    def get_database_password(self) -> str:
        """Get database password securely."""
        return config('DB_PASSWORD', default='')
    
    def get_email_password(self) -> str:
        """Get email password securely."""
        return config('EMAIL_HOST_PASSWORD', default='')
    
    def get_google_client_secret(self) -> str:
        """Get Google OAuth client secret."""
        return config('GOOGLE_CLIENT_SECRET', default='')
    
    def get_facebook_app_secret(self) -> str:
        """Get Facebook app secret."""
        return config('FACEBOOK_APP_SECRET', default='')
    
    def validate_secrets(self) -> dict:
        """Validate that all required secrets are present."""
        validation_results = {
            'stripe_secret_key': {
                'present': bool(self.get_stripe_secret_key()),
                'valid_format': False,
                'is_live': False
            },
            'stripe_publishable_key': {
                'present': bool(self.get_stripe_publishable_key()),
                'valid_format': False
            },
            'stripe_webhook_secret': {
                'present': bool(self.get_stripe_webhook_secret()),
                'valid_format': False
            },
            'database_password': {
                'present': bool(self.get_database_password())
            },
            'email_password': {
                'present': bool(self.get_email_password())
            }
        }
        
        # Validate Stripe secret key format
        try:
            secret_key = self.get_stripe_secret_key()
            validation_results['stripe_secret_key']['valid_format'] = True
            validation_results['stripe_secret_key']['is_live'] = secret_key.startswith('sk_live_')
        except ValueError:
            pass
        
        # Validate Stripe publishable key format
        pub_key = self.get_stripe_publishable_key()
        if pub_key.startswith(('pk_test_', 'pk_live_')):
            validation_results['stripe_publishable_key']['valid_format'] = True
        
        # Validate webhook secret format
        webhook_secret = self.get_stripe_webhook_secret()
        if webhook_secret.startswith('whsec_'):
            validation_results['stripe_webhook_secret']['valid_format'] = True
        
        return validation_results

# Global instance
secret_store = SecretStore()

def get_stripe_secret_key() -> str:
    """Get Stripe secret key safely."""
    return secret_store.get_stripe_secret_key()

def get_stripe_publishable_key() -> str:
    """Get Stripe publishable key safely."""
    return secret_store.get_stripe_publishable_key()

def get_stripe_webhook_secret() -> str:
    """Get Stripe webhook secret safely."""
    return secret_store.get_stripe_webhook_secret()

def validate_all_secrets() -> dict:
    """Validate all secrets and return results."""
    return secret_store.validate_secrets() 