#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def fix_content_type_final():
    """Final fix for django_content_type table."""
    
    with connection.cursor() as cursor:
        # Temporarily allow NULL values
        cursor.execute("ALTER TABLE django_content_type ALTER COLUMN name DROP NOT NULL")
        print("✓ Temporarily allowed NULL values in name column")
        
        # Update any existing NULL values
        cursor.execute("UPDATE django_content_type SET name = CONCAT(app_label, '.', model) WHERE name IS NULL")
        updated_count = cursor.rowcount
        print(f"✓ Updated {updated_count} NULL values")
        
        # Make name column NOT NULL again
        cursor.execute("ALTER TABLE django_content_type ALTER COLUMN name SET NOT NULL")
        print("✓ Made name column NOT NULL again")
        
        # Verify no NULL values remain
        cursor.execute("SELECT COUNT(*) FROM django_content_type WHERE name IS NULL")
        remaining_nulls = cursor.fetchone()[0]
        print(f"✓ Remaining NULL values: {remaining_nulls}")
        
        print("\nContent type table fixed! Now Django should work properly.")

if __name__ == "__main__":
    fix_content_type_final() 