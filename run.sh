#!/bin/bash
set -e
cd /root/task
echo "[INFO] Starting containerized PostgreSQL and FastAPI environment..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "[INFO] Waiting for PostgreSQL service to become available..."
MAX_RETRIES=30
RETRY=0
until docker exec pg_recipes pg_isready -U utkrusht ; do
  sleep 2
  RETRY=$((RETRY+1))
  if [ $RETRY -ge $MAX_RETRIES ]; then
    echo "[ERROR] PostgreSQL did not become ready in time."
    docker-compose logs postgres
    exit 1
  fi
done
echo "[INFO] PostgreSQL is ready."

# FastAPI health check
echo "[INFO] Verifying FastAPI application startup..."
MAX_RETRIES=20
RETRY=0
until curl -s http://localhost:8000/docs > /dev/null ; do
  sleep 2
  RETRY=$((RETRY+1))
  if [ $RETRY -ge $MAX_RETRIES ]; then
    echo "[ERROR] FastAPI app did not respond in time."
    docker-compose logs fastapi
    exit 2
  fi
done
echo "[SUCCESS] FastAPI app is running and responding."
