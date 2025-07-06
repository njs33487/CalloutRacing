# OTP Authentication Deployment Guide

This guide covers deploying phone/email OTP authentication in production for CalloutRacing.

## 🚀 Overview

The OTP system supports:
- **Phone OTP**: SMS via Twilio, AWS SNS, or Vonage
- **Email OTP**: Email via SMTP (Gmail, SendGrid, etc.)
- **Frontend Integration**: React/Redux with TypeScript
- **Backend**: Django with REST API

## 📋 Prerequisites

### Backend Requirements
- Django 4.x+
- PostgreSQL database
- Redis (optional, for OTP caching)
- SMTP email service
- SMS service (Twilio recommended)

### Frontend Requirements
- React 18+
- Redux Toolkit
- TypeScript
- Tailwind CSS

## 🔧 Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install twilio  # For SMS
pip install boto3   # For AWS SNS (alternative)
pip install vonage  # For Vonage SMS (alternative)
```

### 2. Environment Variables

Add to your production environment:

```bash
# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_FROM_NUMBER=+1234567890

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@calloutracing.com

# OTP Settings
OTP_EXPIRY_MINUTES=10
OTP_LENGTH=6

# Alternative SMS providers (optional)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
VONAGE_API_KEY=your-vonage-api-key
VONAGE_API_SECRET=your-vonage-api-secret
```

### 3. Database Migration

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Test User

```python
# In Django shell
python manage.py shell

from core.models import User
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    phone_number='+12345678901',
    password='testpass123'
)
```

## 📱 SMS Provider Setup

### Option 1: Twilio (Recommended)

1. **Sign up**: [twilio.com](https://www.twilio.com)
2. **Get credentials**: Account SID, Auth Token
3. **Get phone number**: Purchase a number for sending SMS
4. **Configure environment variables** (see above)

### Option 2: AWS SNS

1. **AWS Account**: Set up AWS account
2. **IAM User**: Create user with SNS permissions
3. **Configure credentials** in environment variables

### Option 3: Vonage (Nexmo)

1. **Sign up**: [vonage.com](https://www.vonage.com)
2. **Get API credentials**
3. **Configure environment variables**

## 📧 Email Setup

### Gmail (Recommended for Development)

1. **Enable 2FA** on your Gmail account
2. **Generate App Password**: Google Account → Security → App Passwords
3. **Use App Password** instead of regular password

### SendGrid (Recommended for Production)

1. **Sign up**: [sendgrid.com](https://www.sendgrid.com)
2. **Verify domain** or use single sender verification
3. **Get API key**
4. **Update settings**:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

## 🎯 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

Create `.env` file:

```bash
VITE_API_URL=https://your-backend-domain.com/api
```

### 3. Build for Production

```bash
npm run build
```

## 🧪 Testing

### 1. Backend Testing

```bash
cd backend
python scripts/testing/test_otp_auth.py
```

### 2. Manual Testing

1. **Start backend**: `python manage.py runserver`
2. **Start frontend**: `npm run dev`
3. **Navigate to**: `http://localhost:5173/otp-login`
4. **Test flow**:
   - Enter phone/email
   - Check console for OTP code
   - Enter OTP code
   - Verify login success

### 3. API Testing

```bash
# Send OTP
curl -X POST http://localhost:8000/api/auth/otp/send/ \
  -H "Content-Type: application/json" \
  -d '{"identifier": "+12345678901", "type": "phone"}'

# Verify OTP (replace with actual code from logs)
curl -X POST http://localhost:8000/api/auth/otp/verify/ \
  -H "Content-Type: application/json" \
  -d '{"identifier": "+12345678901", "otp_code": "123456", "type": "phone"}'
```

## 🚀 Production Deployment

### 1. Railway Deployment

```bash
# Backend
cd backend
railway login
railway link
railway up

# Frontend
cd frontend
railway login
railway link
railway up
```

### 2. Environment Variables in Railway

Set all environment variables in Railway dashboard:
- Go to your project
- Click "Variables" tab
- Add all required environment variables

### 3. Database Migration

```bash
railway run python manage.py migrate
```

### 4. Create Superuser

```bash
railway run python manage.py createsuperuser
```

## 🔒 Security Considerations

### 1. Rate Limiting

Add rate limiting to prevent abuse:

```python
# In Django settings
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',
        'user': '10/minute'
    }
}
```

### 2. OTP Expiration

OTPs expire after 10 minutes by default. Adjust in settings:

```python
OTP_EXPIRY_MINUTES = 10
```

### 3. HTTPS Only

Ensure all production traffic uses HTTPS:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Monitoring

### 1. Logging

Monitor OTP failures:

```python
# In otp_service.py
logger.info(f"OTP sent to {identifier}")
logger.error(f"Failed to send OTP: {error}")
```

### 2. Analytics

Track OTP usage:
- Success/failure rates
- Most used methods (phone vs email)
- Peak usage times

## 🐛 Troubleshooting

### Common Issues

1. **SMS not sending**:
   - Check Twilio credentials
   - Verify phone number format
   - Check account balance

2. **Email not sending**:
   - Verify SMTP settings
   - Check app password (Gmail)
   - Test with simple email first

3. **Frontend not connecting**:
   - Check CORS settings
   - Verify API URL
   - Check network tab for errors

4. **OTP verification failing**:
   - Check database for OTP records
   - Verify OTP expiration
   - Check user exists in database

### Debug Commands

```bash
# Check OTP records
python manage.py shell
from core.models import OTP
OTP.objects.all()

# Test email sending
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])

# Test SMS (if Twilio configured)
python manage.py shell
from core.otp_service import OTPService
OTPService.send_phone_otp('+12345678901', '123456')
```

## 📈 Performance Optimization

### 1. Redis Caching

For high-traffic applications, cache OTPs in Redis:

```python
# Install redis
pip install redis

# Add to settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Database Indexing

Ensure proper indexes on OTP table:

```python
# Already included in model
class Meta:
    indexes = [
        models.Index(fields=['identifier', 'code', 'is_used']),
        models.Index(fields=['expires_at']),
    ]
```

## 🎉 Success Metrics

Track these metrics to ensure OTP system is working:

- **Delivery Rate**: >95% for SMS, >99% for email
- **Verification Rate**: >80% of sent OTPs are verified
- **Response Time**: <2 seconds for OTP sending
- **Error Rate**: <1% for system errors

## 📞 Support

For issues or questions:
1. Check logs in Railway dashboard
2. Test with the provided test script
3. Verify environment variables
4. Check network connectivity

---

**Happy OTP Authentication! 🚀** 