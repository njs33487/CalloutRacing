#!/usr/bin/env python3
"""
Helper script to set up environment variables for CalloutRacing backend.
This script will create a .env file from env.example and prompt for required values.
"""

import os
import getpass
from pathlib import Path
import re

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
    
    # Replace placeholders in content with environment variable references
    # This prevents storing sensitive data in clear text
    replacements = {
        'your-secret-key-here': '${DJANGO_SECRET_KEY:-' + secret_key + '}',
        'your-staff-email@example.com': '${STAFF_EMAIL:-' + staff_email + '}',
        'your-secure-password': '${STAFF_PASSWORD:-CHANGE_ME_IN_PRODUCTION}',
        'your-email@gmail.com': '${EMAIL_HOST_USER:-' + (email_host_user or '') + '}',
        'your-app-password': '${EMAIL_HOST_PASSWORD:-SET_VIA_ENVIRONMENT_VARIABLE}',
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    # Write .env file with environment variable references instead of clear text
    with open(env_file, 'w') as f:
        f.write(content)
    
    # Create a separate .env.local file for local development with actual values
    # This file should be in .gitignore
    local_env_file = Path('.env.local')
    if not local_env_file.exists():
        with open(local_env_file, 'w') as f:
            f.write(f"# Local development overrides\n")
            f.write(f"# This file should NOT be committed to version control\n")
            f.write(f"# WARNING: This file contains sensitive information\n")
            f.write(f"# Use environment variables in production instead\n")
            f.write(f"DJANGO_SECRET_KEY={secret_key}\n")
            f.write(f"STAFF_EMAIL={staff_email}\n")
            # Don't store password in clear text - use environment variable instead
            f.write(f"STAFF_PASSWORD=CHANGE_ME_IN_PRODUCTION\n")
            if email_host_user:
                f.write(f"EMAIL_HOST_USER={email_host_user}\n")
            # Don't store email password in clear text - use environment variable instead
            f.write(f"EMAIL_HOST_PASSWORD=SET_VIA_ENVIRONMENT_VARIABLE\n")
    
    print(f"\n✅ Environment file created: {env_file}")
    print(f"✅ Local overrides created: {local_env_file}")
    print("\nNext steps:")
    print("1. Review the .env file and update any other settings as needed")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py populate_sample_data")
    print("4. Run: python manage.py runserver")
    
    print(f"\n⚠️  Security reminder:")
    print("- Never commit the .env or .env.local files to version control")
    print("- Use strong passwords in production")
    print("- Keep your secret keys secure")
    print("- Set environment variables in production instead of using .env files")
    print("- The .env.local file contains actual values and should be kept private")
    print("- Passwords are NOT stored in clear text - set them via environment variables")
    print("- For production: Set STAFF_PASSWORD and EMAIL_HOST_PASSWORD as environment variables")
    
    # Security validation
    validate_security(env_file, local_env_file)

def validate_security(env_file, local_env_file):
    """Validate that no sensitive data is stored in clear text"""
    sensitive_patterns = [
        r'STAFF_PASSWORD=.*[^CHANGE_ME_IN_PRODUCTION]',
        r'EMAIL_HOST_PASSWORD=.*[^SET_VIA_ENVIRONMENT_VARIABLE]',
        r'DJANGO_SECRET_KEY=.*[^${DJANGO_SECRET_KEY]',
    ]
    
    files_to_check = [env_file, local_env_file]
    
    for file_path in files_to_check:
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
                for pattern in sensitive_patterns:
                    if re.search(pattern, content):
                        print(f"⚠️  WARNING: Potential sensitive data found in {file_path}")
                        print("   Please review the file and ensure no passwords are stored in clear text")

if __name__ == "__main__":
    main() 