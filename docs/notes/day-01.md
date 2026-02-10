# Day 01 — Repository Bootstrap

## Goal
Initialize the project repository with a clean structure and documentation baseline.

## What I did
- Created project directory
- Initialized Git repository
- Set default branch to main
- Created base folder structure
- Added .gitignore
- Created documentation files

## Commands I ran
```bash
mkdir -p p1-realtime-order-platform
cd p1-realtime-order-platform
git init
git branch -M main
mkdir -p docs/notes docs/adr services/order-api services/inventory-worker services/payment-worker deploy/local
touch README.md docs/architecture.md docs/notes/day-01.md .gitignore
