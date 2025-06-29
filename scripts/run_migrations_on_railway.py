#!/usr/bin/env python
"""
One-time script to run migrations on Railway
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line

def run_migrations():
    """Run all migrations"""
    print("=== Running migrations on Railway ===")
    
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
        print("=== Migrations completed successfully ===")
        
        # Show migration status
        execute_from_command_line(['manage.py', 'showmigrations'])
        
    except Exception as e:
        print(f"=== Migration failed: {e} ===")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_migrations() 