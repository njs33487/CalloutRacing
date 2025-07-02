#!/usr/bin/env python
import os
import sys
import django
import subprocess
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append('backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

def deploy_to_production():
    """Deploy to production database with migrations and data population"""
    print("🚀 Starting production deployment...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path('backend')
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return
    
    os.chdir(backend_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    try:
        # Step 1: Make migrations
        print("\n📝 Step 1: Creating migrations...")
        result = subprocess.run(['python', 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations created successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print("⚠️  Migration creation output:")
            print(result.stdout)
            print(result.stderr)
        
        # Step 2: Run migrations
        print("\n🔄 Step 2: Running migrations...")
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Migration failed!")
            print(result.stdout)
            print(result.stderr)
            return
        
        # Step 3: Run the migration commands for User model
        print("\n👥 Step 3: Migrating custom User model...")
        result = subprocess.run(['python', 'manage.py', 'migrate_to_django_user'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ User migration completed")
            if result.stdout:
                print(result.stdout)
        else:
            print("⚠️  User migration output:")
            print(result.stdout)
            print(result.stderr)
        
        # Step 4: Remove custom user table
        print("\n🗑️  Step 4: Removing custom user table...")
        result = subprocess.run(['python', 'manage.py', 'remove_custom_user_table'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Custom user table removed")
            if result.stdout:
                print(result.stdout)
        else:
            print("⚠️  Table removal output:")
            print(result.stdout)
            print(result.stderr)
        
        # Step 5: Populate data
        print("\n📊 Step 5: Populating production data...")
        os.chdir('..')  # Go back to root directory
        result = subprocess.run(['python', 'populate_production_data.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Data population completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Data population failed!")
            print(result.stdout)
            print(result.stderr)
            return
        
        print("\n" + "=" * 50)
        print("🎉 PRODUCTION DEPLOYMENT COMPLETE! 🎉")
        print("=" * 50)
        print("✅ Migrations created and applied")
        print("✅ User model migrated to Django built-in")
        print("✅ Custom user table removed")
        print("✅ Production data populated")
        print("\n🔗 Your production database is ready!")
        print("🌐 Frontend: https://calloutracing.up.railway.app")
        print("🔧 Backend: https://calloutracing-backend-production.up.railway.app")
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        return

if __name__ == "__main__":
    deploy_to_production() 