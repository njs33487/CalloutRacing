# SSO (Single Sign-On) Setup Guide

This guide will help you set up Google and Facebook SSO for your CalloutRacing application.

## Prerequisites

- A Google Cloud Platform account
- A Facebook Developer account
- Access to your application's environment variables

## Google SSO Setup

### 1. Create Google OAuth 2.0 Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application" as the application type
   - Add your domain to "Authorized JavaScript origins":
     - `http://localhost:5173` (for development)
     - `https://yourdomain.com` (for production)
   - Add your domain to "Authorized redirect URIs":
     - `http://localhost:5173` (for development)
     - `https://yourdomain.com` (for production)
5. Copy the Client ID

### 2. Configure Environment Variables

Add the following to your `.env` file or environment variables:

```bash
GOOGLE_CLIENT_ID=your-google-client-id-here
```

## Facebook SSO Setup

### 1. Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "Create App"
3. Choose "Consumer" as the app type
4. Fill in the app details and create the app
5. Go to "Settings" > "Basic" and copy the App ID
6. Go to "Facebook Login" > "Settings"
7. Add your domain to "Valid OAuth Redirect URIs":
   - `http://localhost:5173` (for development)
   - `https://yourdomain.com` (for production)

### 2. Configure Environment Variables

Add the following to your `.env` file or environment variables:

```bash
FACEBOOK_APP_ID=your-facebook-app-id-here
```

## Environment Variables

For the backend, add these to your `.env` file:

```bash
# SSO Configuration
GOOGLE_CLIENT_ID=your-google-client-id-here
FACEBOOK_APP_ID=your-facebook-app-id-here
```

## Testing SSO

1. Start your backend server
2. Start your frontend development server
3. Go to the login or signup page
4. You should see "Continue with Google" and "Continue with Facebook" buttons
5. Click on either button to test the SSO flow

## Troubleshooting

### SSO Buttons Not Showing

1. Check that the environment variables are set correctly
2. Verify that the SSO configuration endpoint is working:
   ```bash
   curl http://localhost:8000/api/auth/sso-config/
   ```
3. Check the browser console for any errors
4. Ensure CORS is properly configured

### SSO Login Failing

1. Verify that your OAuth credentials are correct
2. Check that your domain is added to the authorized origins
3. Ensure the redirect URIs are configured correctly
4. Check the backend logs for any authentication errors

### Common Issues

1. **CORS Errors**: Make sure your frontend domain is in the CORS allowed origins
2. **Invalid Token**: Verify that your OAuth credentials are correct
3. **Redirect Issues**: Ensure redirect URIs match exactly (including protocol and port)

## Security Considerations

1. Never commit OAuth credentials to version control
2. Use environment variables for all sensitive configuration
3. Regularly rotate your OAuth credentials
4. Monitor your OAuth usage and set up alerts for unusual activity
5. Implement proper error handling for SSO failures

## Production Deployment

When deploying to production:

1. Update your OAuth app settings with the production domain
2. Set the environment variables in your production environment
3. Ensure HTTPS is enabled (required for OAuth)
4. Test the SSO flow in the production environment
5. Monitor logs for any SSO-related issues

## Support

If you encounter issues with SSO setup:

1. Check the browser console for JavaScript errors
2. Check the backend logs for authentication errors
3. Verify your OAuth app configuration
4. Test with a simple OAuth flow first
5. Consult the Google and Facebook developer documentation 