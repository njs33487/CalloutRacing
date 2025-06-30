#!/bin/bash

# Docker Registry Setup Script for CalloutRacing
# This script helps set up and manage Docker images in GitHub Container Registry

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="ghcr.io"
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
GITHUB_USERNAME=$(git config user.name | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Default image names
BACKEND_IMAGE="${REGISTRY}/${GITHUB_USERNAME}/${REPO_NAME}/backend"
FRONTEND_IMAGE="${REGISTRY}/${GITHUB_USERNAME}/${REPO_NAME}/frontend"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Docker installation
check_docker() {
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Function to login to GitHub Container Registry
login_to_registry() {
    print_status "Logging in to GitHub Container Registry..."
    
    if [ -z "$GITHUB_TOKEN" ]; then
        print_warning "GITHUB_TOKEN not set. Please set it or create a Personal Access Token."
        print_status "You can create a token at: https://github.com/settings/tokens"
        print_status "Required scopes: write:packages, read:packages"
        echo
        read -p "Enter your GitHub Personal Access Token: " GITHUB_TOKEN
    fi
    
    echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
    
    if [ $? -eq 0 ]; then
        print_success "Successfully logged in to GitHub Container Registry"
    else
        print_error "Failed to login to GitHub Container Registry"
        exit 1
    fi
}

# Function to build and push backend image
build_backend() {
    local tag=${1:-latest}
    
    print_status "Building backend image with tag: $tag"
    
    docker build -t "${BACKEND_IMAGE}:${tag}" -f Dockerfile .
    
    if [ $? -eq 0 ]; then
        print_success "Backend image built successfully"
        
        print_status "Pushing backend image to registry..."
        docker push "${BACKEND_IMAGE}:${tag}"
        
        if [ $? -eq 0 ]; then
            print_success "Backend image pushed successfully"
        else
            print_error "Failed to push backend image"
            exit 1
        fi
    else
        print_error "Failed to build backend image"
        exit 1
    fi
}

# Function to build and push frontend image
build_frontend() {
    local tag=${1:-latest}
    
    print_status "Building frontend image with tag: $tag"
    
    docker build -t "${FRONTEND_IMAGE}:${tag}" -f frontend/Dockerfile frontend/
    
    if [ $? -eq 0 ]; then
        print_success "Frontend image built successfully"
        
        print_status "Pushing frontend image to registry..."
        docker push "${FRONTEND_IMAGE}:${tag}"
        
        if [ $? -eq 0 ]; then
            print_success "Frontend image pushed successfully"
        else
            print_error "Failed to push frontend image"
            exit 1
        fi
    else
        print_error "Failed to build frontend image"
        exit 1
    fi
}

# Function to build and push all images
build_all() {
    local tag=${1:-latest}
    
    print_status "Building and pushing all images with tag: $tag"
    
    build_backend "$tag"
    build_frontend "$tag"
    
    print_success "All images built and pushed successfully"
}

# Function to pull images
pull_images() {
    local tag=${1:-latest}
    
    print_status "Pulling images with tag: $tag"
    
    docker pull "${BACKEND_IMAGE}:${tag}"
    docker pull "${FRONTEND_IMAGE}:${tag}"
    
    print_success "Images pulled successfully"
}

# Function to run with docker-compose
run_compose() {
    local env_file=${1:-.env}
    
    if [ ! -f "$env_file" ]; then
        print_warning "Environment file $env_file not found. Creating from example..."
        if [ -f "env.example" ]; then
            cp env.example "$env_file"
            print_success "Created $env_file from env.example"
        else
            print_error "No env.example file found. Please create $env_file manually."
            exit 1
        fi
    fi
    
    print_status "Running with docker-compose..."
    docker-compose up -d
    
    print_success "Services started successfully"
    print_status "Backend: http://localhost:8000"
    print_status "Frontend: http://localhost:3000"
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    
    print_success "Services stopped successfully"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  login              Login to GitHub Container Registry"
    echo "  build-backend      Build and push backend image"
    echo "  build-frontend     Build and push frontend image"
    echo "  build-all          Build and push all images"
    echo "  pull               Pull images from registry"
    echo "  run                Run services with docker-compose"
    echo "  stop               Stop services"
    echo "  setup              Complete setup (login + build-all)"
    echo
    echo "Options:"
    echo "  -t, --tag TAG      Specify image tag (default: latest)"
    echo "  -e, --env FILE     Specify environment file (default: .env)"
    echo "  -h, --help         Show this help message"
    echo
    echo "Environment Variables:"
    echo "  GITHUB_TOKEN       GitHub Personal Access Token"
    echo "  GITHUB_USERNAME    GitHub username (auto-detected from git config)"
}

# Main script logic
main() {
    local command=""
    local tag="latest"
    local env_file=".env"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            login|build-backend|build-frontend|build-all|pull|run|stop|setup)
                command="$1"
                shift
                ;;
            -t|--tag)
                tag="$2"
                shift 2
                ;;
            -e|--env)
                env_file="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    if [ -z "$command" ]; then
        print_error "No command specified"
        show_usage
        exit 1
    fi
    
    # Check Docker installation
    check_docker
    
    # Execute command
    case $command in
        login)
            login_to_registry
            ;;
        build-backend)
            build_backend "$tag"
            ;;
        build-frontend)
            build_frontend "$tag"
            ;;
        build-all)
            build_all "$tag"
            ;;
        pull)
            pull_images "$tag"
            ;;
        run)
            run_compose "$env_file"
            ;;
        stop)
            stop_services
            ;;
        setup)
            login_to_registry
            build_all "$tag"
            ;;
        *)
            print_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 