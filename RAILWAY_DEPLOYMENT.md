# Railway Deployment Guide for CalloutRacing

This guide covers deploying CalloutRacing to Railway using their built-in environment variables and deployment process.

## 🚀 Quick Deploy to Railway

### 1. Connect Your Repository

1. Go to [Railway](https://railway.app/)
2. Create a new project
3. Connect your GitHub repository
4. Railway will automatically detect your Django application

### 2. Railway Environment Variables

Railway automatically provides these environment variables:

#### Database Variables (Auto-provided by Railway)
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_PUBLIC_URL` - Public database URL
- `PGDATA` - PostgreSQL data directory
- `PGDATABASE` - Database name
- `PGHOST` - Database host
- `PGPASSWORD` - Database password
- `PGPORT` - Database port
- `PGUSER` - Database user
- `POSTGRES_DB` - Database name
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_USER` - Database user

#### Railway-Specific Variables
- `PORT` - Port to run the application on
- `RAILWAY_DEPLOYMENT_DRAINING_SECONDS` - Deployment draining time
- `SSL_CERT_DAYS` - SSL certificate days

### 3. Required Environment Variables

Add these to your Railway project settings:

#### Django Settings
```
SECRET_KEY=your-secure-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app,localhost,127.0.0.1
```

#### Email Settings (Gmail)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_HOST_USER=digibin@digitalbinarysolutionsllc.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=noreply@calloutracing.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

#### Stripe Settings
```
STRIPE_SECRET_KEY=sk_live_your_production_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_production_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_production_webhook_secret
```

#### Staff Settings
```
STAFF_EMAIL=admin@calloutracing.com
STAFF_PASSWORD=your-secure-admin-password
```

## 🏗️ Railway-Specific Configuration

### Dockerfile for Railway

Use `backend/Dockerfile.railway` for Railway deployment:

```dockerfile
# Railway-optimized Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=calloutracing.settings

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client build-essential libpq-dev dos2unix curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY start-railway.sh /app/start-railway.sh
RUN dos2unix /app/start-railway.sh && chmod +x /app/start-railway.sh

RUN mkdir -p /app/staticfiles /app/media
RUN python manage.py collectstatic --noinput

EXPOSE $PORT

CMD ["bash", "/app/start-railway.sh"]
```

### Start Script for Railway

Use `backend/start-railway.sh` which:
- Automatically detects Python command (`python` or `python3`)
- Uses Railway's `PORT` environment variable
- Handles database migrations
- Collects static files

## 🔧 Railway Deployment Steps

### 1. Automatic Deployment

Railway will automatically:
- Detect your Django application
- Use the `Dockerfile.railway` if present
- Run the `start-railway.sh` script
- Provide database environment variables
- Handle SSL certificates

### 2. Manual Environment Setup

If you need to set environment variables manually:

1. Go to your Railway project dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add the required environment variables listed above

### 3. Database Setup

Railway automatically:
- Creates a PostgreSQL database
- Provides connection strings
- Handles database migrations via the start script

## 📊 Monitoring on Railway

### Logs
- View logs in Railway dashboard
- Real-time log streaming
- Error tracking

### Health Checks
- Railway automatically monitors your application
- Health check endpoint: `/health/`

### Metrics
- CPU and memory usage
- Request/response times
- Error rates

## 🔄 Railway-Specific Commands

### View Logs
```bash
# In Railway dashboard or CLI
railway logs
```

### Run Commands
```bash
# Execute Django commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### Environment Variables
```bash
# View current variables
railway variables

# Set variables
railway variables set SECRET_KEY=your-secret-key
```

## 🚨 Troubleshooting Railway Deployment

### Common Issues

1. **Python Command Not Found**
   - Use `start-railway.sh` which auto-detects Python
   - Ensure `python:3.11-slim` base image

2. **Database Connection Issues**
   - Railway provides `DATABASE_URL` automatically
   - Check if database service is running

3. **Static Files Not Serving**
   - Railway serves static files automatically
   - Ensure `collectstatic` runs in start script

4. **Port Issues**
   - Railway uses `PORT` environment variable
   - Application must bind to `0.0.0.0:$PORT`

### Debug Commands

```bash
# Check Railway environment
railway run env

# Test database connection
railway run python manage.py check --database default

# View application logs
railway logs --follow
```

## 🔒 Security on Railway

### Automatic Security Features
- SSL/TLS certificates (automatic)
- Environment variable encryption
- Network isolation
- Automatic backups

### Best Practices
- Use Railway's built-in environment variables
- Never commit secrets to repository
- Use Railway's secret management
- Enable automatic deployments

## 📈 Scaling on Railway

### Automatic Scaling
- Railway scales based on traffic
- Automatic resource allocation
- Pay-per-use pricing

### Manual Scaling
- Adjust resources in Railway dashboard
- Scale database independently
- Add additional services as needed

## 🔗 Railway CLI

Install Railway CLI for local development:

```bash
npm install -g @railway/cli
railway login
railway link
```

## 📞 Railway Support

- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app/)

## 🎯 Next Steps

1. **Deploy to Railway**
   - Connect your repository
   - Railway will auto-deploy

2. **Configure Domain**
   - Add custom domain in Railway dashboard
   - Update `ALLOWED_HOSTS`

3. **Set Up Monitoring**
   - Configure alerts in Railway
   - Set up external monitoring

4. **Configure CI/CD**
   - Railway auto-deploys on git push
   - Configure deployment branches

Your CalloutRacing application is now ready for Railway deployment! 🚀 