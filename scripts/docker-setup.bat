@echo off
setlocal enabledelayedexpansion

REM Docker Registry Setup Script for CalloutRacing (Windows)
REM This script helps set up and manage Docker images in GitHub Container Registry

REM Configuration
set REGISTRY=ghcr.io
set REPO_NAME=CalloutRacing
set GITHUB_USERNAME=njs33487

REM Default image names
set BACKEND_IMAGE=%REGISTRY%/%GITHUB_USERNAME%/%REPO_NAME%/backend
set FRONTEND_IMAGE=%REGISTRY%/%GITHUB_USERNAME%/%REPO_NAME%/frontend

REM Function to print colored output
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Function to check Docker installation
:check_docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed. Please install Docker Desktop first."
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not running. Please start Docker Desktop."
    exit /b 1
)

call :print_success "Docker is installed and running"
goto :eof

REM Function to login to GitHub Container Registry
:login_to_registry
call :print_status "Logging in to GitHub Container Registry..."

if "%GITHUB_TOKEN%"=="" (
    call :print_warning "GITHUB_TOKEN not set. Please set it or create a Personal Access Token."
    call :print_status "You can create a token at: https://github.com/settings/tokens"
    call :print_status "Required scopes: write:packages, read:packages"
    echo.
    set /p GITHUB_TOKEN="Enter your GitHub Personal Access Token: "
)

echo %GITHUB_TOKEN% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin

if errorlevel 1 (
    call :print_error "Failed to login to GitHub Container Registry"
    exit /b 1
) else (
    call :print_success "Successfully logged in to GitHub Container Registry"
)
goto :eof

REM Function to build and push backend image
:build_backend
set tag=%~1
if "%tag%"=="" set tag=latest

call :print_status "Building backend image with tag: %tag%"

docker build -t %BACKEND_IMAGE%:%tag% -f Dockerfile .

if errorlevel 1 (
    call :print_error "Failed to build backend image"
    exit /b 1
) else (
    call :print_success "Backend image built successfully"
    
    call :print_status "Pushing backend image to registry..."
    docker push %BACKEND_IMAGE%:%tag%
    
    if errorlevel 1 (
        call :print_error "Failed to push backend image"
        exit /b 1
    ) else (
        call :print_success "Backend image pushed successfully"
    )
)
goto :eof

REM Function to build and push frontend image
:build_frontend
set tag=%~1
if "%tag%"=="" set tag=latest

call :print_status "Building frontend image with tag: %tag%"

docker build -t %FRONTEND_IMAGE%:%tag% -f frontend/Dockerfile frontend/

if errorlevel 1 (
    call :print_error "Failed to build frontend image"
    exit /b 1
) else (
    call :print_success "Frontend image built successfully"
    
    call :print_status "Pushing frontend image to registry..."
    docker push %FRONTEND_IMAGE%:%tag%
    
    if errorlevel 1 (
        call :print_error "Failed to push frontend image"
        exit /b 1
    ) else (
        call :print_success "Frontend image pushed successfully"
    )
)
goto :eof

REM Function to build and push all images
:build_all
set tag=%~1
if "%tag%"=="" set tag=latest

call :print_status "Building and pushing all images with tag: %tag%"

call :build_backend %tag%
call :build_frontend %tag%

call :print_success "All images built and pushed successfully"
goto :eof

REM Function to pull images
:pull_images
set tag=%~1
if "%tag%"=="" set tag=latest

call :print_status "Pulling images with tag: %tag%"

docker pull %BACKEND_IMAGE%:%tag%
docker pull %FRONTEND_IMAGE%:%tag%

call :print_success "Images pulled successfully"
goto :eof

REM Function to run with docker-compose
:run_compose
set env_file=%~1
if "%env_file%"=="" set env_file=.env

if not exist "%env_file%" (
    call :print_warning "Environment file %env_file% not found. Creating from example..."
    if exist "env.example" (
        copy env.example "%env_file%" >nul
        call :print_success "Created %env_file% from env.example"
    ) else (
        call :print_error "No env.example file found. Please create %env_file% manually."
        exit /b 1
    )
)

call :print_status "Running with docker-compose..."
docker-compose up -d

call :print_success "Services started successfully"
call :print_status "Backend: http://localhost:8000"
call :print_status "Frontend: http://localhost:3000"
goto :eof

REM Function to stop services
:stop_services
call :print_status "Stopping services..."
docker-compose down

call :print_success "Services stopped successfully"
goto :eof

REM Function to show usage
:show_usage
echo Usage: %~nx0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   login              Login to GitHub Container Registry
echo   build-backend      Build and push backend image
echo   build-frontend     Build and push frontend image
echo   build-all          Build and push all images
echo   pull               Pull images from registry
echo   run                Run services with docker-compose
echo   stop               Stop services
echo   setup              Complete setup (login + build-all)
echo.
echo Options:
echo   -t TAG             Specify image tag (default: latest)
echo   -e FILE            Specify environment file (default: .env)
echo   -h                 Show this help message
echo.
echo Environment Variables:
echo   GITHUB_TOKEN       GitHub Personal Access Token
echo   GITHUB_USERNAME    GitHub username (default: njs33487)
goto :eof

REM Main script logic
:main
set command=
set tag=latest
set env_file=.env

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :execute_command

if "%~1"=="login" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="build-backend" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="build-frontend" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="build-all" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="pull" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="run" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="stop" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="setup" (
    set command=%~1
    shift
    goto :parse_args
)
if "%~1"=="-t" (
    set tag=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-e" (
    set env_file=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-h" (
    call :show_usage
    exit /b 0
)

call :print_error "Unknown option: %~1"
call :show_usage
exit /b 1

:execute_command
if "%command%"=="" (
    call :print_error "No command specified"
    call :show_usage
    exit /b 1
)

REM Check Docker installation
call :check_docker
if errorlevel 1 exit /b 1

REM Execute command
if "%command%"=="login" (
    call :login_to_registry
) else if "%command%"=="build-backend" (
    call :build_backend %tag%
) else if "%command%"=="build-frontend" (
    call :build_frontend %tag%
) else if "%command%"=="build-all" (
    call :build_all %tag%
) else if "%command%"=="pull" (
    call :pull_images %tag%
) else if "%command%"=="run" (
    call :run_compose %env_file%
) else if "%command%"=="stop" (
    call :stop_services
) else if "%command%"=="setup" (
    call :login_to_registry
    call :build_all %tag%
) else (
    call :print_error "Unknown command: %command%"
    call :show_usage
    exit /b 1
)

exit /b 0 