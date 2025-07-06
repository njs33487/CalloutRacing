#!/usr/bin/env python3
"""
Check User model schema and database columns
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.db import connection
from core.models.auth import User

def check_user_schema():
    """Check the User model schema and database columns"""
    print("🔍 Checking User Model Schema")
    print("=" * 50)
    
    # Check model fields
    print("\n📋 User Model Fields:")
    for field in User._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")
        if hasattr(field, 'max_length'):
            print(f"    Max length: {field.max_length}")
        if hasattr(field, 'null'):
            print(f"    Nullable: {field.null}")
        if hasattr(field, 'blank'):
            print(f"    Blank: {field.blank}")
    
    # Check database columns
    print("\n🗄️ Database Columns:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'core_user'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        for column in columns:
            column_name, data_type, is_nullable, column_default = column
            print(f"  - {column_name}: {data_type}")
            print(f"    Nullable: {is_nullable}")
            if column_default:
                print(f"    Default: {column_default}")
    
    # Check if phone_number column exists
    phone_column_exists = any(col[0] == 'phone_number' for col in columns)
    print(f"\n📱 Phone Number Column Exists: {phone_column_exists}")
    
    if not phone_column_exists:
        print("❌ Phone number column is missing from database!")
        print("This suggests the User model changes haven't been migrated properly.")
    else:
        print("✅ Phone number column exists in database!")

if __name__ == "__main__":
    check_user_schema() 