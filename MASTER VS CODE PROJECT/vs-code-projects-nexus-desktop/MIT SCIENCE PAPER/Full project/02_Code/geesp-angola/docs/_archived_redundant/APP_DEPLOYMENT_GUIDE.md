# GEESP-Angola Unified App: Deployment Guide
**Version**: 1.0 | **Date**: 2026-02-09 | **Platform**: Streamlit

---

## 🚀 QUICK START (2 minutes)

### Option A: Run Locally (Easiest)

```bash
# 1. Install dependencies
pip install -r requirements-unified.txt

# 2. Run the app
streamlit run geesp-unified-app.py

# 3. Open browser → http://localhost:8501
```

**That's it!** The app will open in your default browser.

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Build image
docker build -t geesp-angola:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  geesp-angola:latest

# Access at http://localhost:8501
```

### Docker Compose (Recommended)

```bash
# Start the app service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```


---

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (FREE & EASIEST)

1. **Push code to GitHub**
   ```bash
   git add geesp_unified_app.py requirements-app.txt
   git commit -m "feat: unified app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repo + branch
   - Point to `geesp_unified_app.py`
   - Click "Deploy"

3. **Your app is live at**: `https://<username>-geesp-angola.streamlit.app`

**Pros**: ✅ Free, ✅ Auto-updates on git push, ✅ Easy sharing  
**Cons**: ⚠️ Limited resources, ⚠️ Cold starts

---

### Option 2: AWS/Heroku/GCP

#### AWS EC2 + Systemd

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-instance.compute.amazonaws.com

# Clone repo
git clone https://github.com/geesp-angola/geesp-angola.git
cd geesp-angola

# Install dependencies
pip install -r requirements-app.txt

# Create systemd service (as root)
sudo tee /etc/systemd/system/geesp.service > /dev/null <<EOF
[Unit]
Description=GEESP-Angola Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/geesp-angola
ExecStart=/usr/local/bin/streamlit run geesp_unified_app.py --server.port=80
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl enable geesp
sudo systemctl start geesp

# View logs
sudo systemctl status geesp
sudo journalctl -u geesp -f
```

#### Heroku

```bash
# Create Heroku app
heroku create geesp-angola

# Add Buildpack for Python + System Dependencies
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/sharkby7e/gdal-buildpack.git

# Create Procfile
echo "web: streamlit run geesp_unified_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 📦 Standalone Desktop App (PyInstaller)

### Build Windows Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create spec file
pyinstaller --onefile \
  --windowed \
  --name "GEESP-Angola" \
  --icon "logo.ico" \
  geesp_unified_app.py

# Executable created at: dist/GEESP-Angola.exe
# Share this file with end-users
```

### Build for macOS

```bash
pyinstaller --onefile \
  --windowed \
  --name "GEESP-Angola" \
  --icon "logo.icns" \
  geesp_unified_app.py

# Executable: dist/GEESP-Angola.app
  codesign -s - dist/GEESP-Angola.app  # Sign if needed
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Set Streamlit config
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_LOGGER_LEVEL=info

# Or create .streamlit/config.toml
streamlit config show > ~/.streamlit/config.toml
```

### Custom config.json

Create `config.json` in project root:

```json
{
  "map_generation": {
    "output_shape": [280, 300],
    "output_dir": "data/processed"
  },
  "mcda": {
    "weights": {
      "irradiacao": 0.25,
      "populacao": 0.25,
      "distancia_rede": 0.20,
      "declividade": 0.15,
      "ndvi": 0.15
    }
  },
  "lcoe": {
    "wacc": 0.08,
    "project_lifetime_years": 20
  }
}
```

---

## 📊 Performance Optimization

### For Local Development

```bash
# Run with caching enabled
streamlit run geesp_unified_app.py \
  --logger.level=info \
  --client.showErrorDetails=true \
  --cache_expiration_seconds=3600
```

### For Production

```bash
# Run with optimizations
streamlit run geesp_unified_app.py \
  --logger.level=warning \
  --client.showErrorDetails=false \
  --server.maxUploadSize=200 \
  --server.enableXsrfProtection=true
```

---

## 🔐 Security

### Basic Authentication

Add to `geesp_unified_app.py`:

```python
import streamlit as st

# Simple password protection
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    with st.form("password_form"):
        password = st.text_input("Password:", type="password")
        if st.form_submit_button("Login"):
            if password == st.secrets["app_password"]:
                st.session_state.password_correct = True
                return True
            else:
                st.error("❌ Invalid password")
                return False

    return False

# Add at top of main app
if not check_password():
    st.stop()
```

### Environment Secrets

Create `.streamlit/secrets.toml`:

```toml
app_password = "your-secure-password-here"
database_url = "postgresql://user:pass@localhost/db"
```

---

## 📈 Monitoring & Logging

### Streamlit Logs

```bash
# View Streamlit logs
tail -f ~/.streamlit/logs/app

# Or from Heroku
heroku logs --tail

# Or from Docker
docker logs -f container_id
```

### Application Logs

Add to `geesp_unified_app.py`:

```python
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("App started")
```

---

## 🐛 Troubleshooting

### "Module not found" Error

```bash
# Ensure all dependencies installed
pip install -r requirements-app.txt --upgrade

# Check Streamlit is working
streamlit --version
```

### Port Already in Use

```bash
# Use different port
streamlit run geesp_unified_app.py --server.port=8502

# Or kill process on port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows
```

### Maps Not Loading

```bash
# Ensure data directory exists
mkdir -p data/processed

# Generate maps first
python scripts/generate_maps_simple.py
```

### MCDA Module Errors

```python
# Check imports
python -c "from scripts.mcda_analysis import MCDAnalyzer; print('✓ OK')"

# If error, regenerate synthetic data
python scripts/generate_maps_simple.py
```

---

## 📱 Mobile Access

### Run on Network

```bash
# Get your IP
ipconfig getifaddr en0  # macOS
hostname -I            # Linux
ipconfig               # Windows

# Run Streamlit
streamlit run geesp_unified_app.py --server.address=0.0.0.0

# Access from another device
# http://YOUR_IP:8501
```

### Ngrok (Public Tunnel)

```bash
# Install ngrok
brew install ngrok  # macOS

# Create tunnel
ngrok http 8501

# Share public URL
# https://xxx-xxx-xxx.ngrok.io
```

---

## 🚀 GitHub Actions CI/CD

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements-app.txt
      - run: pytest tests/
      - name: Deploy to Streamlit Cloud
        env:
          STREAMLIT_CLOUD_TOKEN: ${{ secrets.STREAMLIT_CLOUD_TOKEN }}
        run: |
          streamlit run geesp_unified_app.py
```

---

## 📚 Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/deploy/streamlit-cloud
- **Docker Docs**: https://docs.docker.com
- **GitHub Actions**: https://docs.github.com/en/actions

---

## ❓ Support

For issues or questions:
1. Check the [GEESP GitHub Issues](https://github.com/geesp-angola/geesp-angola/issues)
2. Email: geesp@email.com
3. Submit a bug report with logs

---

**Happy deploying! 🚀**
