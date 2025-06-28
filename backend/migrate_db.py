#!/usr/bin/env python
"""
Standalone migration script for Railway deployment
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line

def run_migrations():
    """Run Django migrations"""
    print("=== Starting Database Migration ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
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
        sys.exit(1)

if __name__ == '__main__':
    run_migrations() 