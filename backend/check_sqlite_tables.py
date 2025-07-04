#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def check_sqlite_tables():
    """Check what tables exist in the SQLite database."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("Tables in SQLite database:")
        for table in tables:
            print(f"  {table[0]}")
        
        # Check specifically for core_user
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_user'")
        core_user_exists = cursor.fetchone() is not None
        print(f"\ncore_user table exists: {core_user_exists}")

if __name__ == "__main__":
    check_sqlite_tables() 