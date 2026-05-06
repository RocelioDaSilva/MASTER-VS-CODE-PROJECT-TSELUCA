#!/bin/bash
# Docker Test Suite for GEESP-Angola
# Tests that Docker image builds and runs correctly and performs a Streamlit smoke test

set -euo pipefail

echo "=== GEESP-Angola Docker Test Suite ==="

# Quick check: docker available?
if ! command -v docker >/dev/null 2>&1; then
	echo "Docker not found on PATH — skipping docker tests." >&2
	exit 0
fi

IMAGE=geesp-angola:latest
CONTAINER=test_geesp_streamlit
STREAMLIT_APP_PATH="Coding parts/geesp-angola/app.py"

echo "[TEST 1] Building Docker image..."
docker build -t "$IMAGE" -f Dockerfile .
echo "✓ Docker image built: $IMAGE"

echo "[TEST 2] Verify python runtime inside image..."
docker run --rm "$IMAGE" python --version
echo "✓ Python runtime verified"

echo "[TEST 3] Run unit tests inside container (fast subset)..."
docker run --rm "$IMAGE" python -m pytest "Coding parts/geesp-angola/tests" -q || {
	echo "✗ Unit tests failed inside container" >&2
	exit 1
}
echo "✓ Unit tests passed inside container"

echo "[TEST 4] Verify required packages import..."
docker run --rm "$IMAGE" python - <<'PY'
import sys
required = ["numpy","pandas","streamlit"]
missing = []
for r in required:
		try:
				__import__(r)
		except Exception as e:
				missing.append((r,str(e)))
if missing:
		print("Missing packages:", missing)
		sys.exit(2)
print("✓ Required packages import successfully")
PY

# Test 5: Streamlit smoke test — run container in background and poll HTTP
if [ -f "$STREAMLIT_APP_PATH" ]; then
	echo "[TEST 5] Streamlit smoke test using $STREAMLIT_APP_PATH"
	# Run detached container mapping 8501
	docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
	docker run -d --name "$CONTAINER" -e STREAMLIT_APP="$STREAMLIT_APP_PATH" -p 8501:8501 "$IMAGE" || {
		echo "✗ Failed to start container for Streamlit smoke test" >&2
		exit 1
	}

	# Wait up to 30s for service to respond
	echo "Waiting for Streamlit to become available on http://localhost:8501 ..."
	success=0
	for i in {1..30}; do
		if curl -sSf --max-time 2 http://localhost:8501/ >/dev/null 2>&1; then
			success=1
			break
		fi
		sleep 1
	done

	if [ "$success" -eq 1 ]; then
		echo "✓ Streamlit responded on http://localhost:8501"
	else
		echo "✗ Streamlit did not respond within timeout — fetching logs:" >&2
		docker logs "$CONTAINER" --tail 200 >&2 || true
		docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
		exit 1
	fi

	# Optional: check container health status if defined
	if docker inspect --format '{{json .State.Health}}' "$CONTAINER" 2>/dev/null | grep -q '"Status"'; then
		echo "Container exposes HEALTHCHECK — status: $(docker inspect --format '{{.State.Health.Status}}' $CONTAINER)"
	fi

	# Cleanup
	docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
else
	echo "[TEST 5] Streamlit app file not found at $STREAMLIT_APP_PATH — skipping smoke test"
fi

echo "[TEST 6] Volume mount test (writes)"
docker run --rm -v /tmp/geesp_test:/data "$IMAGE" python - <<'PY'
import os
os.makedirs('/data', exist_ok=True)
f='/data/docker_test.txt'
open(f,'w').write('ok')
print('✓ Volume write successful' if os.path.exists(f) else '✗ Volume write failed')
PY

if [ -f "docker-compose.yml" ]; then
	echo "[TEST 7] Docker Compose build check"
	docker-compose build --no-cache || { echo '✗ docker-compose build failed' >&2; exit 1; }
	echo "✓ docker-compose build succeeded"
else
	echo "[TEST 7] docker-compose.yml not found — skipping compose test"
fi

echo ""
echo "=== Docker tests completed successfully ==="
echo "Image ready: $IMAGE"

exit 0
