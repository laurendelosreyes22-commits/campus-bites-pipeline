# Campus Bites Database

Local Postgres database for analyzing campus food delivery order data.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running

## Quick Start

### Start the database

```bash
docker compose up -d
```

This will:
- Pull the Postgres 16 image (first time only)
- Create the `campus_bites` database
- Create the `orders` table and load data from the CSV

### Connect and run queries

```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

### Stop the database

```bash
docker compose down
```

### Reset the database (wipe all data)

```bash
docker compose down -v
docker compose up -d
```

## Connection Details

| Property | Value |
|----------|-------|
| Host | `localhost` |
| Port | `5432` |
| Database | `campus_bites` |
| User | `postgres` |
| Password | `postgres` |

### Connection String

```
postgresql://postgres:postgres@localhost:5432/campus_bites
```

Works with any Postgres client: pgAdmin, DBeaver, DataGrip, VS Code extensions, etc.

## Schema

### orders

| Column | Type | Description |
|--------|------|-------------|
| order_id | INTEGER | Primary key |
| order_date | DATE | Date of order |
| order_time | TIME | Time of order |
| customer_segment | VARCHAR(50) | Customer type (Dorm, Grad Student, Greek Life, Off-Campus) |
| order_value | DECIMAL(10,2) | Order total in dollars |
| cuisine_type | VARCHAR(50) | Type of food (Asian, Pizza, Mexican, etc.) |
| delivery_time_mins | INTEGER | Delivery time in minutes |
| promo_code_used | BOOLEAN | Whether a promo code was applied |
| is_reorder | BOOLEAN | Whether this is a repeat order |

## Sample Queries

```sql
-- Count total orders
SELECT COUNT(*) FROM orders;

-- Orders by cuisine type
SELECT cuisine_type, COUNT(*) as order_count
FROM orders
GROUP BY cuisine_type
ORDER BY order_count DESC;

-- Average order value by customer segment
SELECT customer_segment, ROUND(AVG(order_value), 2) as avg_order
FROM orders
GROUP BY customer_segment
ORDER BY avg_order DESC;

-- Promo code effectiveness
SELECT
    promo_code_used,
    COUNT(*) as orders,
    ROUND(AVG(order_value), 2) as avg_value
FROM orders
GROUP BY promo_code_used;

-- Busiest order hours
SELECT
    EXTRACT(HOUR FROM order_time) as hour,
    COUNT(*) as orders
FROM orders
GROUP BY hour
ORDER BY orders DESC;
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start the database |
| `docker compose down` | Stop the database |
| `docker compose down -v` | Stop and delete all data |
| `docker compose logs -f` | View database logs |
