# Docker & Local Development

This document describes how to build and run the project locally using Docker.

Build the image:

```bash
docker build -t geesp-app .
```

Run unit tests inside the container (default CMD runs pytest):

```bash
docker run --rm geesp-app
```

Run the Streamlit app (if `Coding parts/geesp-angola/app.py` exists):

```bash
docker run --rm -p 8501:8501 -e STREAMLIT_APP="Coding parts/geesp-angola/app.py" geesp-app
```

Use docker-compose for local PostGIS + app:

```bash
docker-compose up --build
```

Mount volumes for live development:

```bash
docker run --rm -p 8501:8501 -v "$(pwd)":/app -e STREAMLIT_APP="Coding parts/geesp-angola/app.py" geesp-app
```

CI notes:
- `.github/workflows/ci.yml` already runs `python -m pytest "Coding parts/geesp-angola/tests"`.
- The `scripts/test_docker.sh` performs additional validation — you can integrate it into CI if your runner supports Docker.
