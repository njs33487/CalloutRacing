#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def fix_content_type_names():
    """Fix all NULL values in django_content_type name column."""
    
    with connection.cursor() as cursor:
        # First, let's see what records have NULL names
        cursor.execute("SELECT id, app_label, model, name FROM django_content_type WHERE name IS NULL")
        null_records = cursor.fetchall()
        
        print(f"Found {len(null_records)} records with NULL names:")
        for record in null_records:
            print(f"  ID {record[0]}: {record[1]}.{record[2]} -> {record[3]}")
        
        # Update all NULL names
        cursor.execute("UPDATE django_content_type SET name = CONCAT(app_label, '.', model) WHERE name IS NULL")
        updated_count = cursor.rowcount
        print(f"\nUpdated {updated_count} records")
        
        # Verify the fix
        cursor.execute("SELECT COUNT(*) FROM django_content_type WHERE name IS NULL")
        remaining_nulls = cursor.fetchone()[0]
        print(f"Remaining NULL values: {remaining_nulls}")

if __name__ == "__main__":
    fix_content_type_names() 