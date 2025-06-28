# Email Verification System

This guide explains the email verification system implemented in the CalloutRacing application.

## Overview

The email verification system ensures that users provide valid email addresses during registration and helps maintain the integrity of the user base. Users must verify their email addresses before they can log in to the application.

## Features

- **Email Verification Required**: Users must verify their email before logging in
- **Automatic Email Sending**: Verification emails are sent automatically upon registration
- **Token-Based Verification**: Secure UUID tokens for email verification
- **Expiration Handling**: Verification tokens expire after 24 hours
- **Resend Functionality**: Users can request new verification emails
- **Welcome Emails**: Welcome emails sent after successful verification
- **Beautiful Email Templates**: Professional HTML and plain text email templates

## Backend Implementation

### Custom User Model

The application uses a custom User model that extends Django's AbstractUser:

```python
class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)
    email_verification_expires_at = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True)
```

### Email Service

The `core.email_service` module handles all email-related functionality:

- `send_email_verification(user)`: Sends verification email
- `send_welcome_email(user)`: Sends welcome email after verification
- `verify_email_token(token)`: Verifies email verification token
- `resend_verification_email(email)`: Resends verification email

### API Endpoints

- `POST /api/auth/register/`: User registration (sends verification email)
- `GET /api/auth/verify-email/<token>/`: Verify email with token
- `POST /api/auth/resend-verification/`: Resend verification email
- `POST /api/auth/login/`: Login (checks email verification)

### Email Templates

The system uses Django templates for emails:

- `templates/emails/email_verification.html`: HTML verification email
- `templates/emails/email_verification.txt`: Plain text verification email
- `templates/emails/welcome_email.html`: HTML welcome email
- `templates/emails/welcome_email.txt`: Plain text welcome email

## Frontend Implementation

### Email Verification Page

The `EmailVerification` component handles email verification:

- Displays verification status (loading, success, error)
- Handles expired tokens with resend functionality
- Provides clear user feedback
- Redirects to login after successful verification

### Updated Registration Flow

The registration process now:

1. Creates user account
2. Sends verification email
3. Shows success message with email verification instructions
4. Requires email verification before login

### Updated Login Flow

The login process now:

1. Checks if email is verified
2. Returns error if email not verified
3. Allows login only after email verification

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@calloutracing.com

# Frontend URL for email verification links
FRONTEND_URL=https://calloutracing.up.railway.app
```

### Gmail Setup

For Gmail SMTP:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

## User Experience

### Registration Flow

1. User fills out registration form
2. System creates account and sends verification email
3. User sees success message with verification instructions
4. User clicks verification link in email
5. Email is verified and welcome email is sent
6. User can now log in

### Login Flow

1. User attempts to log in
2. System checks if email is verified
3. If not verified, shows error message
4. If verified, allows login

### Email Verification Flow

1. User clicks verification link
2. System validates token
3. If valid, marks email as verified
4. Sends welcome email
5. Shows success message
6. Redirects to login

## Security Features

### Token Security

- UUID-based tokens for uniqueness
- 24-hour expiration for security
- One-time use tokens
- Rate limiting on resend requests

### Email Security

- Server-side token verification
- Secure email delivery
- Professional email templates
- Clear security messaging

## Error Handling

### Common Scenarios

1. **Expired Token**: User can request new verification email
2. **Invalid Token**: Clear error message with resend option
3. **Email Delivery Failure**: Graceful handling with user notification
4. **Rate Limiting**: Prevents spam with 5-minute cooldown

### User Feedback

- Clear success and error messages
- Loading states for all operations
- Helpful instructions for next steps
- Multiple recovery options

## Testing

### Development Testing

1. Use Django's console email backend for testing:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. Check console output for email content
3. Test verification flow with console tokens

### Production Testing

1. Configure production email settings
2. Test email delivery to real addresses
3. Verify email templates render correctly
4. Test token expiration and renewal

## Troubleshooting

### Common Issues

1. **Emails not sending**: Check SMTP configuration
2. **Verification links not working**: Verify FRONTEND_URL setting
3. **Tokens expiring too quickly**: Check timezone settings
4. **Email templates not rendering**: Verify template paths

### Debug Steps

1. Check Django logs for email errors
2. Verify environment variables
3. Test SMTP connection manually
4. Check email template syntax

## Best Practices

### Email Delivery

1. Use reliable SMTP provider (Gmail, SendGrid, etc.)
2. Monitor email delivery rates
3. Handle bounces and failures gracefully
4. Use professional email templates

### Security

1. Use secure tokens (UUID)
2. Implement rate limiting
3. Set appropriate expiration times
4. Validate all inputs

### User Experience

1. Clear messaging at each step
2. Multiple recovery options
3. Professional email design
4. Helpful error messages

## Future Enhancements

Potential improvements to the email verification system:

1. **Email Change Verification**: Verify new email addresses
2. **Bulk Email Operations**: Handle multiple verifications
3. **Advanced Templates**: Dynamic content based on user data
4. **Email Analytics**: Track open rates and click-through rates
5. **Alternative Verification**: SMS verification option
6. **Social Login Integration**: Skip verification for verified social accounts 