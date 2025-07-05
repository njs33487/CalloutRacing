# Docker Setup and GitHub Container Registry

This document provides comprehensive instructions for setting up Docker images and using GitHub Container Registry (GHCR) for the CalloutRacing project.

## Overview

The project uses Docker containers for both backend and frontend services, with images stored in GitHub Container Registry for easy deployment and distribution.

## Prerequisites

1. **Docker Desktop** installed and running
2. **GitHub account** with access to the repository
3. **GitHub Personal Access Token** with appropriate permissions

## GitHub Container Registry Setup

### 1. Create GitHub Personal Access Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select the following scopes:
   - `write:packages` - Upload packages to GitHub Package Registry
   - `read:packages` - Download packages from GitHub Package Registry
   - `delete:packages` - Delete packages from GitHub Package Registry
4. Generate the token and copy it securely

### 2. Set Environment Variables

Set the following environment variables:

```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token_here"
$env:GITHUB_USERNAME="njs33487"

# Windows (Command Prompt)
set GITHUB_TOKEN=your_github_token_here
set GITHUB_USERNAME=njs33487

# Linux/macOS
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_USERNAME="njs33487"
```

## Quick Start

### Using the Setup Scripts

The project includes convenient scripts for managing Docker images:

#### Windows (PowerShell/Command Prompt)
```bash
# Complete setup (login + build all images)
scripts\docker-setup.bat setup

# Individual commands
scripts\docker-setup.bat login
scripts\docker-setup.bat build-all
scripts\docker-setup.bat run
scripts\docker-setup.bat stop
```

#### Linux/macOS
```bash
# Make script executable
chmod +x scripts/docker-setup.sh

# Complete setup (login + build all images)
./scripts/docker-setup.sh setup

# Individual commands
./scripts/docker-setup.sh login
./scripts/docker-setup.sh build-all
./scripts/docker-setup.sh run
./scripts/docker-setup.sh stop
```

### Manual Setup

If you prefer to run commands manually:

#### 1. Login to GitHub Container Registry
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
```

#### 2. Build and Push Images
```bash
# Backend
docker build -t ghcr.io/njs33487/calloutracing/backend:latest -f Dockerfile .
docker push ghcr.io/njs33487/calloutracing/backend:latest

# Frontend
docker build -t ghcr.io/njs33487/calloutracing/frontend:latest -f frontend/Dockerfile frontend/
docker push ghcr.io/njs33487/calloutracing/frontend:latest
```

## Docker Compose Setup

### Development Environment

For local development, use the standard docker-compose file:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Environment

For production deployment, use the production docker-compose file:

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@db:5432/calloutracing
POSTGRES_DB=calloutracing
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Email Configuration
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Staff Account
STAFF_EMAIL=admin@calloutracing.com
STAFF_PASSWORD=your_secure_admin_password

# Frontend
VITE_API_URL=https://your-domain.com/api

# Redis
REDIS_URL=redis://redis:6379/0

# GitHub Repository (for Docker images)
GITHUB_REPOSITORY=njs33487/calloutracing
```

### Environment File Setup

You can use the provided setup script to create the environment file:

```bash
# Copy from example
cp env.example .env

# Edit the file with your actual values
# Windows
notepad .env

# Linux/macOS
nano .env
```

## GitHub Actions Workflow

The project includes a GitHub Actions workflow (`.github/workflows/docker-build.yml`) that automatically builds and pushes Docker images when:

- Code is pushed to `main` or `dev` branches
- Tags are created (e.g., `v1.0.0`)
- Pull requests are created

### Workflow Features

- **Multi-platform builds** using Docker Buildx
- **Layer caching** for faster builds
- **Automatic tagging** based on git events
- **Parallel builds** for backend and frontend
- **Security scanning** (can be added)

### Manual Workflow Trigger

You can manually trigger the workflow:

1. Go to the GitHub repository
2. Click "Actions" tab
3. Select "Build and Push Docker Images"
4. Click "Run workflow"
5. Select branch and click "Run workflow"

## Image Management

### Available Commands

```bash
# Build specific images
scripts/docker-setup.sh build-backend -t v1.0.0
scripts/docker-setup.sh build-frontend -t v1.0.0

# Pull latest images
scripts/docker-setup.sh pull

# Pull specific version
scripts/docker-setup.sh pull -t v1.0.0

# List local images
docker images | grep calloutracing

# Remove old images
docker image prune -f
```

### Image Tags

The workflow automatically creates tags based on:

- **Branch names**: `dev`, `main`
- **Git tags**: `v1.0.0`, `v1.0.1`
- **Commit SHA**: `dev-abc123`, `main-def456`

### Image Security

- Images are scanned for vulnerabilities
- Base images are regularly updated
- Multi-stage builds reduce attack surface
- Non-root user in containers

## Deployment

### Local Development

```bash
# Start development environment
docker-compose up -d

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Database: localhost:5432
# Redis: localhost:6379
```

### Production Deployment

```bash
# Set production environment variables
export DEBUG=False
export ALLOWED_HOSTS=your-domain.com

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Access services
# Application: https://your-domain.com
# API: https://your-domain.com/api
```

### SSL Configuration

For production HTTPS, you need SSL certificates:

1. Create `ssl/` directory
2. Add your certificates:
   - `ssl/cert.pem` - SSL certificate
   - `ssl/key.pem` - Private key

```bash
mkdir ssl
# Copy your SSL certificates to ssl/ directory
```

## Troubleshooting

### Common Issues

#### 1. Docker Login Failed
```bash
# Check token permissions
# Ensure token has write:packages scope
# Verify username is correct
```

#### 2. Build Failures
```bash
# Check Docker is running
docker info

# Clear Docker cache
docker system prune -a

# Check disk space
docker system df
```

#### 3. Container Startup Issues
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend
```

#### 4. Network Issues
```bash
# Check network connectivity
docker network ls
docker network inspect calloutracing-network

# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

### Debug Commands

```bash
# Enter running container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container resources
docker stats

# View detailed container info
docker inspect <container_id>

# Check image layers
docker history <image_name>
```

## Best Practices

### Security
- Use specific image tags instead of `latest`
- Regularly update base images
- Scan images for vulnerabilities
- Use secrets management for sensitive data

### Performance
- Use multi-stage builds
- Optimize layer caching
- Minimize image size
- Use .dockerignore files

### Monitoring
- Set up health checks
- Monitor container resources
- Log aggregation
- Alert on failures

## Support

For issues related to Docker setup:

1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Check container logs
4. Create an issue in the repository

## Additional Resources

- [GitHub Container Registry Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/) 