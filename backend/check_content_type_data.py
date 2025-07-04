#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection

def check_content_type_data():
    """Check the actual data in django_content_type table."""
    
    with connection.cursor() as cursor:
        # Get all records
        cursor.execute("SELECT id, app_label, model, name FROM django_content_type ORDER BY id")
        records = cursor.fetchall()
        
        print("All django_content_type records:")
        for record in records:
            print(f"  ID {record[0]}: {record[1]}.{record[2]} -> name: '{record[3]}'")
        
        # Check for NULL or empty names
        cursor.execute("SELECT id, app_label, model, name FROM django_content_type WHERE name IS NULL OR name = ''")
        null_records = cursor.fetchall()
        
        print(f"\nRecords with NULL or empty names: {len(null_records)}")
        for record in null_records:
            print(f"  ID {record[0]}: {record[1]}.{record[2]} -> name: '{record[3]}'")

if __name__ == "__main__":
    check_content_type_data() 