# Monitoring Stack Setup and Usage Guide

## Overview

The GEESP-Angola monitoring stack provides:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **AlertManager**: Alert routing and notifications
- **Node Exporter**: Host system metrics
- **cAdvisor**: Docker container metrics
- **PostgreSQL Exporter**: Database metrics
- **Redis Exporter**: Cache metrics

## Quick Start

### 1. Start the Monitoring Stack

```bash
cd Full\ project

# Start with main app and monitoring
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Verify all services are running
docker-compose ps
```

### 2. Access the Monitoring Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin / admin (default) |
| **Prometheus** | http://localhost:9090 | — (no auth) |
| **AlertManager** | http://localhost:9093 | — |
| **Node Exporter** | http://localhost:9100/metrics | — |
| **cAdvisor** | http://localhost:8080 | — |
| **PostgreSQL Exporter** | http://localhost:9187/metrics | — |
| **Redis Exporter** | http://localhost:8001/metrics | — |

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=secure_grafana_password_here

# PostgreSQL (must match docker-compose.yml)
DB_USER=geesp_app
DB_PASSWORD=secure_db_password_here
DB_NAME=geesp_production
```

### Prometheus Configuration

Edit `monitoring/prometheus.yml` to:
- Add/remove scrape targets
- Adjust scrape intervals
- Configure external_labels
- Modify alerting rules

### AlertManager Configuration

Edit `monitoring/alertmanager.yml` to configure:
- Alert routing (which alerts go to which receivers)
- Notification channels (Slack, Email, PagerDuty)
- Inhibition rules (suppress less-important alerts when critical fires)

Example Slack notification setup:

```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

receivers:
  - name: 'critical-alerts'
    slack_configs:
      - channel: '#geesp-critical'
        title: 'CRITICAL - {{ .GroupLabels.alertname }}'
```

## Grafana Dashboards

### Import Pre-built Dashboards

In Grafana:
1. Go to **Dashboards** → **Import**
2. Enter dashboard ID or paste JSON
3. Select Prometheus data source
4. Click **Import**

**Recommended dashboard IDs:**
- `1860`: Node Exporter (system metrics)
- `3662`: Prometheus stats
- `9628`: PostgreSQL overview
- `12114`: Redis overview

### Create Custom Dashboards

1. Go to **Dashboards** → **New Dashboard**
2. Click **Add New Panel**
3. Write Prometheus query (examples below)
4. Customize visualization and save

**Example Prometheus Queries:**

```promql
# CPU usage over time
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Memory usage
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Disk usage
100 * (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes))

# HTTP request latency (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Database connections
pg_stat_activity_count

# Redis memory usage (MB)
redis_memory_used_bytes / (1024*1024)
```

## Alerting

### Setting Up Email Alerts

In `monitoring/alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'email-alerts'
  group_by: ['alertname']

receivers:
  - name: 'email-alerts'
    email_configs:
      - to: 'alerts@geesp-angola.org'
        from: 'alertmanager@geesp.internal'
        smarthost: 'mail.geesp.internal:587'
        auth_username: 'alertmanager'
        auth_password: 'secure_password'
        headers:
          Subject: '{{ .GroupLabels.alertname }}'
```

### Testing Alerts

```bash
# Send test alert to AlertManager
curl -X POST http://localhost:9093/api/v1/alerts \
  -H 'Content-Type: application/json' \
  -d '[{
    "labels": {
      "alertname": "TestAlert",
      "severity": "critical"
    },
    "annotations": {
      "summary": "This is a test alert"
    }
  }]'
```

### Checking Alert Status

In Prometheus UI (http://localhost:9090):
1. Go to **Alerts** tab
2. View active and inactive alerts
3. See alert rules and their status

## Data Retention and Cleanup

### Prometheus Retention

Modify `docker-compose.monitoring.yml` to change retention:

```yaml
prometheus:
  command:
    - '--storage.tsdb.retention.time=30d'  # Change this
    - '--storage.tsdb.retention.size=10GB'  # Or size limit
```

### Persistent Volume Management

```bash
# Check volume usage
docker volume ls
docker volume inspect geesp-prometheus_data

# Backup Prometheus data
docker run --rm -v geesp-prometheus_data:/data \
  -v $(pwd)/backups:/backup \
  busybox tar czf /backup/prometheus_backup.tar.gz -C /data .

# Restore from backup
docker run --rm -v geesp-prometheus_data:/data \
  -v $(pwd)/backups:/backup \
  busybox tar xzf /backup/prometheus_backup.tar.gz -C /data
```

## Troubleshooting

### Prometheus cannot scrape target

```bash
# Check target status in Prometheus UI
# URL: http://localhost:9090/targets

# Test manual scrape
curl -s http://localhost:9100/metrics | head -20

# Check Docker network connectivity
docker-compose exec prometheus curl http://node-exporter:9100/metrics
```

### Grafana not showing data

1. Verify Prometheus is running: `docker-compose ps prometheus`
2. Check Prometheus data source in Grafana:
   - **Configuration** → **Data Sources** → **Prometheus**
   - Verify URL: `http://prometheus:9090`
3. Test with simple query in Grafana explorer

### AlertManager not sending notifications

1. Check AlertManager logs: `docker-compose logs alertmanager`
2. Verify webhook URL is correct in `alertmanager.yml`
3. Test webhook manually:
   ```bash
   curl -X POST your_slack_webhook_url \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test message"}'
   ```

### High memory usage in Prometheus

- Reduce `scrape_interval` and `evaluation_interval` in `prometheus.yml`
- Lower `--storage.tsdb.retention.time` flag
- Remove unnecessary scrape configs
- Increase container memory limit in `docker-compose.monitoring.yml`

## Integration with Main Application

### Add Custom Metrics to Streamlit App

```python
# In your Streamlit app (app.py)
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
prediction_counter = Counter(
    'geesp_predictions_total',
    'Total number of predictions made',
    ['location', 'technology']
)

analysis_latency = Histogram(
    'geesp_analysis_duration_seconds',
    'Time to complete analysis'
)

# Use in code
with analysis_latency.time():
    result = run_analysis()

prediction_counter.labels(location='Luanda', technology='solar').inc()

# Expose metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
```

### Configure Prometheus to Scrape App

In `monitoring/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'geesp-app'
    static_configs:
      - targets: ['geesp-app:8501']  # or 5000 if using Flask
    metrics_path: '/metrics'
    scrape_interval: 10s
```

## Maintenance

### Regular Tasks

**Weekly:**
- Review Grafana dashboards for trends
- Check AlertManager for unhandled alerts

**Monthly:**
- Rotate Grafana admin password
- Archive and backup Prometheus data
- Review and optimize alert thresholds

**Quarterly:**
- Update Prometheus and Grafana images
- Review and refine alert rules
- Capacity planning (disk, memory)

### Stopping the Stack

```bash
# Stop monitoring services
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml down

# Stop and remove volumes (careful!)
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml down -v
```

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AlertManager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- [Exporters and Integrations](https://prometheus.io/docs/instrumenting/exporters/)
