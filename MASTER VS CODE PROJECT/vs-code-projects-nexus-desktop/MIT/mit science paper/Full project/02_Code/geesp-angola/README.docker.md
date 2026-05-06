Docker usage (build & run) for GEESP-Angola

Build the image from `Coding parts/geesp-angola`:

```bash
cd "Coding parts/geesp-angola"
docker build -t geesp-angola:latest .
```

Run tests inside the container (image runs pytest by default):

```bash
docker run --rm geesp-angola:latest
```

To start a shell in the container for interactive debugging:

```bash
docker run --rm -it geesp-angola:latest bash
```

Notes:
- This Dockerfile uses `python:3.11-slim` and installs system dependencies required by common geospatial Python packages. If you will build large packages (e.g., GDAL/PyProj) on Windows host, consider using WSL or a Linux CI environment.
- The `requirements.txt` in the folder is used to install Python dependencies. Adjust versions as needed.
