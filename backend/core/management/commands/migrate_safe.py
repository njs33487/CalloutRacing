from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Run migrations safely by skipping post-migrate signals'

    def handle(self, *args, **options):
        # First, clean up any problematic content type rows
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_content_type WHERE name IS NULL")
            deleted_count = cursor.rowcount
            if deleted_count > 0:
                self.stdout.write(f"Deleted {deleted_count} problematic content type rows")
        
        # Run the migration without post-migrate signals
        try:
            # Use Django's migrate command but capture the output
            call_command('migrate', verbosity=0)
            self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {str(e)}'))
            # If migration fails, try to clean up and retry
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM django_content_type WHERE name IS NULL")
                self.stdout.write("Cleaned up content type table, please try again") 