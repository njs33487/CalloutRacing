# SSO (Single Sign-On) Setup Guide

This guide explains how to set up Google and Facebook SSO authentication for the CalloutRacing application.

## Overview

The application supports Single Sign-On (SSO) authentication through Google and Facebook, allowing users to sign in or create accounts using their existing social media accounts. This provides a seamless authentication experience and reduces friction during user registration.

## Features

- **Google SSO**: Users can sign in with their Google account
- **Facebook SSO**: Users can sign in with their Facebook account
- **Automatic Account Creation**: New users are automatically created when they first sign in via SSO
- **Seamless Integration**: SSO works alongside traditional email/password authentication
- **Secure Token Verification**: All SSO tokens are verified with the respective providers

## Backend Setup

### 1. Install Dependencies

The following packages are required for SSO functionality:

```bash
pip install django-allauth==0.60.1 requests==2.31.0
```

### 2. Environment Variables

Add the following environment variables to your `.env` file:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here

# Facebook OAuth Configuration
FACEBOOK_APP_ID=your_facebook_app_id_here
```

### 3. API Endpoints

The following SSO endpoints are available:

- `POST /api/auth/google/` - Google SSO authentication
- `POST /api/auth/facebook/` - Facebook SSO authentication
- `GET /api/auth/sso-config/` - Get SSO configuration for frontend

## Frontend Setup

### 1. SSO Components

The application includes a reusable `SSOButtons` component that handles both Google and Facebook authentication:

```tsx
import { SSOButtons } from '../components/SSOButtons'

<SSOButtons 
  onSuccess={() => navigate('/app')}
  onError={(error) => setError(error)}
  className="mb-6"
/>
```

### 2. Authentication Context

The `AuthContext` has been extended with SSO methods:

```tsx
const { googleLogin, facebookLogin } = useAuth()

// Google SSO
await googleLogin(idToken)

// Facebook SSO
await facebookLogin(accessToken)
```

## Google OAuth Setup

### 1. Create Google OAuth Application

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create an OAuth 2.0 Client ID
5. Set the application type to "Web application"
6. Add authorized JavaScript origins:
   - `http://localhost:3000` (for development)
   - `https://yourdomain.com` (for production)
7. Add authorized redirect URIs:
   - `http://localhost:3000` (for development)
   - `https://yourdomain.com` (for production)

### 2. Configure Environment Variables

Set your Google Client ID in the environment variables:

```env
GOOGLE_CLIENT_ID=your_google_client_id_here
```

### 3. Frontend Integration

The Google SSO integration uses the Google Identity Services library:

```javascript
// Google Identity Services is loaded dynamically
window.google.accounts.id.initialize({
  client_id: ssoConfig.google.client_id,
  callback: async (response) => {
    await googleLogin(response.credential)
  },
})
```

## Facebook OAuth Setup

### 1. Create Facebook Application

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or select an existing one
3. Add the Facebook Login product to your app
4. Configure the Facebook Login settings:
   - Add your domain to "Valid OAuth Redirect URIs"
   - Set the app domain
   - Configure privacy policy and terms of service URLs
5. Get your App ID from the app settings

### 2. Configure Environment Variables

Set your Facebook App ID in the environment variables:

```env
FACEBOOK_APP_ID=your_facebook_app_id_here
```

### 3. Frontend Integration

The Facebook SSO integration uses the Facebook JavaScript SDK:

```javascript
// Facebook SDK is loaded dynamically
window.FB.init({
  appId: ssoConfig.facebook.app_id,
  cookie: true,
  xfbml: true,
  version: 'v18.0'
})

window.FB.login(async (response) => {
  if (response.authResponse) {
    await facebookLogin(response.authResponse.accessToken)
  }
}, { scope: 'email,public_profile' })
```

## User Account Creation

When a user signs in via SSO for the first time:

1. The system verifies the SSO token with the provider
2. Extracts user information (email, name, etc.)
3. Checks if a user with that email already exists
4. If not, creates a new user account with:
   - Username derived from email (with uniqueness check)
   - Email from SSO provider
   - First and last name from SSO provider
   - No password (SSO users don't need passwords)
5. Creates a user profile
6. Generates an authentication token
7. Returns the token and user data to the frontend

## Security Considerations

### 1. Token Verification

All SSO tokens are verified with the respective providers:

- **Google**: Tokens are verified with Google's tokeninfo endpoint
- **Facebook**: Tokens are verified with Facebook's Graph API

### 2. Email Verification

SSO providers are trusted sources for email verification, so users signing in via SSO have verified email addresses.

### 3. Account Linking

The system uses email addresses to link SSO accounts to existing user accounts. If a user signs in with SSO using an email that already exists in the system, they will be logged into that existing account.

## Error Handling

The SSO implementation includes comprehensive error handling:

### Backend Errors

- Invalid tokens
- Missing required fields
- Network errors when verifying tokens
- User creation failures

### Frontend Errors

- SSO provider not configured
- User cancellation of SSO flow
- Network errors
- Authentication failures

## Testing

### Development Testing

1. Set up Google and Facebook OAuth applications with localhost origins
2. Configure environment variables with test credentials
3. Test SSO flow in development environment
4. Verify user account creation and authentication

### Production Testing

1. Update OAuth applications with production domains
2. Configure production environment variables
3. Test SSO flow in production environment
4. Verify user account linking and authentication

## Troubleshooting

### Common Issues

1. **"SSO is not configured"**: Check that environment variables are set correctly
2. **"Invalid token"**: Verify OAuth application configuration and token verification
3. **"Email not provided"**: Ensure the SSO provider is configured to request email permissions
4. **"User creation failed"**: Check database connectivity and user model configuration

### Debug Steps

1. Check browser console for JavaScript errors
2. Verify network requests in browser developer tools
3. Check backend logs for authentication errors
4. Verify environment variable configuration
5. Test SSO provider configuration independently

## Best Practices

1. **Always verify tokens**: Never trust client-side tokens without server-side verification
2. **Handle errors gracefully**: Provide clear error messages to users
3. **Secure environment variables**: Keep OAuth credentials secure and never commit them to version control
4. **Test thoroughly**: Test SSO flows in both development and production environments
5. **Monitor usage**: Track SSO usage and authentication success rates
6. **Plan for outages**: Have fallback authentication methods available

## Future Enhancements

Potential improvements to the SSO system:

1. **Additional providers**: Support for Apple, Twitter, GitHub, etc.
2. **Account linking**: Allow users to link multiple SSO accounts
3. **Profile completion**: Prompt new SSO users to complete their profile
4. **Advanced security**: Implement additional security measures like device verification
5. **Analytics**: Track SSO usage patterns and user behavior 