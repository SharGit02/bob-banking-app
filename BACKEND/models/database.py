"""
models/database.py
------------------
Handles SQLite connection, schema initialisation, and demo data seeding.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

# Path to the SQLite database file, sitting next to this package inside BACKEND/
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "banking.db")


def get_connection():
    """Open and return a new SQLite connection.

    Rows are returned as sqlite3.Row objects so columns are accessible by name.
    Callers are responsible for closing the connection (or use a context manager).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist, then seed a demo customer."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # --- customers table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL,
                name     TEXT    NOT NULL,
                balance  REAL    NOT NULL DEFAULT 0.0
            )
        """)

        # --- transactions table (ledger) ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                type        TEXT    NOT NULL CHECK(type IN ('deposit', 'withdrawal')),
                amount      REAL    NOT NULL,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        conn.commit()

        # --- Seed demo account (only if table is empty) ---
        existing = cursor.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if existing == 0:
            cursor.execute(
                "INSERT INTO customers (username, password, name, balance) VALUES (?, ?, ?, ?)",
                (
                    "demo",
                    generate_password_hash("password123"),
                    "Alex Johnson",
                    1500.00,
                ),
            )
            conn.commit()
    finally:
        conn.close()
