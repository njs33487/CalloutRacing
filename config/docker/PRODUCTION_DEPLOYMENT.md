# CalloutRacing Production Deployment Guide

This guide covers deploying CalloutRacing to production with Docker.

## 🚀 Quick Start

### 1. Setup Production Environment

```bash
cd config/docker
chmod +x setup-production.sh
./setup-production.sh
```

This will create a `.env.production` file with all required environment variables.

### 2. Deploy to Production

```bash
chmod +x deploy-production.sh
./deploy-production.sh
```

## 📋 Prerequisites

- Docker and Docker Compose installed
- Railway database credentials
- Gmail SMTP credentials
- Stripe production keys
- Domain name configured
- SSL certificate (recommended)

## 🔧 Configuration

### Environment Variables

The following environment variables must be set in `.env.production`:

#### Django Settings
- `SECRET_KEY`: Secure Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains

#### Database (Railway)
- `DATABASE_URL`: Railway PostgreSQL connection string
- `DATABASE_PUBLIC_URL`: Railway public database URL
- `PGPASSWORD`: Database password
- `PGUSER`: Database user

#### Email (Gmail)
- `EMAIL_HOST`: SMTP server (smtp.gmail.com)
- `EMAIL_HOST_USER`: Gmail address
- `EMAIL_HOST_PASSWORD`: Gmail app password
- `DEFAULT_FROM_EMAIL`: From email address

#### Stripe
- `STRIPE_SECRET_KEY`: Production Stripe secret key
- `STRIPE_PUBLISHABLE_KEY`: Production Stripe publishable key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret

#### Frontend
- `VITE_API_URL`: Backend API URL
- `VITE_APP_NAME`: Application name

## 🏗️ Architecture

### Production Services

1. **Backend** (`calloutracing-backend:latest`)
   - Django REST API
   - Runs on port 8000
   - Uses Railway PostgreSQL
   - Non-root user for security

2. **Frontend** (`calloutracing-frontend:latest`)
   - React/Vite application
   - Served by Nginx
   - Runs on port 80
   - Optimized for production

3. **Redis** (`redis:7-alpine`)
   - Session storage
   - Caching
   - Runs on port 6379

### Security Features

- Non-root users in containers
- Security headers in Nginx
- Gzip compression
- Static file caching
- Health checks
- Environment variable validation

## 🔒 Security Checklist

Before deploying to production:

- [ ] `DEBUG=False` in environment
- [ ] Secure `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database credentials are secure
- [ ] Email credentials are secure
- [ ] Stripe production keys configured
- [ ] SSL/TLS certificates installed
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] Monitoring configured

## 📊 Monitoring

### Health Checks

- Backend: `http://localhost:8000/health/`
- Frontend: `http://localhost/health`

### Logs

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs

# View specific service logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

### Container Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

## 🔄 Maintenance

### Database Migrations

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### Static Files

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic
```

### Restart Services

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and deploy
./deploy-production.sh
```

## 🚨 Troubleshooting

### Common Issues

1. **Environment Variables Not Loading**
   ```bash
   # Check if .env.production exists
   ls -la .env.production
   
   # Verify variables are set
   docker-compose -f docker-compose.prod.yml config
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   docker-compose -f docker-compose.prod.yml exec backend python manage.py check --database default
   ```

3. **Static Files Not Serving**
   ```bash
   # Recollect static files
   docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
   ```

4. **Container Won't Start**
   ```bash
   # Check container logs
   docker-compose -f docker-compose.prod.yml logs backend
   
   # Check container status
   docker-compose -f docker-compose.prod.yml ps
   ```

### Performance Optimization

1. **Enable Gzip Compression** (already configured in nginx.conf)
2. **Cache Static Files** (already configured)
3. **Use CDN** for static assets
4. **Database Optimization**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python manage.py dbshell
   ```

## 📝 Backup Strategy

### Database Backup

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec backend python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Restore backup
docker-compose -f docker-compose.prod.yml exec backend python manage.py loaddata backup_file.json
```

### Volume Backup

```bash
# Backup volumes
docker run --rm -v calloutracing_static_volume:/data -v $(pwd):/backup alpine tar czf /backup/static_backup.tar.gz -C /data .
docker run --rm -v calloutracing_media_volume:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          # Add your deployment commands here
          ssh user@server "cd /path/to/app && git pull && ./deploy-production.sh"
```

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review container logs
3. Verify environment variables
4. Test database connectivity
5. Check network connectivity

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Railway Documentation](https://docs.railway.app/) 