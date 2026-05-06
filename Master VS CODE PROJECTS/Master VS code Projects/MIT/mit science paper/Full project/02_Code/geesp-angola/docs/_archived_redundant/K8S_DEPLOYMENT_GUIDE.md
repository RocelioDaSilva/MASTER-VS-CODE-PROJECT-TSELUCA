# Kubernetes Deployment & Auto-Scaling Guide for GEESP-Angola

## Overview

This guide provides comprehensive instructions for deploying GEESP-Angola to Kubernetes with automatic scaling capabilities. The deployment includes:

- **API Service**: FastAPI backend with 2-10 replicas based on demand
- **Auto-scaling**: CPU, memory, and request-rate based (Horizontal Pod Autoscaler)
- **Resource Management**: VPA for resource optimization
- **Monitoring**: Prometheus metrics integration with alerting
- **High Availability**: Pod disruption budgets, anti-affinity policies
- **Security**: Network policies, RBAC, TLS encryption
- **Health Checks**: Liveness and readiness probes

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL TRAFFIC                             │
│                                                                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
               ┌─────────────────────┐
               │  Ingress Controller │ (nginx)
               │  (TLS termination)  │
               └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ geesp-  │  │ geesp-  │  │ geesp-  │
    │ api-1   │  │ api-2   │  │ api-3   │
    └─────────┘  └─────────┘  └─────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                 ┌───────▼────────┐
                 │  Service       │
                 │  geesp-api     │
                 └────────────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │  PostgreSQL    │
                 │  Database      │
                 └────────────────┘

   ┌──────────────────────────────────┐
   │     Monitoring & Auto-Scaling    │
   ├──────────────────────────────────┤
   │ • Prometheus (metrics)           │
   │ • Metrics-Server (resource info) │
   │ • HPA (CPU/Memory/Requests)      │
   │ • VPA (resource optimization)    │
   └──────────────────────────────────┘
```

## Prerequisites

### 1. Kubernetes Cluster

Minimum requirements:
- **Version**: 1.19+ (tested with 1.22-1.27)
- **Nodes**: 3+ nodes recommended
- **Resources**: 4+ CPU cores, 8GB RAM minimum per node

### 2. Install Required Components

#### Metrics Server (required for HPA)

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify installation
kubectl get deployment metrics-server -n kube-system
```

#### Prometheus (required for custom metrics & monitoring)

```bash
# Install Prometheus Operator
kubectl apply -f https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.68.1/bundle.yaml

# Install Prometheus Stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

#### Ingress Controller (nginx recommended)

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace \
  --set controller.metrics.enabled=true
```

#### Cert-Manager (for TLS certificates)

```bash
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

### 3. Database Setup

Create PostgreSQL database (or use managed service):

```bash
# Example using Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql -n geesp-angola --create-namespace \
  --set auth.username=geesp_admin \
  --set auth.password=your_secure_password \
  --set auth.database=geesp_imon \
  --set primary.persistence.size=10Gi
```

## Deployment Steps

### Step 1: Prepare Configuration

**Update placeholders in `geesp-deployment.yaml`:**

```bash
# Edit deployment file
nano k8s/geesp-deployment.yaml

# Key sections to update:
# 1. Image location (spec.template.spec.containers[0].image)
# 2. Database credentials in geesp-db-secret
# 3. Ingress hostname (change geesp-angola.example.com)
# 4. Resource limits based on your cluster capacity
```

**Create database secret:**

```bash
kubectl create secret generic geesp-db-secret \
  --from-literal=db_host=postgres.geesp-angola.svc.cluster.local \
  --from-literal=db_port=5432 \
  --from-literal=db_name=geesp_imon \
  --from-literal=db_user=geesp_admin \
  --from-literal=db_password='your_secure_password' \
  -n geesp-angola
```

### Step 2: Build & Push Docker Image

```bash
# Build image
docker build -t geesp-angola:v1.0 .

# Push to registry
docker tag geesp-angola:v1.0 your-registry/geesp-angola:v1.0
docker push your-registry/geesp-angola:v1.0

# Update image in deployment
kubectl set image deployment/geesp-api geesp-api=your-registry/geesp-angola:v1.0 \
  -n geesp-angola
```

### Step 3: Deploy Application

```bash
# Apply all manifests
kubectl apply -f k8s/geesp-deployment.yaml

# Verify deployment
kubectl get all -n geesp-angola
kubectl describe deployment geesp-api -n geesp-angola

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=geesp -n geesp-angola --timeout=300s
```

### Step 4: Configure TLS Certificate

```bash
# Create ClusterIssuer for Let's Encrypt
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@geesp-angola.example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Certificate will be automatically created and renewed
kubectl get certificate -n geesp-angola
```

## Auto-Scaling Configuration

### CPU-Based Scaling

The primary HPA scales based on CPU utilization:
- **Min replicas**: 2
- **Max replicas**: 10
- **Target CPU**: 70% per pod
- **Scale Up**: +100% every 15 seconds
- **Scale Down**: -50% every 60 seconds (stabilization: 5 min)

### Memory-Based Scaling

Secondary scaling rule (slower):
- **Target Memory**: 80% per pod
- **Enabled when**: CPU scaling is insufficient

### Request-Rate Based Scaling (Custom Metrics)

Optional scaling based on HTTP requests/second:
- **Requirement**: Prometheus + custom metrics server
- **Target**: 100 requests/second per pod
- **Configuration**: In `geesp-api-hpa-requests`

### Resource Limits

Each pod has:
- **Request (guaranteed)**: 500m CPU, 512Mi memory
- **Limit (cap)**: 2000m CPU, 2Gi memory

These prevent "noisy neighbor" problems and enable predictable scaling.

### Monitoring Scaling Events

```bash
# Watch HPA status in real-time
kubectl get hpa -n geesp-angola -w

# Detailed HPA status
kubectl describe hpa geesp-api-hpa-cpu -n geesp-angola

# View scaling events
kubectl get events -n geesp-angola --sort-by='.lastTimestamp'

# Check pod metrics
kubectl top pods -n geesp-angola
kubectl top nodes
```

### Testing Auto-Scaling

Generate load to trigger scaling:

```bash
# Install load testing tool
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/test/images/load-generator/load-generator.yaml

# Get pod name
LOAD_POD=$(kubectl get pod -l app=load-generator -o jsonpath='{.items[0].metadata.name}')

# Generate sustained load
kubectl exec -it $LOAD_POD -- sh
# Inside pod: while true; do curl http://geesp-api.geesp-angola.svc.cluster.local/api/mcda; done

# Watch scaling happen
kubectl get hpa -n geesp-angola -w
kubectl get pods -n geesp-angola -w
```

## Monitoring & Alerts

### View Metrics in Prometheus

```bash
# Port-forward to Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring

# Access at: http://localhost:9090

# Example queries:
# - rate(http_requests_total{job="geesp-api"}[5m])
# - histogram_quantile(0.95, http_request_duration_seconds_bucket)
# - container_memory_usage_bytes{pod=~"geesp-api.*"}
```

### View Alerts

```bash
# Port-forward to Alertmanager
kubectl port-forward svc/prometheus-kube-prometheus-alertmanager 9093:9093 -n monitoring

# Access at: http://localhost:9093

# View active alerts
kubectl get prometheus -n geesp-angola
```

### Key Metrics to Monitor

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| High Error Rate | >5% errors | Page on-call engineer |
| High Response Time | p95 > 1s | Scale up or investigate |
| Pod Restarts | >3 in 15min | Investigate logs |
| Pod Evictions | > 0 | Increase node resources |
| DB Connection Errors | > 0 sustained | Check database |

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n geesp-angola

# Check logs
kubectl logs <pod-name> -n geesp-angola
kubectl logs <pod-name> -n geesp-angola --previous  # Crashed pod logs

# Check events
kubectl get events -n geesp-angola --sort-by='.lastTimestamp'
```

### HPA not scaling

```bash
# Check HPA status
kubectl describe hpa geesp-api-hpa-cpu -n geesp-angola

# Common causes:
# 1. Metrics Server not installed
kubectl get deployment metrics-server -n kube-system

# 2. Pods don't have resource requests
kubectl get pod <pod-name> -n geesp-angola -o yaml | grep -A 5 resources

# 3. Metrics not available yet (wait 1-2 minutes after deployment)
kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/geesp-angola/pods
```

### Database connection issues

```bash
# Test connectivity from pod
kubectl run -it --rm debug --image=alpine --restart=Never -n geesp-angola -- sh
# Inside pod: telnet postgres.geesp-angola.svc.cluster.local 5432

# Check database secret
kubectl get secret geesp-db-secret -n geesp-angola -o yaml

# Test with psql
kubectl run -it --rm debug --image=postgres:14 --restart=Never -n geesp-angola -- \
  psql -h postgres.geesp-angola.svc.cluster.local -U geesp_admin -d geesp_imon
```

### High memory usage

```bash
# Check memory allocation
kubectl top pods -n geesp-angola --sort-by=memory

# Check VPA recommendations
kubectl describe vpa geesp-api-vpa -n geesp-angola

# Increase limits if needed
kubectl set resources deployment geesp-api -n geesp-angola \
  --limits=cpu=4000m,memory=4Gi \
  --requests=cpu=1000m,memory=1Gi
```

## Maintenance

### Update Application

```bash
# Update image and trigger rollout
kubectl set image deployment/geesp-api \
  geesp-api=your-registry/geesp-angola:v1.1 \
  -n geesp-angola

# Monitor rollout
kubectl rollout status deployment/geesp-api -n geesp-angola

# Rollback if needed
kubectl rollout undo deployment/geesp-api -n geesp-angola
```

### Backup Database

```bash
# Backup Database
kubectl exec -i $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}' -n geesp-angola) \
  -n geesp-angola -- pg_dump -U geesp_admin geesp_imon > backup.sql

# Restore Database
kubectl cp backup.sql $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}' -n geesp-angola):/tmp/
kubectl exec $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}' -n geesp-angola) \
  -n geesp-angola -- psql -U geesp_admin geesp_imon < /tmp/backup.sql
```

### Scale Manual Adjustments

```bash
# Adjust min/max replicas
kubectl patch hpa geesp-api-hpa-cpu -n geesp-angola -p \
  '{"spec":{"minReplicas":3,"maxReplicas":15}}'

# Disable HPA (manual scaling)
kubectl patch hpa geesp-api-hpa-cpu -n geesp-angola -p \
  '{"spec":{"minReplicas":2,"maxReplicas":2}}'
```

## Performance Tuning

### Optimize Resource Requests/Limits

1. Monitor actual usage for 1-2 weeks
2. Set requests to observed p95 usage
3. Set limits to 1.5x-2x of requests
4. Let VPA fine-tune

### Enable Request-Rate Scaling

1. Install Prometheus custom metrics adapter
2. Uncomment `geesp-api-hpa-requests` manifest
3. Tune `averageValue` based on typical load

### Database Optimization

```bash
# Check slow queries
kubectl exec -it $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}' -n geesp-angola) \
  -n geesp-angola -- psql -U geesp_admin geesp_imon -c \
  "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10"
```

## Production Checklist

- [ ] Cluster meets minimum requirements (3+ nodes, 4+ CPU, 8GB RAM)
- [ ] All prerequisites installed (metrics-server, prometheus, ingress, cert-manager)
- [ ] Database created and accessible
- [ ] Docker image built and pushed to registry
- [ ] TLS certificate configured
- [ ] Resource limits appropriate for your cluster
- [ ] HPA min/max replicas tuned for expected load
- [ ] Monitoring dashboards created
- [ ] Alert thresholds set and tested
- [ ] Backup strategy implemented
- [ ] Load testing performed and scaling verified
- [ ] Documentation accessible to ops team

## Cost Optimization

### Remove Non-Essential Components

```bash
# Remove VPA if not needed
kubectl delete vpa geesp-api-vpa -n geesp-angola

# Remove custom metrics HPA if using CPU/memory only
kubectl delete hpa geesp-api-hpa-requests -n geesp-angola
```

### Adjust Resource Requests

Reduce requests to lower cost (but maintain reliability):

```bash
kubectl set resources deployment geesp-api -n geesp-angola \
  --requests=cpu=250m,memory=256Mi
```

### Enable Spot Instances

In cloud providers (AWS, GCP, Azure), use spot/preemptible instances for non-critical workloads:

```bash
# Configure node affinity for spot instances
nodeAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
  - weight: 100
    preference:
      matchExpressions:
      - key: cloud.google.com/gke-preemptible
        operator: In
        values: ["true"]
```

## Support & References

- [Kubernetes HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
- [Ingress-Nginx](https://kubernetes.github.io/ingress-nginx/)
- [Cert-Manager](https://cert-manager.io/)

## Changelog

### v1.0 (2026-02-10)
- Initial deployment manifests
- CPU and memory-based auto-scaling
- Prometheus metrics integration
- TLS certificate automation
- High availability configuration
- Security policies (RBAC, network policies)
