#!/bin/bash

# Xempla AI Systems Intern Prototype - Deployment Script
# Supports multiple environments and automated deployment

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
DOCKER_IMAGE="xempla/xempla-dashboard"
VERSION="${1:-latest}"
ENVIRONMENT="${2:-development}"
NAMESPACE="xempla-ai"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if kubectl is available (for Kubernetes deployment)
    if [ "$ENVIRONMENT" = "production" ] && ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed (required for production deployment)"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Function to build Docker image
build_image() {
    log_info "Building Docker image..."
    
    cd "$PROJECT_ROOT"
    
    # Build the image
    docker build -t "$DOCKER_IMAGE:$VERSION" -f deployment/docker/Dockerfile .
    
    if [ $? -eq 0 ]; then
        log_success "Docker image built successfully: $DOCKER_IMAGE:$VERSION"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    log_info "Running tests..."
    
    cd "$PROJECT_ROOT"
    
    # Run unit tests
    python -m unittest discover -s tests -v
    
    if [ $? -eq 0 ]; then
        log_success "Tests passed"
    else
        log_error "Tests failed"
        exit 1
    fi
}

# Function to deploy to development environment
deploy_development() {
    log_info "Deploying to development environment..."
    
    cd "$PROJECT_ROOT/deployment/docker"
    
    # Stop existing containers
    docker-compose down
    
    # Start services
    docker-compose up -d
    
    # Wait for service to be ready
    sleep 10
    
    # Check health
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        log_success "Development deployment successful"
        log_info "Dashboard available at: http://localhost:8501"
    else
        log_error "Development deployment failed - health check failed"
        exit 1
    fi
}

# Function to deploy to production environment
deploy_production() {
    log_info "Deploying to production environment..."
    
    # Check if namespace exists
    if ! kubectl get namespace "$NAMESPACE" > /dev/null 2>&1; then
        log_info "Creating namespace: $NAMESPACE"
        kubectl create namespace "$NAMESPACE"
    fi
    
    # Apply Kubernetes manifests
    cd "$PROJECT_ROOT/deployment/kubernetes"
    
    # Apply namespace
    kubectl apply -f namespace.yaml
    
    # Apply ConfigMap
    kubectl apply -f configmap.yaml
    
    # Apply Secrets (assuming they exist)
    log_warning "Please ensure secrets are configured: xempla-secrets"
    
    # Apply PersistentVolumeClaims
    kubectl apply -f pvc.yaml
    
    # Apply Service
    kubectl apply -f service.yaml
    
    # Apply Deployment
    kubectl apply -f deployment.yaml
    
    # Apply Ingress
    kubectl apply -f ingress.yaml
    
    # Wait for deployment to be ready
    log_info "Waiting for deployment to be ready..."
    kubectl rollout status deployment/xempla-dashboard -n "$NAMESPACE" --timeout=300s
    
    if [ $? -eq 0 ]; then
        log_success "Production deployment successful"
        
        # Get service URL
        SERVICE_URL=$(kubectl get service xempla-dashboard -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
        if [ -n "$SERVICE_URL" ]; then
            log_info "Dashboard available at: http://$SERVICE_URL"
        fi
    else
        log_error "Production deployment failed"
        exit 1
    fi
}

# Function to perform health check
health_check() {
    log_info "Performing health check..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying in 10 seconds..."
        sleep 10
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Function to rollback deployment
rollback() {
    log_warning "Rolling back deployment..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        kubectl rollout undo deployment/xempla-dashboard -n "$NAMESPACE"
        kubectl rollout status deployment/xempla-dashboard -n "$NAMESPACE" --timeout=300s
    else
        cd "$PROJECT_ROOT/deployment/docker"
        docker-compose down
        docker-compose up -d
    fi
    
    log_success "Rollback completed"
}

# Function to cleanup
cleanup() {
    log_info "Cleaning up..."
    
    # Remove old Docker images
    docker image prune -f
    
    # Remove unused containers
    docker container prune -f
    
    log_success "Cleanup completed"
}

# Main deployment function
main() {
    log_info "Starting deployment process..."
    log_info "Version: $VERSION"
    log_info "Environment: $ENVIRONMENT"
    
    # Check prerequisites
    check_prerequisites
    
    # Run tests
    run_tests
    
    # Build image
    build_image
    
    # Deploy based on environment
    case $ENVIRONMENT in
        "development")
            deploy_development
            ;;
        "production")
            deploy_production
            ;;
        *)
            log_error "Unknown environment: $ENVIRONMENT"
            log_info "Supported environments: development, production"
            exit 1
            ;;
    esac
    
    # Perform health check
    if ! health_check; then
        log_error "Deployment failed health check"
        rollback
        exit 1
    fi
    
    # Cleanup
    cleanup
    
    log_success "Deployment completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    "rollback")
        rollback
        ;;
    "health")
        health_check
        ;;
    "cleanup")
        cleanup
        ;;
    *)
        main
        ;;
esac 