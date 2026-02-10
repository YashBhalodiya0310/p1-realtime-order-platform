# Day 04 — Docker Compose (Multi-Service Setup)

## Goal
Run multiple services together using Docker Compose.

## Services
- order-api (FastAPI service)
- inventory-worker (background worker placeholder)

## What I built
- docker-compose.yml
- Shared bridge network
- Multi-service startup with one command

## Commands used
```bash
docker compose up --build
curl http://127.0.0.1:8000/health
