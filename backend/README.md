# CalloutRacing Backend

Django REST API backend for the CalloutRacing drag racing social network.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. **Option A: Use the setup script (recommended)**
   ```bash
   python setup_env.py
   ```
   This will guide you through setting up your environment variables interactively.

   **Option B: Manual setup**
   - Copy `env.example` to `.env` and configure your environment variables
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

## Environment Variables

Copy `env.example` to `.env` and configure the following variables:

### Required
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to True for development
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Staff Credentials (for sample data)
- `STAFF_EMAIL`: Email for the admin user created by sample data
- `STAFF_PASSWORD`: Password for the admin user

### Email Configuration
- `EMAIL_HOST_USER`: Your email address
- `EMAIL_HOST_PASSWORD`: Your email app password

### Optional
- `DATABASE_URL`: Database connection string
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_SECRET_KEY`: Stripe secret key

## Sample Data

To populate the database with sample data:

1. Set up your environment variables (especially `STAFF_EMAIL` and `STAFF_PASSWORD`)
2. Run: `python manage.py populate_sample_data`

This will create:
- Staff admin user (using environment variables)
- Sample tracks across the US
- Sample users with racing profiles
- Sample events and callouts
- Sample hotspots and marketplace listings

## API Documentation

The API documentation is available at `/swagger/` when running the development server.

## Development

- Run tests: `python manage.py test`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Reset database: `python manage.py reset_db`

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for staff credentials
- Keep your secret keys secure
- Use environment variables for all sensitive configuration 