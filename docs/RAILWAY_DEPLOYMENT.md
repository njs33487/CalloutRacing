# Railway Deployment Guide for CalloutRacing

This guide will walk you through deploying the CalloutRacing Django/React application to Railway.

## Prerequisites

- Railway account (sign up at [railway.app](https://railway.app))
- Git repository with your CalloutRacing project
- Railway CLI (optional but recommended)

## Deployment Strategy

We'll deploy the application using a monorepo approach with two services:
1. **Backend Service**: Django API
2. **Frontend Service**: React application

## Step 1: Prepare Your Repository

### 1.1 Backend Configuration

The backend is already configured for Railway deployment with:
- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `runtime.txt` - Python version specification
- Updated `settings.py` for production

### 1.2 Frontend Configuration

The frontend is configured with:
- `railway.json` - Railway configuration
- Updated `package.json` with preview script
- Production build settings in `vite.config.ts`

## Step 2: Deploy to Railway

### Option A: Using Railway Dashboard

1. **Create a new project**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect your repository**:
   - Select your CalloutRacing repository
   - Railway will detect the project structure

3. **Deploy Backend**:
   - Railway will automatically detect the Django backend
   - Set the root directory to `backend`
   - Add environment variables (see below)

4. **Deploy Frontend**:
   - Create a new service for the frontend
   - Set the root directory to `frontend`
   - Add environment variables (see below)

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

## Step 3: Environment Variables

### Backend Environment Variables

Set these in your Railway backend service:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=your-railway-domain.railway.app

# Database (Railway will provide this automatically)
DATABASE_URL=postgresql://...

# CORS Settings
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.railway.app

# Media Files
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

### Frontend Environment Variables

Set these in your Railway frontend service:

```bash
# API Configuration
VITE_API_URL=https://your-backend-domain.railway.app/api
VITE_APP_NAME=CalloutRacing

# Development Settings
VITE_DEV_MODE=false
```

## Step 4: Database Setup

1. **Add PostgreSQL service**:
   - In your Railway project, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically link it to your backend

2. **Run migrations**:
   - Go to your backend service
   - Open the terminal
   - Run: `python manage.py migrate`

3. **Create superuser**:
   - Run: `python manage.py createsuperuser`

## Step 5: Domain Configuration

### Custom Domains

1. **Backend API**:
   - Go to your backend service settings
   - Add a custom domain (e.g., `api.calloutracing.com`)

2. **Frontend**:
   - Go to your frontend service settings
   - Add a custom domain (e.g., `calloutracing.com`)

### Update CORS Settings

After setting up domains, update your backend CORS settings:

```bash
CORS_ALLOWED_ORIGINS=https://calloutracing.com,https://www.calloutracing.com
```

## Step 6: SSL and Security

Railway automatically provides SSL certificates for all domains. The Django settings are already configured for production security:

- HTTPS redirect enabled
- Secure cookies
- HSTS headers
- XSS protection

## Step 7: Monitoring and Logs

### View Logs

- Go to your service in Railway dashboard
- Click on "Deployments" tab
- View real-time logs

### Health Checks

Both services have health check endpoints:
- Backend: `/api/`
- Frontend: `/`

## Step 8: Continuous Deployment

Railway automatically deploys when you push to your main branch. To set up:

1. **Connect GitHub repository** (if not already done)
2. **Configure branch**:
   - Go to service settings
   - Set "Deploy Branch" to `main`

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check the build logs in Railway dashboard
   - Ensure all dependencies are in `requirements.txt` (backend) or `package.json` (frontend)

2. **Database Connection**:
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running

3. **CORS Errors**:
   - Ensure `CORS_ALLOWED_ORIGINS` includes your frontend domain
   - Check that domains are using HTTPS

4. **Static Files**:
   - Run `python manage.py collectstatic` in backend terminal
   - Ensure `STATIC_ROOT` is set correctly

### Performance Optimization

1. **Database**:
   - Monitor query performance
   - Add database indexes as needed

2. **Frontend**:
   - Enable gzip compression
   - Optimize images and assets

3. **Caching**:
   - Consider adding Redis for caching
   - Implement CDN for static files

## Environment-Specific Configurations

### Development

```bash
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Staging

```bash
DEBUG=False
CORS_ALLOWED_ORIGINS=https://staging.calloutracing.com
```

### Production

```bash
DEBUG=False
CORS_ALLOWED_ORIGINS=https://calloutracing.com,https://www.calloutracing.com
```

## Backup and Recovery

### Database Backups

Railway automatically backs up PostgreSQL databases. To create manual backups:

```bash
# In Railway backend terminal
python manage.py dumpdata > backup.json
```

### Restore Database

```bash
# In Railway backend terminal
python manage.py loaddata backup.json
```

## Cost Optimization

1. **Service Scaling**:
   - Start with minimal resources
   - Scale up based on usage

2. **Database**:
   - Use appropriate PostgreSQL plan
   - Monitor storage usage

3. **Bandwidth**:
   - Optimize images and assets
   - Use CDN for static files

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Project Issues: Create an issue in your repository

---

**Happy Deploying! 🚀** 