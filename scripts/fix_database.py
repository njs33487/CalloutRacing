#!/usr/bin/env python
"""
Database fix script for Railway deployment
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def check_database():
    """Check database status and fix if needed"""
    print("=== Database Status Check ===")
    
    try:
        with connection.cursor() as cursor:
            # Check if core_user table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'core_user'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            print(f"core_user table exists: {table_exists}")
            
            if not table_exists:
                print("=== Table missing, running migrations ===")
                # Run makemigrations
                execute_from_command_line(['manage.py', 'makemigrations', '--noinput'])
                
                # Run migrate
                execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
                
                # Check again
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'core_user'
                    );
                """)
                table_exists_after = cursor.fetchone()[0]
                print(f"core_user table exists after migration: {table_exists_after}")
            else:
                print("=== Table exists, checking migration status ===")
                execute_from_command_line(['manage.py', 'showmigrations'])
                
    except Exception as e:
        print(f"=== Database check failed: {e} ===")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_database() 