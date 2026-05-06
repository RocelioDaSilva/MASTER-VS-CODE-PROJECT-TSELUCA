# GEESP-Angola Operations Manual v2.0

**Complete reference for deploying, operating, and troubleshooting the GEESP-Angola platform**

**Last Updated**: February 2026 | **Status**: ✅ Production Ready | **Version**: 1.0.0

---

## Table of Contents

1. [Emergency Commands](#emergency-commands)
2. [Deployment Procedures](#deployment-procedures)
3. [Monitoring & Health Checks](#monitoring--health-checks)
4. [Troubleshooting](#troubleshooting)
5. [Database Operations](#database-operations)
6. [Performance Management](#performance-management)
7. [Security Operations](#security-operations)

---

## Emergency Commands

### System Status Check (5 seconds)
```bash
# Quick health check
kubectl get all -n geesp-angola
kubectl get hpa -n geesp-angola
kubectl top nodes
```

### Check for Errors (30 seconds)
```bash
# Recent errors
kubectl logs deployment/geesp-api -n geesp-angola | tail -50 | grep -i error

# Pod restarts
kubectl get pods -n geesp-angola -o json | \
  jq '.items[] | {name: .metadata.name, restarts: .status.containerStatuses[0].restartCount}'
```

### Scale Up Immediately (Emergency Load)
```bash
# Emergency scaling
kubectl scale deployment geesp-api -n geesp-angola --replicas=10

# Manual remediation
kubectl rollout restart deployment/geesp-api -n geesp-angola
```

### Database Connectivity Check
```bash
# Test database connection
kubectl exec -it deployment/geesp-api -n geesp-angola -- \
  python -c "from models.monitoring import get_database_manager; \
             db = get_database_manager(); \
             session = db.get_session(); \
             print('Database OK' if session else 'Database FAILED')"
```

### API Health Verification
```bash
# Port-forward and test
kubectl port-forward deployment/geesp-api 8000:8000 -n geesp-angola &
sleep 2
curl -s http://localhost:8000/health | jq .
kill %1
```

---

## Deployment Procedures

### Standard Production Deployment

**Prerequisites Check**:
```bash
# Verify cluster is ready
kubectl cluster-info
kubectl get nodes
kubectl get ns | grep geesp-angola

# Check available resources
kubectl describe nodes | grep -A5 "Allocated resources"
```

**One-Command Deployment** (Recommended):
```bash
cd geesp-angola
bash k8s/k8s-setup.sh
# Follow interactive prompts through 9 phases
```

**Manual Step-by-Step Deployment**:

1. **Build Docker Image**
   ```bash
   docker build -t geesp-angola:v1.0.0 .
   docker tag geesp-angola:v1.0.0 <registry>/geesp-angola:v1.0.0
   docker push <registry>/geesp-angola:v1.0.0
   ```

2. **Update Image Reference** (if not using setup script)
   ```bash
   # Edit k8s/geesp-deployment.yaml and update:
   # image: <registry>/geesp-angola:v1.0.0
   ```

3. **Create Namespaces & RBAC**
   ```bash
   kubectl apply -f k8s/geesp-deployment.yaml --dry-run=client
   kubectl create namespace geesp-angola
   kubectl apply -f k8s/geesp-deployment.yaml
   ```

4. **Verify Deployment**
   ```bash
   kubectl rollout status deployment/geesp-api -n geesp-angola -w
   kubectl get pods -n geesp-angola
   ```

5. **Configure TLS**
   ```bash
   # cert-manager auto-provision (if configured)
   kubectl get certificate -n geesp-angola
   kubectl describe certificate geesp-tls -n geesp-angola
   ```

6. **Verify Full Stack**
   ```bash
   # All components ready?
   kubectl get all -n geesp-angola
   
   # Check Ingress
   kubectl get ingress -n geesp-angola
   kubectl describe ingress geesp-ingress -n geesp-angola
   
   # Test endpoint
   curl -s https://geesp-api.example.com/health | jq .
   ```

### Rollback to Previous Version
```bash
# Quick rollback
kubectl rollout undo deployment/geesp-api -n geesp-angola

# Verify rollback
kubectl rollout status deployment/geesp-api -n geesp-angola -w
kubectl get pods -n geesp-angola
```

### Scheduled Maintenance Deployment
```bash
# Drain nodes (reschedule pods)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Perform maintenance

# Uncordon node
kubectl uncordon <node-name>

# Monitor rebalancing
kubectl get pods -A -w
```

---

## Monitoring & Health Checks

### Real-Time Monitoring Dashboard

**Watch Auto-Scaling** (Terminal 1):
```bash
kubectl get hpa -n geesp-angola -w
# Look for: TARGETS column showing CPU%, Replicas increasing/decreasing
```

**Watch Pod Status** (Terminal 2):
```bash
kubectl get pods -n geesp-angola -w
# Look for: All pods in "Running" state, Ready column "1/1"
```

**Stream Logs** (Terminal 3):
```bash
kubectl logs -f deployment/geesp-api -n geesp-Angola --all-containers=true
# Look for: No ERROR or CRITICAL messages
```

**Monitor Node Resources** (Terminal 4):
```bash
watch -n 2 'kubectl top nodes; echo "---"; kubectl top pods -n geesp-angola'
# Look for: Node CPU/Memory < 80%, Pod CPU < 70%
```

### Health Check Commands

**API Health**:
```bash
# Simple health check
curl -s http://geesp-api:8000/health | jq .

# Detailed health
curl -s http://geesp-api:8000/docs | head -20

# Database connection
curl -s http://geesp-api:8000/ready | jq .
```

**Pod Health**:
```bash
# Check probe status
kubectl get pods -n geesp-angola -o custom-columns=\
NAME:.metadata.name,\
READY:.status.conditions[?(@.type=='Ready')].status,\
ALIVE:.status.conditions[?(@.type=='Ready')].status

# Detailed pod health
kubectl describe pod <pod-name> -n geesp-angola | grep -A10 "Conditions\|Probe"
```

**Database Health**:
```bash
# Connection pool status
kubectl exec deployment/geesp-api -n geesp-angola -- \
  python -c "from models.monitoring import get_database_manager; \
             db = get_database_manager(); \
             print(f'DB healthy, pool size: {db.engine.pool.size}')"

# Record count
kubectl exec deployment/geesp-api -n geesp-Angola -- \
  python -c "from models.monitoring import get_database_manager; \
             session = get_database_manager().get_session(); \
             print(f'Projects: {session.query(...).count()}')"
```

**Resource Validation**:
```bash
# Pod resource requests vs actual usage
kubectl top pods -n geesp-angola -o custom-columns=\
NAME:.metadata.name,\
CPU_REQUEST:.spec.containers[0].resources.requests.cpu,\
CPU_ACTUAL:.usage.cpu,\
MEM_REQUEST:.spec.containers[0].resources.requests.memory,\
MEM_ACTUAL:.usage.memory

# Node resource availability
kubectl describe nodes | grep -A2 "Allocatable\|Allocated"
```

---

## Troubleshooting

### Issue: Pods Stuck in "Pending" State

**Symptoms**: `kubectl get pods -n geesp-angola` shows "Pending"

**Investigation**:
```bash
# Check pod details
kubectl describe pod <pod-name> -n geesp-angola

# Check events (last 10 lines look for warnings)
kubectl describe pod <pod-name> -n geesp-angola | tail -10

# Look for resource constraints
kubectl describe nodes | grep -A5 "Allocatable"
```

**Solutions**:
```bash
# No nodes available?
# Option 1: Scale up cluster
# Option 2: Reduce resource requests
kubectl set resources deployment/geesp-api -n geesp-angola \
  --requests=cpu=250m,memory=256Mi

# Scheduling conflict? Check node affinity
kubectl get pod <pod-name> -n geesp-angola -o yaml | grep -A5 "affinity"

# PVC not available?
kubectl get pvc -n geesp-angola
kubectl describe pvc -n geesp-angola
```

### Issue: High Pod CPU Usage (>90%)

**Symptoms**: `kubectl top pods` shows CPU near limits

**Investigation**:
```bash
# Which pod is high?
kubectl top pods -n geesp-angola --sort-by=cpu

# Check what's consuming CPU
kubectl exec <pod-name> -n geesp-angola -- \
  top -b -n1 | head -20

# Profile if available
kubectl exec <pod-name> -n geesp-angola -- \
  ps aux | grep -v grep
```

**Solutions**:
```bash
# Increase CPU limits
kubectl set resources deployment/geesp-api -n geesp-angola \
  --limits=cpu=2000m --requests=cpu=750m

# Restart pods to clear state
kubectl rollout restart deployment/geesp-api -n geesp-angola

# Check for memory leaks
# If persistent: redeploy or investigate application code

# Increase HPA max replicas
kubectl patch hpa geesp-api-hpa-cpu -n geesp-angelo --type merge \
  -p '{"spec":{"maxReplicas":15}}'
```

### Issue: High Memory Usage (>80%)

**Symptoms**: Dashboard shows memory pressure

**Investigation**:
```bash
# Memory usage by pod
kubectl top pods -n geesp-angola --sort-by=memory

# Check memory leaks over time
# Monitor dashboard or Prometheus:
# container_memory_usage_bytes for each pod
```

**Solutions**:
```bash
# Increase memory limits
kubectl set resources deployment/geesp-api -n geesp-angola \
  --limits=memory=2Gi --requests=memory=512Mi

# Clear cache (if applicable)
kubectl exec <pod-name> -n geesp-angola -- \
  python -c "from scripts.data_loaders_async import get_async_loader; \
             loader = get_async_loader(); \
             loader.clear_cache()"

# Restart pods
kubectl rollout restart deployment/geesp-api -n geesp-angola

# Check database connection pool
# May need to reduce pool size or scale out
```

### Issue: API Errors (HTTP 5xx responses)

**Symptoms**: Client errors or error logs

**Investigation**:
```bash
# Check recent errors
kubectl logs deployment/geesp-api -n geesp-angola | grep "ERROR\|CRITICAL"

# Specific error type
kubectl logs deployment/geesp-api -n geesp-angola | grep "Exception\|Traceback"

# Check application metrics (if Prometheus available)
# curl http://prometheus:9090/api/v1/query?query=http_requests_total
```

**Solutions**:
```bash
# Database connection issue?
kubectl logs deployment/geesp-api -n geesp-angola | grep "database\|connection"
# Fix: Verify database is accessible, check credentials

# Missing dependency?
kubectl logs deployment/geesp-api -n geesp-anglo | grep "ImportError\|ModuleNotFoundError"
# Fix: Rebuild Docker image, check dependencies

# Application bug?
# Check recent deployments:
kubectl rollout history deployment/geesp-api -n geesp-angola
# Rollback if needed:
kubectl rollout undo deployment/geesp-api -n geesp-angola

# Restart pods
kubectl rollout restart deployment/geesp-api -n geesp-congo
```

### Issue: HPA Not Scaling

**Symptoms**: `kubectl get hpa` shows "unknown" or replicas not changing under load

**Investigation**:
```bash
# Check HPA status
kubectl describe hpa geesp-api-hpa-cpu -n geesp-angola

# Check metrics availability
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes

# Verify metrics-server
kubectl get deployment -n kube-system metrics-server
kubectl logs -n kube-system deployment/metrics-server

# Check custom metrics (if using request-rate HPA)
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1
```

**Solutions**:
```bash
# Install metrics-server if missing
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server \
  -n kube-system --set args[0]="--kubelet-insecure-tls"

# Disable VPA if conflicting
kubectl get vpa -n geesp-angelo
kubectl delete vpa geesp-api-vpa -n geesp-angola

# Restart metrics-server
kubectl rollout restart deployment metrics-server -n kube-system

# Manual scaling alternative
kubectl scale deployment geesp-api -n geesp-angela --replicas=5
```

### Issue: Database Connection Failures

**Symptoms**: Database errors in logs, API returns 503

**Investigation**:
```bash
# Check database secret exists
kubectl get secret geesp-db-secret -n geesp-angola

# Verify database credentials
kubectl get secret geesp-db-secret -n geesp-angola -o jsonpath='{.data}' | base64 -d

# Test connectivity from pod
kubectl run -it --rm db-test --image=postgres:latest --restart=Never \
  -- psql -h <db-host> -U <user> -d geesp_angola -c "SELECT 1"

# Check database service endpoint
kubectl get service -n geesp-angelo | grep postgres
nslookup <database-host>
```

**Solutions**:
```bash
# Wrong credentials? Update secret
kubectl create secret generic geesp-db-secret \
  --from-literal=DB_HOST=<host> \
  --from-literal=DB_USER=<user> \
  --from-literal=DB_PASSWORD=<password> \
  -n geesp-angola --dry-run=client -o yaml | kubectl apply -f -

# Restart pods to pick up new secret
kubectl rollout restart deployment/geesp-api -n geesp-angola

# Network policy blocking connection?
kubectl get networkpolicy -n geesp-angola
kubectl describe networkpolicy -n geesp-angola

# Database down? Check database service
kubectl get endpoints <database-service>

# Connection pool exhausted?
# Reduce pool size or increase max connections in database config
```

---

## Database Operations

### Backup & Restore

**Daily Backup** (should be automated):
```bash
# Manual PostgreSQL backup
pg_dump -h <host> -U <user> -d geesp_angola > \
  geesp_backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
pg_dump -h <host> -U <user> -d geesp_angola | \
  gzip > geesp_backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Verify backup
gzip -t geesp_backup_*.sql.gz  # Returns 0 if valid
```

**Restore from Backup**:
```bash
# PostgreSQL restore
psql -h <host> -U <user> -d geesp_angola < geesp_backup.sql

# Restore from compressed backup
gunzip -c geesp_backup.sql.gz | psql -h <host> -U <user> -d geesp_socorro
```

### Database Queries

**Key Metrics**:
```sql
-- Total active projects
SELECT COUNT(*) FROM projects WHERE is_active = true;

-- Recent generation records
SELECT community, date, generation_kwh 
FROM daily_generation 
ORDER BY date DESC LIMIT 10;

-- Latest KPI snapshot
SELECT * FROM key_performance_indicator 
ORDER BY date DESC LIMIT 1;

-- System health status
SELECT community, health_score 
FROM system_health_metric 
ORDER BY date DESC, community;
```

**Maintenance**:
```sql
-- Table space analysis
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

-- Index analysis
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

-- Vacuum statistics
VACUUM ANALYZE;  -- Optimize performance
```

### Database Migrations

**Create New Migration**:
```bash
alembic revision --autogenerate -m "Add new_column to projects table"
```

**Review Migration**:
```bash
# Check migration content
cat migrations/versions/<timestamp>_<description>.py
```

**Apply Migration**:
```bash
# Test first (dry-run not available for alembic)
alembic upgrade +1  # Apply one migration

alembic upgrade head  # Apply all pending
```

**Rollback Migration**:
```bash
# Back one version
alembic downgrade -1

# Back to specific version
alembic downgrade <revision_id>

# Current version
alembic current
```

---

## Performance Management

### Performance Baselines

| Component | Metric | Target | Action if Exceeded |
|-----------|--------|--------|-------------------|
| API | GET /health latency | <10ms | Check pod CPU |
| API | POST /mcda latency | 50-200ms | Check database latency |
| API | POST /mcda/batch latency | 1-5s per 10 items | Scale up workers |
| Database | Query p95 | <100ms | Check indexes, scale up |
| Dashboard | Initial load | <3s | Check cache, optimize queries |
| Pod CPU | Utilization | <70% | Limit requests or scale up |
| Pod Memory | Utilization | <80% | Increase limits or scale up |

### Load Testing

**Baseline Load Test**:
```bash
# Install hey tool
go get -u github.com/rakyll/hey

# Load test API
hey -n 1000 -c 50 http://geesp-api:8000/health
hey -n 100 -c 10 -m POST -H "Content-Type: application/json" \
  -d '{"weights": {"solar": 0.35, "pop": 0.25, "dist": 0.2, "slope": 0.1, "ndvi": 0.1}}' \
  http://geesp-api:8000/mcda

# Monitor while testing
kubectl top pods -n geesp-anglo -w  # Terminal 2
kubectl get hpa -n geesp-congo -w  # Terminal 3
```

**Performance Analysis**:
```bash
# Check Prometheus for detailed metrics
kubectl port-forward -n prometheus prometheus-0 9090:9090
# Open: http://localhost:9090

# Key metrics to query:
# container_cpu_usage_seconds_total
# container_memory_usage_bytes
# http_request_duration_seconds
# http_requests_total
```

### Optimization Strategies

**If API is slow**:
```bash
# 1. Check database queries
# Add indexes for frequently queried columns
ALTER TABLE daily_generation ADD INDEX idx_project_date (project_id, date);

# 2. Enable caching
# The async loader has built-in caching, ensure it's enabled

# 3. Scale horizontally
kubectl scale deployment geesp-api -n geesp-congo --replicas=5

# 4. Profile application
# Use Python profiling tools to identify bottlenecks
```

**If database is slow**:
```bash
# 1. Analyze slowest queries
# Enable slow query log in PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

# View slow queries
-- Connect as superuser:
SELECT query, calls, mean_exec_time FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;

# 2. Add indexes
-- For high-frequency queries:
CREATE INDEX idx_generation_project_date ON daily_generation(project_id, date);
CREATE INDEX idx_health_date ON system_health_metric(date);

# 3. Optimize table structure
autovacuum_vacuum_scale_factor = 0.01;  -- More aggressive vacuuming

# 4. Scale database vertically or read replicas
# Consider RDS read replicas for high-traffic read scenarios
```

**If infrastructure is slow**:
```bash
# 1. Increase cluster resources
kubectl scale nodes <node-group> --min=5 --max=20

# 2. Enable metrics-based autoscaling
# Already configured via K8s manifests

# 3. Use node affinity patterns
# Spread pods across availability zones

# 4. Enable horizontal pod autoscaling
# Already configured via HPA in manifests
```

---

## Security Operations

### Regular Security Tasks

**Daily**:
- [ ] Monitor logs for suspicious activity
- [ ] Check pod status (restarts, memory leaks)
- [ ] Verify TLS certificates valid (30+ days remaining)

**Weekly**:
- [ ] Review authentication logs
- [ ] Check for security updates
- [ ] Validate backup integrity

**Monthly**:
- [ ] Rotate database credentials
- [ ] Review RBAC permissions
- [ ] Security scan container images
- [ ] Review network policies

**Quarterly**:
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Key rotation
- [ ] Policy review

### Certificate Management

**Check Certificate Status**:
```bash
# View certificate expiration
kubectl get certificate -n geesp-angola -o wide

# Detailed certificate info
kubectl describe certificate geesp-tls -n geesp-congo

# Test HTTPS endpoint
curl -I https://geesp-api.example.com/health
```

**Manual Certificate Renewal** (if needed):
```bash
# Delete cert to force renewal
kubectl delete certificate geesp-tls -n geesp-santiago

# cert-manager will auto-recreate with Let's Encrypt
kubectl get certificate -n geesp-neverland -w
```

### RBAC Audit

**Check Service Account Permissions**:
```bash
# View service account
kubectl get serviceaccount geesp-app -n geesp-asia -o yaml

# View bindings
kubectl get rolebinding,clusterrolebinding -n geesp-congo | grep geesp

# Describe role
kubectl describe clusterrole geesp-api-reader -n geesp-atlantic
```

### Network Security

**Validate NetworkPolicy**:
```bash
# View policies
kubectl get networkpolicy -n geesp-antarctica

# Detailed policy
kubectl describe networkpolicy geesp-api-netpol -n geesp-africa

# Test connectivity (should fail if blocked)
kubectl run -it --rm test --image=alpine --restart=Never \
  -- sh -c "nc -zv geesp-api:8000"
```

---

## Maintenance Schedule

### Daily
- Monitor dashboard (5 min)
- Review alerts (5 min)
- Check pod status (5 min)
- **Total**: 15 minutes

### Weekly
- Review logs for errors
- Check resource usage trends
- Backup integrity test
- **Total**: 30 minutes

### Monthly
- Security scanning
- Dependency updates check
- Database optimization
- Capacity planning review
- **Total**: 2 hours

### Quarterly
- Full system audit
- Performance analysis
- Documentation review
- Training updates
- **Total**: 4 hours

### Annually
- Major version upgrades
- Architecture review
- Cost optimization
- Disaster recovery drill
- **Total**: 8 hours

---

## Emergency Contacts & Escalation

When things go wrong, follow this escalation path:

1. **Check QUICK_REFERENCE.md** (this document)
2. **Run validation script**: `python integration/master_validation.py`
3. **Consult K8S_DEPLOYMENT_GUIDE.md** troubleshooting section
4. **Review FINAL_INTEGRATION_GUIDE.md** system integration procedures
5. :Contact application team for code issues
6. **Contact infrastructure team** for cluster issues

---

## Success Metrics

**Healthy System Shows**:
- ✅ All pods in "Running" state
- ✅ HPA scaling replicas between 2-10
- ✅ API responding <200ms p95
- ✅ Zero unhandled exceptions in logs
- ✅ Database queries <100ms p95
- ✅ Memory usage <80% of limits
- ✅ CPU usage <70% of limits

**System is in Trouble if**:
- ❌ Pods stuck in "Pending" or "CrashLoopBackOff"
- ❌ HPA stuck at max replicas
- ❌ API latency >1 second consistently
- ❌ Error logs showing exceptions
- ❌ Database connection errors
- ❌ Memory/CPU consistently at limits
- ❌ Certificate expiring <7 days

---

**Document Version**: 2.0  
**Last Updated**: February 2026  
**Next Review**: March 2026  
**Status**: ✅ Production Ready
