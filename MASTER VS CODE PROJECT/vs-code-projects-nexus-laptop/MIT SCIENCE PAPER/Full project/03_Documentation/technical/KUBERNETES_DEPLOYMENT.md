# Kubernetes Deployment Guide for GEESP-Angola

## Overview

This guide covers deploying GEESP-Angola to Kubernetes clusters (local or cloud).

## Prerequisites

- Kubernetes cluster (v1.19+ recommended)
- `kubectl` configured to access your cluster
- Docker image available in registry or local
- Persistent storage provisioner (local, NFS, cloud storage, etc.)

### Install kubectl

```bash
# macOS
brew install kubectl

# Ubuntu/Debian
sudo apt-get install -y kubectl

# Windows (with Chocolatey)
choco install kubernetes-cli
```

## Cluster Setup (Local)

### Option 1: Docker Desktop Kubernetes

```bash
# Enable Kubernetes in Docker Desktop
# Preferences → Kubernetes → Enable Kubernetes
# Then verify:
kubectl cluster-info
```

### Option 2: Minikube

```bash
# Install Minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --cpus=4 --memory=8192 --disk-size=50g

# Enable ingress addon
minikube addons enable ingress

# Get IP for service access
minikube service geesp-app -n geesp-production --url
```

### Option 3: Kind (Kubernetes in Docker)

```bash
# Install Kind
curl -Lo ./kind https://github.com/kubernetes-sigs/kind/releases/latest/download/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster --name geesp-dev

# Set context
kubectl cluster-info --context kind-geesp-dev
```

## Deployment Steps

### 1. Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace geesp-production

# Create database credentials secret
kubectl create secret generic geesp-database-credentials \
  --from-literal=db-user=geesp_app \
  --from-literal=db-password=$(openssl rand -base64 32) \
  --from-literal=redis-password=$(openssl rand -base64 32) \
  -n geesp-production

# (Or apply from YAML if secrets already defined)
kubectl apply -f k8s/geesp-app-deployment.yaml
```

### 2. Configure Docker Registry Access (if needed)

```bash
# For private Docker registry
kubectl create secret docker-registry geesp-registry-credentials \
  --docker-server=registry.example.com \
  --docker-username=your_user \
  --docker-password=your_password \
  --docker-email=your_email@example.com \
  -n geesp-production
```

### 3. Apply PostgreSQL StatefulSet

```bash
# Create storage class (if not using defaults)
kubectl apply -f k8s/geesp-postgres-statefulset.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres \
  -n geesp-production --timeout=300s

# Verify database is running
kubectl get pods -n geesp-production
```

### 4. Apply Application Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Wait for rollout
kubectl rollout status deployment/geesp-app -n geesp-production

# Check pod status
kubectl get pods -n geesp-production
```

### 5. Expose and Access Application

```bash
# Get service endpoint
kubectl get svc geesp-app -n geesp-production

# For LoadBalancer type (cloud)
EXTERNAL_IP=$(kubectl get svc geesp-app -n geesp-production -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Access at: http://$EXTERNAL_IP:8501"

# For local cluster without LoadBalancer
kubectl port-forward svc/geesp-app 8501:8501 -n geesp-production
# Then access: http://localhost:8501
```

## Ingress Setup (for HTTPS and custom domains)

### Install NGINX Ingress Controller

```bash
# For cloud clusters
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/cloud/deploy.yaml

# For Minikube
minikube addons enable ingress

# Verify installation
kubectl wait --namespace ingress-nginx --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### Install Cert-Manager for TLS

```bash
# Install Cert-Manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml

# Wait for CRDs
kubectl wait --for=condition=established --timeout=60s \
  crd/issuers.cert-manager.io crd/certificates.cert-manager.io

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Apply Ingress with TLS

```bash
cat > ingress.yaml <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: geesp-app-ingress
  namespace: geesp-production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - geesp-app.your-domain.com
    secretName: geesp-app-tls
  rules:
  - host: geesp-app.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: geesp-app
            port:
              number: 8501
EOF

kubectl apply -f ingress.yaml
```

## Monitoring Setup

### Apply Prometheus Operator (optional)

```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus Operator
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# http://localhost:9090

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# http://localhost:3000 (admin/prom-operator)
```

## Scaling and Management

### Scale Application Replicas

```bash
# Manual scaling
kubectl scale deployment geesp-app -n geesp-production --replicas=5

# Check scaling
kubectl get deployment geesp-app -n geesp-production
kubectl get pods -n geesp-production
```

### Horizontal Pod Autoscaler

The HPA is already configured in the deployment manifest:

```bash
# Check HPA status
kubectl get hpa -n geesp-production

# Watch autoscaling
kubectl get hpa -n geesp-production -w
```

### Update Deployment (Rolling Updates)

```bash
# Update image
kubectl set image deployment/geesp-app \
  geesp-app=geesp-app:v1.1.0 \
  -n geesp-production

# Monitor rollout
kubectl rollout status deployment/geesp-app -n geesp-production

# Rollback if needed
kubectl rollout undo deployment/geesp-app -n geesp-production
```

## Logging and Debugging

### View Logs

```bash
# Tail logs from all pods
kubectl logs -f deployment/geesp-app -n geesp-production --all-containers=true

# Logs from specific pod
kubectl logs pod-name -n geesp-production -f

# Logs from previous crashed container
kubectl logs pod-name -n geesp-production --previous
```

### Execute Commands in Pod

```bash
# Get shell access
kubectl exec -it pod-name -n geesp-production -- /bin/bash

# Run one-off command
kubectl exec pod-name -n geesp-production -- python -c "import sys; print(sys.version)"
```

### Describe Resources

```bash
# Detailed pod info
kubectl describe pod pod-name -n geesp-production

# Deployment status
kubectl describe deployment geesp-app -n geesp-production

# Check events
kubectl get events -n geesp-production --sort-by='.lastTimestamp'
```

## Backup and Recovery

### Database Backup (on-demand)

```bash
# Create backup job
kubectl create job postgres-backup-$(date +%s) \
  --from=cronjob/postgres-backup \
  -n geesp-production

# Verify backup
kubectl logs -f job/postgres-backup-* -n geesp-production
```

### Backup All Resources

```bash
# Export namespace
kubectl get all -n geesp-production -o yaml > geesp-backup.yaml

# Export specific resources
kubectl get deployment,statefulset,service,pvc \
  -n geesp-production -o yaml > geesp-resources-backup.yaml
```

### Restore from Backup

```bash
# Restore namespace
kubectl apply -f geesp-backup.yaml

# Restore specific resources
kubectl apply -f geesp-resources-backup.yaml
```

## Troubleshooting

### Pod Stuck in Pending

```bash
# Check events
kubectl describe pod pod-name -n geesp-production

# Common causes:
# - PVC not bound: check storage class and PV availability
# - Resource constraints: check node resources
# - Image pull error: check image and registry credentials

# Check node resources
kubectl top nodes
kubectl describe nodes
```

### CrashLoopBackOff

```bash
# Check logs
kubectl logs pod-name -n geesp-production --tail=50

# Describe for exit code
kubectl describe pod pod-name -n geesp-production

# Check limits
kubectl get resource quota -n geesp-production
```

### Database Connection Issues

```bash
# Test connectivity from app pod
kubectl exec -it deployment/geesp-app -n geesp-production \
  -- nc -zv postgres.geesp-production.svc.cluster.local 5432

# Check DNS resolution
kubectl exec -it deployment/geesp-app -n geesp-production \
  -- nslookup postgres.geesp-production.svc.cluster.local
```

## Cleanup

```bash
# Delete deployment (keeps PVCs)
kubectl delete deployment geesp-app -n geesp-production

# Delete everything in namespace
kubectl delete namespace geesp-production

# Delete with PVCs
kubectl delete pvc --all -n geesp-production

# Delete entire cluster (Minikube)
minikube delete
```

## Advanced Topics

### Blue-Green Deployment

```bash
# Deploy v2 alongside v1
kubectl apply -f geesp-app-v2-deployment.yaml

# Switch traffic when ready
kubectl patch service geesp-app -p '{"spec":{"selector":{"version":"v2"}}}'

# Delete v1
kubectl delete deployment geesp-app-v1
```

### Canary Deployment with Istio

See [Istio Canary Deployment Guide](https://istio.io/latest/docs/tasks/traffic-management/traffic-shifting/)

### Multi-Region Deployment

Deploy to multiple clusters and use:
- [Kubefed](https://kubernetes.io/docs/concepts/cluster-administration/federation/)
- [Linkerd Service Mesh](https://linkerd.io/)
- [Istio Multi-Cluster](https://istio.io/latest/docs/setup/install/multicluster/)

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [PostgreSQL on Kubernetes](https://www.postgresql.org/docs/current/runtime-config.html)
- [Helm Package Manager](https://helm.sh/)
