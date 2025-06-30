#!/usr/bin/env python3
"""
Helper script to set up environment variables for CalloutRacing backend.
This script will create a .env file from env.example and prompt for required values.
"""

import os
import getpass
from pathlib import Path

def main():
    print("CalloutRacing Backend Environment Setup")
    print("=" * 40)
    
    # Check if .env already exists
    env_file = Path('.env')
    if env_file.exists():
        response = input("A .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Read env.example
    example_file = Path('env.example')
    if not example_file.exists():
        print("Error: env.example file not found!")
        return
    
    with open(example_file, 'r') as f:
        content = f.read()
    
    # Get user input for required variables
    print("\nPlease provide the following information:")
    print("(Press Enter to use default values where available)\n")
    
    # Staff credentials - use environment variables or prompt securely
    staff_email = os.getenv('STAFF_EMAIL')
    if not staff_email:
        staff_email = input("Staff Email (for sample data): ").strip()
        if not staff_email:
            staff_email = "admin@calloutracing.com"
    
    staff_password = os.getenv('STAFF_PASSWORD')
    if not staff_password:
        staff_password = getpass.getpass("Staff Password (for sample data): ").strip()
        if not staff_password:
            print("Warning: No staff password provided. Please set STAFF_PASSWORD environment variable.")
            staff_password = "CHANGE_ME_IN_PRODUCTION"
    
    # Django settings
    secret_key = os.getenv('DJANGO_SECRET_KEY')
    if not secret_key:
        secret_key = input("Django Secret Key (leave empty to generate): ").strip()
        if not secret_key:
            import secrets
            secret_key = secrets.token_urlsafe(50)
            print("A new secret key has been successfully generated.")
    
    debug = os.getenv('DEBUG', 'True')
    if debug == 'True':
        debug_input = input("Debug mode (True/False) [True]: ").strip()
        if debug_input:
            debug = debug_input
    
    allowed_hosts = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    if allowed_hosts == 'localhost,127.0.0.1':
        allowed_hosts_input = input("Allowed Hosts (comma-separated) [localhost,127.0.0.1]: ").strip()
        if allowed_hosts_input:
            allowed_hosts = allowed_hosts_input
    
    # Email settings
    email_host_user = os.getenv('EMAIL_HOST_USER')
    if not email_host_user:
        email_host_user = input("Email Host User (for sending emails): ").strip()
    
    email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
    if not email_host_password:
        email_host_password = getpass.getpass("Email Host Password: ").strip()
    
    # Replace placeholders in content
    replacements = {
        'your-secret-key-here': secret_key,
        'your-staff-email@example.com': staff_email,
        'your-secure-password': staff_password,
        'your-email@gmail.com': email_host_user,
        'your-app-password': email_host_password,
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Environment file created: {env_file}")
    print("\nNext steps:")
    print("1. Review the .env file and update any other settings as needed")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py populate_sample_data")
    print("4. Run: python manage.py runserver")
    
    print(f"\n⚠️  Security reminder:")
    print("- Never commit the .env file to version control")
    print("- Use strong passwords in production")
    print("- Keep your secret keys secure")
    print("- Set STAFF_PASSWORD environment variable for production")

if __name__ == "__main__":
    main() 