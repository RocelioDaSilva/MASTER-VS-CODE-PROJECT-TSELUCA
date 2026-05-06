Title: CI / Deployment readiness

Owner: DevOps

Description:
Finalize CI and deployment steps: ensure `requirements.txt`, `.github/workflows/ci.yml`, `scripts/test_docker.sh` and Dockerfile are production-ready.

Acceptance criteria:
- CI workflow passes on push/PR
- Docker image builds and `scripts/test_docker.sh` validates container
- Deployment runbook prepared

Labels: devops, high-priority
