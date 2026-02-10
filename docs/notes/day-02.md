# Day 02 — Order API with FastAPI

## Goal
Build a basic Order API service and run it locally.

## What I built
- FastAPI application for order management
- Health check endpoint
- Create order endpoint
- Fetch order by ID endpoint
- In-memory order storage (temporary)

## Tech used
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic

## Project structure
- services/order-api/app/main.py
- services/order-api/requirements.txt

## How I ran it
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn app.main:app --reload
