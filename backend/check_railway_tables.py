#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def check_railway_tables():
    """Check what tables exist in the Railway PostgreSQL database."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print("Tables in Railway PostgreSQL database:")
        for table in tables:
            print(f"  {table[0]}")
        
        # Check specifically for core_user
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'core_user'
            )
        """)
        core_user_exists = cursor.fetchone()[0]
        print(f"\ncore_user table exists: {core_user_exists}")
        
        # Check for django_migrations table
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            )
        """)
        migrations_exists = cursor.fetchone()[0]
        print(f"django_migrations table exists: {migrations_exists}")

if __name__ == "__main__":
    check_railway_tables() 