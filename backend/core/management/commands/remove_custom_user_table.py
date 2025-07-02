from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Remove custom user table after migration to Django built-in User model'

    def handle(self, *args, **options):
        self.stdout.write('Removing custom user table...')
        
        with connection.cursor() as cursor:
            # Check if custom user table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'core_user'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                self.stdout.write('Custom user table does not exist.')
                return
            
            # Drop the custom user table
            cursor.execute("DROP TABLE IF EXISTS core_user CASCADE")
            self.stdout.write('Dropped core_user table')
            
            # Drop related tables if they exist
            cursor.execute("DROP TABLE IF EXISTS core_user_groups CASCADE")
            cursor.execute("DROP TABLE IF EXISTS core_user_user_permissions CASCADE")
            self.stdout.write('Dropped related user tables')
        
        self.stdout.write(self.style.SUCCESS('Custom user table removal completed!'))  # type: ignore 