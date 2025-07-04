#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def check_content_type_structure():
    """Check the actual structure of django_content_type table."""
    with connection.cursor() as cursor:
        # Get column information for django_content_type
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'django_content_type' 
            AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("django_content_type table structure:")
        for column in columns:
            print(f"  {column[0]}: {column[1]} (nullable: {column[2]}, default: {column[3]})")
        
        # Check if name column exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = 'django_content_type' 
                AND column_name = 'name'
                AND table_schema = 'public'
            )
        """)
        name_exists = cursor.fetchone()[0]
        print(f"\n'name' column exists: {name_exists}")

if __name__ == "__main__":
    check_content_type_structure() 