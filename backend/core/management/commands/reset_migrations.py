from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Reset migration state and apply clean initial migration'

    def handle(self, *args, **options):
        self.stdout.write('Resetting migration state...')
        
        with connection.cursor() as cursor:
            # Delete all migration records from django_migrations
            cursor.execute("DELETE FROM django_migrations WHERE app = 'core'")
            self.stdout.write('Deleted existing core migration records')
        
        # Apply the initial migration
        self.stdout.write('Applying initial migration...')
        call_command('migrate', 'core', '0001', verbosity=1)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully reset migration state and applied initial migration')
        ) 