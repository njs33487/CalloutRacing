# Environment Variables for Railway Deployment

## Required Environment Variables

Set these environment variables in your Railway project dashboard:

### Django Core Settings
```
SECRET_KEY=!c+z8w*$64yzo4kic#hkly@t7&%ro&^6$#wb52+*_vzwfao(@0
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,calloutracing.up.railway.app
```

### Database (Railway PostgreSQL)
```
DATABASE_URL=postgresql://postgres:YYXsAGJBiHdzoqKwgluUEhgIrIkAcauu@postgres.railway.internal:5432/railway
```
*Note: This is your actual Railway PostgreSQL database URL*

### CORS Settings
```
CORS_ALLOWED_ORIGINS=https://calloutracing.up.railway.app
```

### Email Configuration (for contact form)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=digibin@digitalbinarysolutionsllc.com
EMAIL_HOST_PASSWORD=troc jbbw ikct mdsl
DEFAULT_FROM_EMAIL=digibin@digitalbinarysolutionsllc.com
```

## How to Set Environment Variables in Railway

1. **Go to Railway Dashboard**
   - Navigate to your project
   - Click on your service (backend)

2. **Access Variables Tab**
   - Click on the "Variables" tab
   - Click "New Variable" to add each variable

3. **Add Variables One by One**
   - Copy each variable from the list above
   - Paste into Railway's variable interface
   - Click "Add"

## Important Notes

### Gmail App Password
For the `EMAIL_HOST_PASSWORD`, you need to:
1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" from Google Account settings
3. Use that app password (not your regular Gmail password)

### CORS Origins
Update `CORS_ALLOWED_ORIGINS` with:
- Your frontend domain (if deployed separately)
- Your Railway app domain (e.g., `https://your-app.railway.app`)

### Database
Railway will automatically provide `DATABASE_URL` when you:
1. Add a PostgreSQL database to your project
2. Link it to your backend service

## Complete Variable List for Copy-Paste

```
SECRET_KEY=!c+z8w*$64yzo4kic#hkly@t7&%ro&^6$#wb52+*_vzwfao(@0
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,calloutracing.up.railway.app
DATABASE_URL=postgresql://postgres:YYXsAGJBiHdzoqKwgluUEhgIrIkAcauu@postgres.railway.internal:5432/railway
CORS_ALLOWED_ORIGINS=https://calloutracing.up.railway.app
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=digibin@digitalbinarysolutionsllc.com
EMAIL_HOST_PASSWORD=troc jbbw ikct mdsl
DEFAULT_FROM_EMAIL=digibin@digitalbinarysolutionsllc.com
```

## Testing Your Setup

After setting the variables:
1. Redeploy your application
2. Check the logs for any configuration errors
3. Test the contact form functionality
4. Verify database connections work

## Security Notes

- Never commit the actual `SECRET_KEY` to version control
- Keep your Gmail app password secure
- Use `DEBUG=False` in production
- Regularly rotate your `SECRET_KEY` 