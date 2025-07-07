# CalloutRacing Docker Build Script for Windows
# This script builds both frontend and backend Docker images

Write-Host "🚀 Starting CalloutRacing Docker Build" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "[INFO] Docker is running" -ForegroundColor Blue
} catch {
    Write-Host "[ERROR] Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Create .env files if they don't exist
if (-not (Test-Path "backend/.env")) {
    Write-Host "[WARNING] Backend .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item "backend/env.example" "backend/.env"
    Write-Host "[SUCCESS] Backend .env file created. Please update with your actual values." -ForegroundColor Green
}

if (-not (Test-Path "frontend/.env")) {
    Write-Host "[WARNING] Frontend .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item "frontend/env.example" "frontend/.env"
    Write-Host "[SUCCESS] Frontend .env file created. Please update with your actual values." -ForegroundColor Green
}

# Build Backend
Write-Host "[INFO] Building Backend Docker image..." -ForegroundColor Blue
Set-Location backend

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERROR] requirements.txt not found in backend directory" -ForegroundColor Red
    exit 1
}

# Build backend image
docker build -t calloutracing-backend:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Backend Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Backend Docker build failed" -ForegroundColor Red
    exit 1
}

Set-Location ..

# Build Frontend
Write-Host "[INFO] Building Frontend Docker image..." -ForegroundColor Blue
Set-Location frontend

# Check if package.json exists
if (-not (Test-Path "package.json")) {
    Write-Host "[ERROR] package.json not found in frontend directory" -ForegroundColor Red
    exit 1
}

# Build frontend image
docker build -t calloutracing-frontend:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Frontend Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Frontend Docker build failed" -ForegroundColor Red
    exit 1
}

Set-Location ..

# List built images
Write-Host "[INFO] Built Docker images:" -ForegroundColor Blue
docker images | Select-String "calloutracing"

# Create docker-compose override for development if it doesn't exist
if (-not (Test-Path "docker-compose.override.yml")) {
    Write-Host "[INFO] Creating docker-compose.override.yml for development..." -ForegroundColor Blue
    @"
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
"@ | Out-File -FilePath "docker-compose.override.yml" -Encoding UTF8
    Write-Host "[SUCCESS] docker-compose.override.yml created for development" -ForegroundColor Green
}

Write-Host "[SUCCESS] Docker build completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update .env files with your actual configuration" -ForegroundColor White
Write-Host "2. Run 'docker-compose up' to start all services" -ForegroundColor White
Write-Host "3. Access the application at http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  docker-compose up          # Start all services" -ForegroundColor White
Write-Host "  docker-compose up -d       # Start all services in background" -ForegroundColor White
Write-Host "  docker-compose down        # Stop all services" -ForegroundColor White
Write-Host "  docker-compose logs        # View logs" -ForegroundColor White
Write-Host "  docker-compose logs -f     # Follow logs" -ForegroundColor White
Write-Host "" 