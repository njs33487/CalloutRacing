# Authentication Guide for CalloutRacing API

## Authentication Methods

Your CalloutRacing API uses **Token Authentication** for secure access to protected endpoints.

## 1. User Registration

### Register a New User
```bash
curl -X POST https://calloutracing.up.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "your_password",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "token": "your_auth_token_here",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

## 2. User Login

### Login to Get Token
```bash
curl -X POST https://calloutracing.up.railway.app/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "token": "your_auth_token_here",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

## 3. Using Authentication Token

### Include Token in API Requests
```bash
curl -X GET https://calloutracing.up.railway.app/api/ \
  -H "Authorization: Token your_auth_token_here"
```

### PowerShell Example
```powershell
$headers = @{
    "Authorization" = "Token your_auth_token_here"
    "Content-Type" = "application/json"
}

Invoke-WebRequest -Uri "https://calloutracing.up.railway.app/api/" -Headers $headers
```

## 4. Testing Authentication

### Test Protected Endpoints

1. **API Root (Protected)**
```bash
curl -X GET https://calloutracing.up.railway.app/api/ \
  -H "Authorization: Token your_auth_token_here"
```

2. **User Profile (Protected)**
```bash
curl -X GET https://calloutracing.up.railway.app/api/profile/ \
  -H "Authorization: Token your_auth_token_here"
```

3. **Create Callout (Protected)**
```bash
curl -X POST https://calloutracing.up.railway.app/api/callouts/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I challenge you to a race!",
    "location_type": "track",
    "race_type": "quarter_mile"
  }'
```

## 5. Public Endpoints (No Auth Required)

### Contact Form
```bash
curl -X POST https://calloutracing.up.railway.app/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "General Inquiry",
    "message": "Hello, I have a question about CalloutRacing."
  }'
```

### Health Check
```bash
curl -X GET https://calloutracing.up.railway.app/health/
```

## 6. Creating a Superuser (Admin)

### Via Django Admin
1. Access: `https://calloutracing.up.railway.app/admin/`
2. Login with superuser credentials
3. Manage users, tokens, and data

### Via Command Line (Local Development)
```bash
cd backend
python manage.py createsuperuser
```

## 7. Token Management

### View Your Tokens
- Go to Django Admin: `https://calloutracing.up.railway.app/admin/authtoken/token/`
- View and manage authentication tokens

### Logout (Invalidate Token)
```bash
curl -X POST https://calloutracing.up.railway.app/api/logout/ \
  -H "Authorization: Token your_auth_token_here"
```

## 8. Environment Variables for Testing

Add these to your local `.env` file for testing:
```
API_BASE_URL=https://calloutracing.up.railway.app
API_TOKEN=your_auth_token_here
```

## 9. Common Authentication Errors

### 401 Unauthorized
- Token is missing or invalid
- Solution: Get a new token via login

### 403 Forbidden
- User doesn't have permission for the action
- Solution: Check user permissions

### 400 Bad Request
- Invalid request data
- Solution: Check request format and required fields

## 10. Testing with Postman/Insomnia

1. **Set Base URL**: `https://calloutracing.up.railway.app`
2. **Add Header**: `Authorization: Token your_auth_token_here`
3. **Test Endpoints**: Use the examples above

## Quick Start Example

1. **Register a user**
2. **Copy the token from the response**
3. **Use the token in subsequent requests**
4. **Test protected endpoints**

Your API is now ready for authenticated requests! 🏁 