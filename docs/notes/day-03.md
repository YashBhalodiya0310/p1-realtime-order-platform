# Day 03 — Dockerizing Order API

## Goal
Run the Order API inside a Docker container.

## What I did
- Created Dockerfile for FastAPI service
- Installed dependencies inside container
- Used python -m uvicorn to avoid PATH issues
- Exposed port 8000
- Ran container locally and verified health endpoint

## Commands used
```bash
docker build -t order-api:dev .
docker run -p 8000:8000 order-api:dev
curl http://127.0.0.1:8000/health
