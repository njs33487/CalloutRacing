"""
Django management command to validate and test secrets.

Usage:
    python manage.py validate_secrets
"""

from django.core.management.base import BaseCommand
from core.secret_store import validate_all_secrets, get_stripe_secret_key
import stripe

class Command(BaseCommand):
    help = 'Validate and test all configured secrets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-stripe',
            action='store_true',
            help='Test Stripe API connectivity',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔐 Validating secrets...'))
        
        # Validate all secrets
        validation_results = validate_all_secrets()
        
        # Display results
        for secret_name, result in validation_results.items():
            status = '✅' if result.get('present', False) else '❌'
            self.stdout.write(f"{status} {secret_name}:")
            
            for key, value in result.items():
                if key == 'present':
                    continue
                self.stdout.write(f"   {key}: {value}")
        
        # Test Stripe connectivity if requested
        if options['test_stripe']:
            self.stdout.write(self.style.SUCCESS('\n🧪 Testing Stripe API connectivity...'))
            try:
                # Test with a simple API call
                stripe.api_key = get_stripe_secret_key()
                account = stripe.Account.retrieve()
                self.stdout.write(self.style.SUCCESS(f"✅ Stripe API connected successfully"))
                self.stdout.write(f"   Account ID: {account.id}")
                self.stdout.write(f"   Account Type: {account.type}")
                
                # Check if using live keys
                if get_stripe_secret_key().startswith('sk_live_'):
                    self.stdout.write(self.style.WARNING("⚠️  Using LIVE Stripe keys - be careful!"))
                else:
                    self.stdout.write(self.style.SUCCESS("✅ Using TEST Stripe keys"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Stripe API test failed: {str(e)}"))
        
        # Summary
        total_secrets = len(validation_results)
        present_secrets = sum(1 for result in validation_results.values() if result.get('present', False))
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary: {present_secrets}/{total_secrets} secrets configured'))
        
        if present_secrets == total_secrets:
            self.stdout.write(self.style.SUCCESS('🎉 All secrets are properly configured!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Some secrets are missing. Check your .env file.')) 