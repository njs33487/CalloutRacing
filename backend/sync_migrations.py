#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def sync_migrations():
    """Sync Django migrations with the actual database state."""
    
    # First, let's check what migrations are recorded
    with connection.cursor() as cursor:
        cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, id")
        recorded_migrations = cursor.fetchall()
        
        print("Currently recorded migrations:")
        for app, name in recorded_migrations:
            print(f"  {app}: {name}")
    
    # Mark all migrations as applied without running them
    print("\nMarking all migrations as applied...")
    
    # Get all migration files
    from django.db.migrations.loader import MigrationLoader
    from django.db import connections
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.writer import MigrationWriter
    
    # Create a list of all apps and their migrations
    apps = ['admin', 'auth', 'authtoken', 'contenttypes', 'core', 'sessions']
    
    for app in apps:
        try:
            # Mark all migrations for this app as applied
            execute_from_command_line(['manage.py', 'migrate', app, '--fake'])
            print(f"Marked {app} migrations as applied")
        except Exception as e:
            print(f"Error with {app}: {e}")
    
    print("\nMigration sync complete!")

if __name__ == "__main__":
    sync_migrations() 