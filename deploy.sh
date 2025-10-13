#!/bin/bash

# MyNutriAI Deployment Script
# Direct gcloud CLI deployment to Cloud Run
# Author: MyNutriAI Team
# Version: 1.0.0

set -e  # Exit on any error

# Configuration
PROJECT_ID="mynutriai"
REGION="us-central1"
BACKEND_SERVICE="mynutriai-backend"
FRONTEND_SERVICE="mynutriai-frontend"

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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        log_error "You are not authenticated with gcloud. Please run 'gcloud auth login'"
        exit 1
    fi
    
    # Check if project is set correctly
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
    if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
        log_warning "Current project is '$CURRENT_PROJECT', setting to '$PROJECT_ID'"
        gcloud config set project $PROJECT_ID
    fi
    
    log_success "Prerequisites check passed"
}

# Enable required APIs
enable_apis() {
    log_info "Enabling required Google Cloud APIs..."
    
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        firestore.googleapis.com \
        storage.googleapis.com \
        --quiet
    
    log_success "APIs enabled successfully"
}

# Deploy backend service
deploy_backend() {
    log_info "Deploying backend service..."
    
    cd backend
    
    gcloud run deploy $BACKEND_SERVICE \
        --source . \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 1 \
        --max-instances 10 \
        --port 8000 \
        --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
        --quiet
    
    cd ..
    
    log_success "Backend deployed successfully"
}

# Get backend URL
get_backend_url() {
    log_info "Getting backend service URL..."
    
    BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE \
        --region=$REGION \
        --format='value(status.url)')
    
    if [ -z "$BACKEND_URL" ]; then
        log_error "Failed to get backend URL"
        exit 1
    fi
    
    log_success "Backend URL: $BACKEND_URL"
    echo "$BACKEND_URL"
}

# Configure frontend environment
configure_frontend() {
    local backend_url=$1
    log_info "Configuring frontend environment..."
    
    # Create production environment file
    cd frontend
    echo "REACT_APP_API_URL=$backend_url" > .env.production
    log_success "Frontend environment configured"
    cd ..
}

# Deploy frontend service
deploy_frontend() {
    log_info "Deploying frontend service..."
    
    cd frontend
    
    gcloud run deploy $FRONTEND_SERVICE \
        --source . \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory 1Gi \
        --cpu 1 \
        --max-instances 5 \
        --port 3000 \
        --quiet
    
    cd ..
    
    log_success "Frontend deployed successfully"
}

# Get frontend URL
get_frontend_url() {
    log_info "Getting frontend service URL..."
    
    FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE \
        --region=$REGION \
        --format='value(status.url)')
    
    if [ -z "$FRONTEND_URL" ]; then
        log_error "Failed to get frontend URL"
        exit 1
    fi
    
    log_success "Frontend URL: $FRONTEND_URL"
    echo "$FRONTEND_URL"
}

# Verify deployment
verify_deployment() {
    local backend_url=$1
    local frontend_url=$2
    
    log_info "Verifying deployment..."
    
    # Test backend health endpoint
    log_info "Testing backend health endpoint..."
    if curl -f -s "$backend_url/api/health" > /dev/null; then
        log_success "Backend health check passed"
    else
        log_warning "Backend health check failed - service may still be starting"
    fi
    
    # Test frontend
    log_info "Testing frontend..."
    if curl -f -s "$frontend_url" > /dev/null; then
        log_success "Frontend health check passed"
    else
        log_warning "Frontend health check failed - service may still be starting"
    fi
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."
    
    # Remove frontend environment file
    if [ -f "frontend/.env.production" ]; then
        rm -f frontend/.env.production
        log_info "Removed frontend/.env.production"
    fi
}

# Main deployment function
main() {
    echo "🚀 MyNutriAI Deployment Script"
    echo "================================"
    echo "Project: $PROJECT_ID"
    echo "Region: $REGION"
    echo "================================"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Enable APIs
    enable_apis
    
    # Deploy backend
    deploy_backend
    
    # Get backend URL
    BACKEND_URL=$(get_backend_url)
    
    # Configure frontend with backend URL
    configure_frontend "$BACKEND_URL"
    
    # Deploy frontend
    deploy_frontend
    
    # Get frontend URL
    FRONTEND_URL=$(get_frontend_url)
    
    # Verify deployment
    verify_deployment "$BACKEND_URL" "$FRONTEND_URL"
    
    # Cleanup
    cleanup
    
    # Success message
    echo ""
    echo "🎉 MyNutriAI deployed successfully!"
    echo "=================================="
    echo "Frontend URL: $FRONTEND_URL"
    echo "Backend URL:  $BACKEND_URL"
    echo "=================================="
    echo ""
    echo "📝 Next Steps:"
    echo "1. Visit the frontend URL to test the application"
    echo "2. Check the backend health: $BACKEND_URL/api/health"
    echo "3. Monitor the services in the Google Cloud Console"
    echo ""
    echo "📚 Useful Commands:"
    echo "• View logs: gcloud run services logs read $FRONTEND_SERVICE --region=$REGION"
    echo "• Update service: Re-run this script"
    echo "• Delete services: gcloud run services delete $FRONTEND_SERVICE --region=$REGION"
    echo ""
}

# Error handling
trap 'log_error "Deployment failed. Check the error messages above."' ERR

# Run main function
main "$@" 