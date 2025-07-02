from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from core.models import UserProfile


class Command(BaseCommand):
    help = 'Migrate from custom User model to Django built-in User model'

    def handle(self, *args, **options):
        self.stdout.write('Starting migration to Django built-in User model...')
        
        # Check if we have data to migrate
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM core_user")
            custom_user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            django_user_count = cursor.fetchone()[0]
        
        self.stdout.write(f'Found {custom_user_count} custom users and {django_user_count} Django users')
        
        if custom_user_count > 0:
            self.stdout.write('Migrating custom users to Django users...')
            self.migrate_users()
        
        # Update UserProfile foreign keys
        self.stdout.write('Updating UserProfile foreign keys...')
        self.update_user_profiles()
        
        self.stdout.write(self.style.SUCCESS('Migration completed successfully!'))  # type: ignore

    def migrate_users(self):
        """Migrate custom users to Django users"""
        with connection.cursor() as cursor:
            # Get all custom users
            cursor.execute("""
                SELECT id, username, email, first_name, last_name, password, 
                       is_staff, is_superuser, is_active, date_joined, last_login
                FROM core_user
            """)
            custom_users = cursor.fetchall()
            
            for user_data in custom_users:
                user_id, username, email, first_name, last_name, password, \
                is_staff, is_superuser, is_active, date_joined, last_login = user_data
                
                # Check if Django user already exists
                cursor.execute("SELECT id FROM auth_user WHERE username = %s OR email = %s", 
                             [username, email])
                existing_user = cursor.fetchone()
                
                if existing_user:
                    self.stdout.write(f'Django user already exists for {username}')
                    continue
                
                # Create Django user
                cursor.execute("""
                    INSERT INTO auth_user (username, email, first_name, last_name, password,
                                         is_staff, is_superuser, is_active, date_joined, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [username, email, first_name, last_name, password, is_staff, 
                     is_superuser, is_active, date_joined, last_login])
                
                self.stdout.write(f'Migrated user: {username}')

    def update_user_profiles(self):
        """Update UserProfile foreign keys to point to Django users"""
        with connection.cursor() as cursor:
            # Get all user profiles
            cursor.execute("SELECT id, user_id FROM core_userprofile")
            profiles = cursor.fetchall()
            
            for profile_id, old_user_id in profiles:
                # Find corresponding Django user
                cursor.execute("""
                    SELECT id FROM auth_user WHERE id = %s
                """, [old_user_id])
                django_user = cursor.fetchone()
                
                if django_user:
                    # Update the foreign key
                    cursor.execute("""
                        UPDATE core_userprofile SET user_id = %s WHERE id = %s
                    """, [django_user[0], profile_id])
                    self.stdout.write(f'Updated profile {profile_id} to Django user {django_user[0]}')
                else:
                    self.stdout.write(f'Warning: No Django user found for profile {profile_id}') 