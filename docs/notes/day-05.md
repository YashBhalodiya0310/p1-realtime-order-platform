# Day-05 — Redis queue (async processing)

## Goal
Move from synchronous “API does everything” to async processing:
- order-api creates an order
- order-api enqueues a job in Redis (list)
- inventory-worker consumes jobs from Redis

## What I implemented
- Added Redis config (REDIS_HOST, REDIS_PORT, QUEUE_NAME) in order-api
- order-api POST /orders now does:
  1) save order in in-memory ORDERS
  2) enqueue job: RPUSH orders {"order_id": "..."}
- Added PATCH /orders/{order_id}/status endpoint for status updates (used later by worker)
- Added Redis service + inventory-worker service into docker-compose
- Verified containers communicate on compose network (host=redis)

## How I verified it works
### Proof that enqueue works
1) Stop worker:
   docker compose stop inventory-worker
2) Create order:
   curl -s -X POST http://127.0.0.1:8000/orders \
     -H "Content-Type: application/json" \
     -d '{"item_id":"coffee","quantity":2}'
3) Check queue:
   docker compose exec redis redis-cli LLEN orders
   docker compose exec redis redis-cli LRANGE orders 0 5

Expected:
- LLEN becomes 1
- LRANGE shows one JSON payload

### Proof worker consumes
1) Start worker:
   docker compose start inventory-worker
2) Check queue again:
   docker compose exec redis redis-cli LLEN orders

Expected:
- LLEN returns to 0 (worker drained it)

## Key learning
If worker is running, the queue can look empty (LLEN=0) because jobs are consumed immediately.
To prove enqueue works, stop the worker first.
