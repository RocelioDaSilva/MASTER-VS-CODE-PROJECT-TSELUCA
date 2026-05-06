# Deployment Guide

Complete step-by-step instructions for deploying GEESP-Angola to development, staging, and production environments.

---

## Prerequisites

- Node.js 18+ (for Express + React)
- Python 3.11+ (for MCDA engine)
- npm or yarn
- Git
- SQLite3 (included in better-sqlite3)
- Gemini API key (from Google AI Studio)

---

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/GEESP-Angola.git
cd GEESP-Angola/Full\ project/02_Code
```

### 2. Python Backend Setup (geesp-angola/)
```bash
cd geesp-angola
python -m venv venv
source venv/Scripts/activate    # Windows
./venv/Scripts/Activate.ps1     # PowerShell
pip install -r requirements.txt
pytest tests/                   # Verify tests pass
```

### 3. Node.js Backend Setup (nevermindu/)
```bash
cd nevermindu
npm install
cp .env.example .env
# Edit .env with your Gemini API key
export GEMINI_API_KEY=your_key_here
npm run lint  # Check TypeScript
```

---

## Development Deployment

### Quick Start (All Services)
```bash
# Terminal 1: nevermindu (runs both server + client)
cd nevermindu
npm run dev

# Terminal 2: Python dashboard (optional)
cd geesp-angola
./venv/Scripts/Activate.ps1
streamlit run dashboard/app.py

# Terminal 3: Run tests (optional)
cd geesp-angola
pytest tests/ -v
```

### Access Points
```
http://localhost:5173    ← React dashboard (Vite dev server)
http://localhost:3000    ← Express API
http://localhost:8501    ← Streamlit dashboard
```

### Verify Setup
```bash
# Check API health
curl http://localhost:3000/api/health
# Expected: {"status":"ok","timestamp":"2026-03-05T..."}

# Check React loads
curl http://localhost:5173
# Expected: HTML index page
```

---

## Staging Deployment

### Build Frontend
```bash
cd nevermindu
npm run build
# Output: dist/ folder (optimized, minified)
```

### Prepare Backend
```bash
cd nevermindu
# Install production dependencies only
npm install --production

# Create environment file
cat > .env << EOF
PORT=3000
NODE_ENV=production
GEMINI_API_KEY=your_staging_key_here
DATABASE_URL=/var/staging/geesp_scenarios.db
EOF

# Test build
npm start
# Should start on http://localhost:3000
```

### Using Docker Compose (Optional)
```bash
docker-compose -f docker-compose.yml up -d

# Logs
docker-compose logs -f app

# Stop
docker-compose down
```

---

## Production Deployment

### 1. Server Preparation
```bash
# On your production server
sudo mkdir -p /opt/geesp-angola
sudo chown $USER:$USER /opt/geesp-angola
cd /opt/geesp-angola

# Clone repo
git clone https://github.com/your-org/GEESP-Angola.git .

# Create data directory
mkdir -p /var/lib/geesp
chmod 755 /var/lib/geesp
```

### 2. Environment Configuration
```bash
# Create production .env
cat > nevermindu/.env.production << EOF
PORT=3000
NODE_ENV=production
GEMINI_API_KEY=${GEMINI_API_KEY}
DATABASE_URL=/var/lib/geesp/geesp_scenarios.db
EOF

# Secure permissions
chmod 600 nevermindu/.env.production
```

### 3. Backend Deployment
```bash
cd /opt/geesp-angola/nevermindu

# Install dependencies
npm install --production

# Build (if using TypeScript)
npm run build

# Start with PM2 (recommended)
npm install -g pm2
pm2 start server.ts --name "geesp-api"
pm2 save

# Or use systemd service
sudo tee /etc/systemd/system/geesp-api.service << EOF
[Unit]
Description=GEESP-Angola API Server
After=network.target

[Service]
Type=simple
User=geesp
WorkingDirectory=/opt/geesp-angola/nevermindu
Environment="NODE_ENV=production"
Environment="PORT=3000"
Environment="GEMINI_API_KEY=${GEMINI_API_KEY}"
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable geesp-api
sudo systemctl start geesp-api
```

### 4. Frontend Deployment (Nginx)
```bash
# Build optimized frontend
cd /opt/geesp-angola/nevermindu
npm run build

# Create Nginx config
sudo tee /etc/nginx/sites-available/geesp-angola << 'EOF'
server {
    listen 80;
    server_name geesp-angola.example.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name geesp-angola.example.com;
    
    ssl_certificate /etc/letsencrypt/live/geesp-angola.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/geesp-angola.example.com/privkey.pem;
    
    # React app
    location / {
        root /opt/geesp-angola/nevermindu/dist;
        try_files $uri /index.html;
    }
    
    # API proxy
    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_pragma $http_authorization;
    }
    
    # Caching
    location ~* \.(js|css|png|jpg|svg)$ {
        expires 30d;
        add_header Cache-Control "immutable";
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/geesp-angola /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d geesp-angola.example.com
# Follow prompts, then systemd auto-renews
```

### 6. Database Backup
```bash
# Daily backup script
cat > /opt/geesp-angola/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/lib/geesp/backups"
mkdir -p $BACKUP_DIR
cp /var/lib/geesp/geesp_scenarios.db $BACKUP_DIR/geesp_$(date +%Y%m%d_%H%M%S).db
find $BACKUP_DIR -mtime +7 -delete  # Keep 7 days
EOF

chmod +x /opt/geesp-angola/backup.sh
crontab -e
# Add: 0 2 * * * /opt/geesp-angola/backup.sh
```

### 7. Monitoring Setup
```bash
# Install Prometheus node exporter (optional)
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xzf node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/

# Create service
sudo tee /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

### 8. Health Checks & Alerts
```bash
# Monitor API health
curl -s http://localhost:3000/api/health | jq .
# Set up Uptime Robot or similar service
```

---

## Verification Checklist

### Post-Deployment
- [ ] Frontend loads at https://geesp-angola.example.com
- [ ] API responds at /api/health
- [ ] Database exists at /var/lib/geesp/geesp_scenarios.db
- [ ] Scenarios can be saved & retrieved
- [ ] Financial calculations work
- [ ] Exports (PDF/Excel/JSON) function
- [ ] Gemini chat responds
- [ ] SSL certificate valid
- [ ] Nginx caching working
- [ ] Backups created automatically

### Performance Baseline
```bash
# Load test (using Apache Bench)
ab -n 1000 -c 10 http://localhost:3000/api/health
# Should handle >100 req/sec

# Database size check
du -sh /var/lib/geesp/geesp_scenarios.db
# Should be <100MB for 10k scenarios
```

---

## Troubleshooting

### API not starting
```bash
# Check Node version
node --version  # Should be 18+

# Check port in use
lsof -i :3000

# Check error logs
tail -50 /var/log/geesp-api.log
```

### Frontend blank page
```bash
# Check browser console for errors
# Verify API endpoint in .env
# Check CORS headers
curl -i http://localhost:3000/api/health
```

### Database locked
```bash
# SQLite can lock under concurrent access
# Solution: Enable WAL mode
sqlite3 /var/lib/geesp/geesp_scenarios.db "PRAGMA journal_mode=WAL;"
```

### Gemini API errors
```bash
# Verify API key
echo $GEMINI_API_KEY

# Test with curl
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$GEMINI_API_KEY
```

---

## Rollback Procedure

```bash
# Stop current deployment
systemctl stop geesp-api

# Restore previous version
git checkout previous-tag
npm install --production
npm run build

# Restore database backup
cp /var/lib/geesp/backups/geesp_20260304_000000.db /var/lib/geesp/geesp_scenarios.db

# Start
systemctl start geesp-api
```

---

## Upgrade Procedure

```bash
# Pull latest code
git pull origin main

# Install new dependencies
npm install

# Run migrations (if applicable)
npm run migrate

# Build
npm run build

# Test before switching
npm run test

# Switch over (zero-downtime with PM2)
pm2 reload geesp-api

# Verify health
curl http://localhost:3000/api/health
```

---

## Performance Optimization

### Frontend
- Enable Gzip compression in Nginx: `gzip on;`
- Cache assets for 30 days
- Use CDN for static files (optional)

### Backend
- SQLite: Enable WAL mode for concurrent writes
- Add API rate limiting (express-rate-limit)
- Implement request caching (Redis, optional)

### Database
- Index on `scenario_id` and `community_id` (already done)
- Vacuum periodically: `sqlite3 ... VACUUM;`
- Monitor size: Should stay <100MB for 10k scenarios

---

## Security Hardening

```bash
# Fail2ban for brute force protection
sudo apt install fail2ban

# Create config
sudo tee /etc/fail2ban/jail.local << EOF
[sshd]
enabled = true

[geesp-api]
enabled = true
port = http,https
filter = geesp-api
logpath = /var/log/geesp-api.log
maxretry = 5
EOF

# Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## Support

- **Issues**: GitHub issues
- **Documentation**: `/02_Code/PRODUCTION_ARCHITECTURE.md`
- **Questions**: Email: support@example.com

---

**Last Updated**: 2026-03-05
**Recommended Hosting**: AWS/Azure/DigitalOcean
**Estimated Cost (AWS)**: ~$20-50/month (t3.micro to t3.small)
