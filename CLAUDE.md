# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Bites Pipeline is a data pipeline for campus food delivery order analytics. It uses Docker-containerized PostgreSQL with a Python ETL script to load CSV data.

## Commands

```bash
# Start PostgreSQL database
docker compose up -d

# Stop database
docker compose down

# Reset all data (destroy volume and recreate)
docker compose down -v && docker compose up -d

# Load CSV data into database
python load_data.py

# Connect to database via psql
docker exec -it campus_bites_db psql -U postgres -d campus_bites

# View container logs
docker compose logs -f
```

## Architecture

**Data Flow**: CSV file → `load_data.py` → PostgreSQL

- **docker-compose.yml**: PostgreSQL 16 service on port 5432
- **load_data.py**: ETL script with `create_table()` and `load_csv()` functions that handle type conversion (booleans from "Yes"/"No", numeric parsing, null handling)
- **data/campus_bites_orders.csv**: Source data (~1,132 orders)

**Database Connection**: `postgresql://postgres:postgres@localhost:5432/campus_bites`

**Schema**: Single `orders` table with columns: order_id (PK), order_date, order_time, customer_segment, order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder

## Dependencies

- Docker
- Python 3.x with psycopg (see requirements.txt)
