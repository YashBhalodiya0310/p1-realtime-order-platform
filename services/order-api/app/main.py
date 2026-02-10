from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from uuid import uuid4
from datetime import datetime, timezone

app = FastAPI(title="Order API", version="0.1.0")

# In-memory store (temporary)
ORDERS: Dict[str, dict] = {}


class CreateOrderRequest(BaseModel):
    item_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=100)


class OrderResponse(BaseModel):
    order_id: str
    status: str
    created_at: str
    item_id: str
    quantity: int


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
    return order


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order
