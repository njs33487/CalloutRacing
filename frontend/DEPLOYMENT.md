# Frontend Deployment Guide for Railway

This guide will help you deploy your React frontend to Railway alongside your Django backend.

## Prerequisites

- Railway account connected to your GitHub repository
- Backend already deployed and running at https://calloutracing-backend-production.up.railway.app/

## Deployment Steps

### 1. Create a New Service in Railway

1. Go to your Railway dashboard
2. Click "New Service" → "GitHub Repo"
3. Select your CalloutRacing repository
4. Choose "Deploy from GitHub"

### 2. Configure the Frontend Service

1. **Service Name**: `calloutracing-frontend` (or any name you prefer)
2. **Root Directory**: `frontend`
3. **Build Command**: Leave empty (Dockerfile handles this)
4. **Start Command**: Leave empty (Dockerfile handles this)

### 3. Set Environment Variables

In the Railway dashboard for your frontend service, add these environment variables:

```
VITE_API_URL=https://calloutracing-backend-production.up.railway.app/api
NODE_ENV=production
```

### 4. Deploy

1. Railway will automatically detect the Dockerfile and build your frontend
2. The build process will:
   - Install dependencies
   - Build the React app
   - Serve the built files

### 5. Configure Custom Domain (Optional)

1. In Railway dashboard, go to your frontend service
2. Click "Settings" → "Domains"
3. Add a custom domain like: `app.calloutracing.com` or `www.calloutracing.com`

## File Structure for Deployment

```
frontend/
├── Dockerfile              # Docker configuration
├── railway.json            # Railway deployment config
├── .dockerignore           # Files to exclude from Docker build
├── package.json            # Dependencies and scripts
├── .env                    # Environment variables
└── src/                    # React source code
```

## How It Works

1. **Dockerfile**: Builds the React app and serves it using `serve`
2. **railway.json**: Configures Railway deployment settings
3. **Environment Variables**: Connect frontend to your deployed backend API
4. **Health Check**: Railway monitors the `/` endpoint

## Troubleshooting

### Build Issues
- Check Railway logs for build errors
- Ensure all dependencies are in `package.json`
- Verify Dockerfile syntax

### API Connection Issues
- Confirm `VITE_API_URL` is set correctly
- Test API endpoints manually
- Check CORS settings in Django backend

### Runtime Issues
- Check Railway service logs
- Verify environment variables are set
- Ensure port configuration is correct

## Expected Result

After deployment, your frontend will be available at:
- Railway URL: `https://your-frontend-service-name.up.railway.app/`
- Custom domain (if configured): `https://your-domain.com/`

The frontend will automatically connect to your backend API at `https://calloutracing-backend-production.up.railway.app/api/`.

## Monitoring

- Use Railway dashboard to monitor deployment status
- Check logs for any errors
- Monitor health check status
- Set up alerts for service downtime

## Updates

To update your frontend:
1. Push changes to GitHub
2. Railway will automatically redeploy
3. Monitor the deployment in Railway dashboard 