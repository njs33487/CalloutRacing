#!/usr/bin/env python
"""
Database diagnostic script for Railway
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')

# Initialize Django
django.setup()

from django.db import connection
from django.conf import settings

def diagnose_database():
    """Diagnose database connection and table issues"""
    print("=== Database Diagnostic ===")
    
    # Check database settings
    print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"Database name: {settings.DATABASES['default'].get('NAME', 'Not specified')}")
    print(f"Database host: {settings.DATABASES['default'].get('HOST', 'Not specified')}")
    print(f"Database port: {settings.DATABASES['default'].get('PORT', 'Not specified')}")
    
    try:
        with connection.cursor() as cursor:
            # Check if we can connect
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL version: {version[0]}")
            
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
            
            if table_exists:
                # Check table structure
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_user' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f"core_user table columns: {[col[0] for col in columns]}")
                
                # Check if there are any users
                cursor.execute("SELECT COUNT(*) FROM core_user;")
                user_count = cursor.fetchone()[0]
                print(f"Number of users in core_user: {user_count}")
            
            # List all tables in the database
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'core_%'
                ORDER BY table_name;
            """)
            core_tables = cursor.fetchall()
            print(f"Core tables in database: {[table[0] for table in core_tables]}")
            
    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_database() 