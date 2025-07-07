#!/bin/bash

# CalloutRacing Docker Build Script
# This script builds both frontend and backend Docker images

set -e  # Exit on any error

echo "🚀 Starting CalloutRacing Docker Build"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    print_warning "Backend .env file not found. Creating from template..."
    cp backend/env.example backend/.env
    print_success "Backend .env file created. Please update with your actual values."
fi

if [ ! -f "frontend/.env" ]; then
    print_warning "Frontend .env file not found. Creating from template..."
    cp frontend/env.example frontend/.env
    print_success "Frontend .env file created. Please update with your actual values."
fi

# Build Backend
print_status "Building Backend Docker image..."
cd backend

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

# Build backend image
docker build -t calloutracing-backend:latest .
if [ $? -eq 0 ]; then
    print_success "Backend Docker image built successfully"
else
    print_error "Backend Docker build failed"
    exit 1
fi

cd ..

# Build Frontend
print_status "Building Frontend Docker image..."
cd frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_error "package.json not found in frontend directory"
    exit 1
fi

# Build frontend image
docker build -t calloutracing-frontend:latest .
if [ $? -eq 0 ]; then
    print_success "Frontend Docker image built successfully"
else
    print_error "Frontend Docker build failed"
    exit 1
fi

cd ..

# List built images
print_status "Built Docker images:"
docker images | grep calloutracing

# Create docker-compose override for development if it doesn't exist
if [ ! -f "docker-compose.override.yml" ]; then
    print_status "Creating docker-compose.override.yml for development..."
    cat > docker-compose.override.yml << EOF
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
      - /app/staticfiles
      - /app/media
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://postgres:password@db:5432/calloutracing
    depends_on:
      - db

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - VITE_API_URL=http://localhost:8000/api
    ports:
      - "3000:3000"

  db:
    environment:
      - POSTGRES_DB=calloutracing
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
EOF
    print_success "docker-compose.override.yml created for development"
fi

print_success "Docker build completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env files with your actual configuration"
echo "2. Run 'docker-compose up' to start all services"
echo "3. Access the application at http://localhost:3000"
echo ""
echo "Available commands:"
echo "  docker-compose up          # Start all services"
echo "  docker-compose up -d       # Start all services in background"
echo "  docker-compose down        # Stop all services"
echo "  docker-compose logs        # View logs"
echo "  docker-compose logs -f     # Follow logs"
echo "" 