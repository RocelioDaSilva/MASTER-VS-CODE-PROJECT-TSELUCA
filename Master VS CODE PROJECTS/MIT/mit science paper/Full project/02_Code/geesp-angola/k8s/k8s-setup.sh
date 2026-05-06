#!/bin/bash
# ============================================================================
# GEESP-Angola Kubernetes Deployment Setup Script
# Automated installation and configuration of all required components
# ============================================================================

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    log_success "$1 is installed"
    return 0
}

# ============================================================================
# PHASE 1: PREREQUISITES CHECK
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 1: Prerequisites"
log_info "=========================================="

# Check for required tools
log_info "Checking for required tools..."
REQUIRED_TOOLS=("kubectl" "helm" "docker")
MISSING_TOOLS=0

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! check_command "$tool"; then
        MISSING_TOOLS=$((MISSING_TOOLS + 1))
    fi
done

if [ $MISSING_TOOLS -gt 0 ]; then
    log_error "Please install missing tools before proceeding"
    exit 1
fi

# Check kubectl connectivity
log_info "Checking Kubernetes cluster connectivity..."
if kubectl cluster-info &> /dev/null; then
    CLUSTER_NAME=$(kubectl config current-context)
    log_success "Connected to cluster: $CLUSTER_NAME"
else
    log_error "Cannot connect to Kubernetes cluster. Please configure kubectl."
    exit 1
fi

# Check Kubernetes version
K8S_VERSION=$(kubectl version --short | grep Server | awk '{print $3}' | cut -d'.' -f1-2)
log_success "Kubernetes version: $K8S_VERSION"

# Check node count and resources
NODE_COUNT=$(kubectl get nodes | tail -n +2 | wc -l)
if [ "$NODE_COUNT" -lt 2 ]; then
    log_warning "Found only $NODE_COUNT nodes. Recommended: 3+ nodes for HA"
else
    log_success "Found $NODE_COUNT nodes"
fi

# ============================================================================
# PHASE 2: NAMESPACE & RBAC
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 2: Namespace & RBAC"
log_info "=========================================="

NAMESPACE="geesp-angola"

log_info "Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
log_success "Namespace created"

# ============================================================================
# PHASE 3: INSTALL METRICS SERVER
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 3: Metrics Server"
log_info "=========================================="

if kubectl get deployment metrics-server -n kube-system &> /dev/null; then
    log_warning "Metrics Server already installed"
else
    log_info "Installing Metrics Server (required for HPA)..."
    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
    
    # Wait for metrics-server to be ready
    kubectl wait --for=condition=available --timeout=300s deployment/metrics-server -n kube-system
    log_success "Metrics Server installed and ready"
fi

# ============================================================================
# PHASE 4: INSTALL PROMETHEUS (optional)
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 4: Prometheus (Optional)"
log_info "=========================================="

read -p "Install Prometheus for monitoring? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Adding Prometheus Helm repository..."
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    
    log_info "Installing Prometheus Stack..."
    helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
        --namespace monitoring \
        --create-namespace \
        --values - <<EOF
prometheus:
  prometheusSpec:
    retention: 30d
    resources:
      requests:
        cpu: 250m
        memory: 512Mi
    externalLabels:
      cluster: geesp-angola
grafana:
  adminPassword: admin
  persistence:
    enabled: true
    size: 10Gi
EOF
    
    log_success "Prometheus Stack installed"
    log_info "Grafana will be available at: kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
else
    log_warning "Skipping Prometheus installation"
fi

# ============================================================================
# PHASE 5: INSTALL INGRESS NGINX
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 5: Ingress Controller"
log_info "=========================================="

if helm list -n ingress-nginx 2>/dev/null | grep ingress-nginx &> /dev/null; then
    log_warning "Ingress NGINX already installed"
else
    log_info "Adding Ingress NGINX Helm repository..."
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    
    log_info "Installing Ingress NGINX..."
    helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
        --namespace ingress-nginx \
        --create-namespace \
        --set controller.metrics.enabled=true \
        --set controller.service.type=LoadBalancer \
        --wait
    
    log_success "Ingress NGINX installed"
    log_info "Getting ingress IP/hostname..."
    kubectl get service -n ingress-nginx ingress-nginx-controller -w
fi

# ============================================================================
# PHASE 6: INSTALL CERT-MANAGER
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 6: Cert-Manager (TLS)"
log_info "=========================================="

read -p "Install Cert-Manager for Let's Encrypt TLS? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if helm list -n cert-manager 2>/dev/null | grep cert-manager &> /dev/null; then
        log_warning "Cert-Manager already installed"
    else
        log_info "Adding Cert-Manager repository..."
        helm repo add jetstack https://charts.jetstack.io
        helm repo update
        
        log_info "Installing Cert-Manager..."
        helm upgrade --install cert-manager jetstack/cert-manager \
            --namespace cert-manager \
            --create-namespace \
            --set installCRDs=true \
            --wait
        
        log_success "Cert-Manager installed"
        
        # Create ClusterIssuer for Let's Encrypt
        log_info "Creating Let's Encrypt issuer..."
        kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: noreply@geesp-angola.example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: noreply@geesp-angola.example.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
        log_success "Let's Encrypt issuers created"
    fi
else
    log_warning "Skipping Cert-Manager installation"
fi

# ============================================================================
# PHASE 7: CONFIGURE DATABASE SECRET
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 7: Database Configuration"
log_info "=========================================="

read -p "Configure database credentials? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Database host (default: postgres.geesp-angola.svc.cluster.local): " DB_HOST
    DB_HOST=${DB_HOST:-postgres.geesp-angola.svc.cluster.local}
    
    read -p "Database port (default: 5432): " DB_PORT
    DB_PORT=${DB_PORT:-5432}
    
    read -p "Database name (default: geesp_imon): " DB_NAME
    DB_NAME=${DB_NAME:-geesp_imon}
    
    read -p "Database user (default: geesp_admin): " DB_USER
    DB_USER=${DB_USER:-geesp_admin}
    
    read -sp "Database password: " DB_PASSWORD
    echo
    
    log_info "Creating database secret..."
    kubectl create secret generic geesp-db-secret \
        --from-literal=db_host=$DB_HOST \
        --from-literal=db_port=$DB_PORT \
        --from-literal=db_name=$DB_NAME \
        --from-literal=db_user=$DB_USER \
        --from-literal=db_password=$DB_PASSWORD \
        -n $NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "Database secret created"
else
    log_warning "Skipping database configuration (will use defaults)"
fi

# ============================================================================
# PHASE 8: DEPLOY APPLICATION
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 8: Deploy Application"
log_info "=========================================="

read -p "Deploy GEESP application? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Docker image (format: registry/name:tag): " DOCKER_IMAGE
    
    if [ -z "$DOCKER_IMAGE" ]; then
        log_error "Docker image is required"
        exit 1
    fi
    
    log_info "Deploying application with image: $DOCKER_IMAGE"
    
    # Apply deployment manifest (assuming it's in current directory)
    if [ -f "geesp-deployment.yaml" ]; then
        # Update image in manifest
        sed "s|image: geesp-angola:v1.0|image: $DOCKER_IMAGE|g" geesp-deployment.yaml | kubectl apply -f -
        log_success "Application deployment started"
        
        # Wait for deployment to be ready
        log_info "Waiting for deployment to be ready..."
        kubectl wait --for=condition=available --timeout=600s deployment/geesp-api -n $NAMESPACE
        log_success "Deployment is ready!"
    else
        log_error "geesp-deployment.yaml not found in current directory"
        exit 1
    fi
else
    log_warning "Skipping application deployment"
fi

# ============================================================================
# PHASE 9: VERIFICATION & SUMMARY
# ============================================================================

log_info "=========================================="
log_info "GEESP-Angola K8s Setup - Phase 9: Verification"
log_info "=========================================="

log_info "Verifying installation..."

# Check pods
log_info "Checking GEESP pods:"
kubectl get pods -n $NAMESPACE

# Check services
log_info "Checking services:"
kubectl get svc -n $NAMESPACE

# Check HPA
log_info "Checking HPA status:"
kubectl get hpa -n $NAMESPACE

# Check ingress
log_info "Checking ingress:"
kubectl get ingress -n $NAMESPACE

# ============================================================================
# FINAL SUMMARY
# ============================================================================

log_info "=========================================="
log_success "GEESP-Angola K8s Setup Complete!"
log_info "=========================================="

echo ""
echo "Next steps:"
echo "1. Update Ingress hostname:"
echo "   kubectl patch ingress geesp-ingress -n $NAMESPACE --type merge -p '{\"spec\":{\"rules\":[{\"host\":\"your-domain.com\"}]}}'"
echo ""
echo "2. Monitor deployment:"
echo "   kubectl get pods -n $NAMESPACE -w"
echo ""
echo "3. View logs:"
echo "   kubectl logs -f deployment/geesp-api -n $NAMESPACE"
echo ""
echo "4. Access application:"
echo "   kubectl port-forward svc/geesp-api 8000:80 -n $NAMESPACE"
echo "   Then visit: http://localhost:8000"
echo ""
echo "5. Scale application manually:"
echo "   kubectl scale deployment geesp-api --replicas=5 -n $NAMESPACE"
echo ""
echo "6. View HPA status:"
echo "   kubectl describe hpa geesp-api-hpa-cpu -n $NAMESPACE"
echo ""

if kubectl get deployment metrics-server -n kube-system &> /dev/null; then
    echo "7. Monitor resource usage:"
    echo "   kubectl top nodes"
    echo "   kubectl top pods -n $NAMESPACE"
    echo ""
fi

if helm list -n monitoring 2>/dev/null | grep prometheus &> /dev/null; then
    echo "8. Access Prometheus:"
    echo "   kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090"
    echo "   Then visit: http://localhost:9090"
    echo ""
    echo "9. Access Grafana:"
    echo "   kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
    echo "   Then visit: http://localhost:3000 (default: admin/admin)"
    echo ""
fi

log_info "For detailed documentation, see: K8S_DEPLOYMENT_GUIDE.md"
