"""
Load CSV data into the Postgres orders table.

Usage:
    python load_data.py
"""

import csv
from pathlib import Path

import psycopg


# Database connection string (user:password@host:port/database)
DB_URL = "postgresql://postgres:postgres@localhost:5432/campus_bites"

# Path to CSV file (relative to this script's location)
CSV_PATH = Path(__file__).parent / "data" / "campus_bites_orders.csv"


def create_table(cursor):
    """Create the orders table if it doesn't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            order_date DATE NOT NULL,
            order_time TIME NOT NULL,
            customer_segment VARCHAR(50) NOT NULL,
            order_value DECIMAL(10,2) NOT NULL,
            cuisine_type VARCHAR(50) NOT NULL,
            delivery_time_mins INTEGER NOT NULL,
            promo_code_used BOOLEAN NOT NULL,
            is_reorder BOOLEAN NOT NULL
        )
    """)


def load_csv(cursor, csv_path):
    """Load CSV data into the orders table, replacing any existing data."""
    # Clear existing data (faster than DELETE, resets table instantly)
    cursor.execute("TRUNCATE TABLE orders")

    # Read CSV and insert each row
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO orders (
                    order_id, order_date, order_time, customer_segment,
                    order_value, cuisine_type, delivery_time_mins,
                    promo_code_used, is_reorder
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(row["order_id"]),
                    row["order_date"],
                    row["order_time"],
                    row["customer_segment"],
                    float(row["order_value"]),
                    row["cuisine_type"],
                    int(row["delivery_time_mins"]),
                    # Convert "Yes"/"No" strings to boolean
                    row["promo_code_used"] == "Yes",
                    # Handle empty values as False
                    row["is_reorder"] == "Yes" if row["is_reorder"] else False,
                ),
            )


def main():
    """Connect to database, create table, and load data."""
    # Context manager auto-closes connection when done
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            create_table(cursor)
            load_csv(cursor, CSV_PATH)

            # Verify the load
            cursor.execute("SELECT COUNT(*) FROM orders")
            count = cursor.fetchone()[0]

        # Commit transaction (saves all changes to database)
        conn.commit()

    print(f"Loaded {count} orders into the database.")


if __name__ == "__main__":
    main()
