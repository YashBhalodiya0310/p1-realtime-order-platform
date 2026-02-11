import os
import json
from typing import Dict
from uuid import uuid4
from datetime import datetime, timezone

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Order API", version="0.2.0")

# In-memory store (temporary for now)
ORDERS: Dict[str, dict] = {}

# Redis config (global)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


class CreateOrderRequest(BaseModel):
    item_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=100)


class OrderResponse(BaseModel):
    order_id: str
    status: str
    created_at: str
    item_id: str
    quantity: int


class UpdateStatusRequest(BaseModel):
    status: str = Field(..., min_length=1)


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-api"}


@app.post("/orders", response_model=OrderResponse)
def create_order(req: CreateOrderRequest):
    order_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    order = {
        "order_id": order_id,
        "status": "CREATED",
        "created_at": created_at,
        "item_id": req.item_id,
        "quantity": req.quantity,
    }

    ORDERS[order_id] = order

    # enqueue job for worker
    redis_client.rpush(QUEUE_NAME, json.dumps({"order_id": order_id}))

    return order


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order


@app.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, req: UpdateStatusRequest):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    order["status"] = req.status
    ORDERS[order_id] = order
    return order
