#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def fix_django_tables():
    """Fix Django system tables to match Django's expectations."""
    
    sql_commands = [
        # Add missing 'name' column to django_content_type
        "ALTER TABLE django_content_type ADD COLUMN IF NOT EXISTS name VARCHAR(100);",
        
        # Update existing records to have a default name
        "UPDATE django_content_type SET name = CONCAT(app_label, '.', model) WHERE name IS NULL;",
        
        # Make name column NOT NULL after updating
        "ALTER TABLE django_content_type ALTER COLUMN name SET NOT NULL;",
    ]
    
    with connection.cursor() as cursor:
        for i, sql in enumerate(sql_commands, 1):
            try:
                cursor.execute(sql)
                print(f"✓ Executed command {i}: {sql[:50]}...")
            except Exception as e:
                print(f"✗ Error in command {i}: {e}")
    
    print("\nDjango tables fixed! Now you can run migrations.")

if __name__ == "__main__":
    fix_django_tables() 