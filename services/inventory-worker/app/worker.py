import os
import json
import time
import requests
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")
ORDER_API_URL = os.getenv("ORDER_API_URL", "http://localhost:8000")

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    # Wait until redis is ready (extra safety)
    for _ in range(30):
        try:
            r.ping()
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError("Redis not reachable")

    print(f"[worker] Connected to Redis at {REDIS_HOST}:{REDIS_PORT}, queue={QUEUE_NAME}")

    while True:
        # BLPOP blocks until an item exists
        item = r.blpop(QUEUE_NAME, timeout=10)
        if not item:
            continue

        _, payload = item
        try:
            job = json.loads(payload)
            order_id = job["order_id"]
            print(f"[worker] Processing order_id={order_id}")

            # simulate inventory reservation
            time.sleep(1)

            # call order-api to update status
            resp = requests.patch(
                f"{ORDER_API_URL}/orders/{order_id}/status",
                json={"status": "INVENTORY_RESERVED"},
                timeout=5,
            )
            print(f"[worker] Updated order {order_id}: {resp.status_code} {resp.text}")

        except Exception as e:
            print(f"[worker] ERROR processing payload={payload}: {e}")

if __name__ == "__main__":
    main()
