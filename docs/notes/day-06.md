# Day 06 — Worker-driven order status lifecycle

## Goal
Make order status change based on inventory-worker processing, not manual PATCH.

## Plan
- Define status states: CREATED -> QUEUED -> PROCESSING -> COMPLETED/FAILED
- When POST /orders happens:
  - Save order
  - Push job to Redis queue
  - Set status to QUEUED
- inventory-worker:
  - BRPOP queue
  - Set status PROCESSING
  - Simulate work
  - Set status COMPLETED (or FAILED)

## Notes / Decisions
- (fill: how worker updates order-api: API call or Redis pubsub)
