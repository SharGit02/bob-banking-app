"""
services/account_service.py
----------------------------
Business logic for account lookup, deposit, and withdrawal.
All database reads and writes for account state live here so routes stay thin.
"""

from models.database import get_connection


def get_account(user_id: int) -> dict | None:
    """Return customer name and balance for the given user_id, or None if not found."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, name, balance FROM customers WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return None
        return {"id": row["id"], "name": row["name"], "balance": row["balance"]}
    finally:
        conn.close()


def deposit(user_id: int, amount: float) -> float:
    """Add *amount* to the customer's balance.

    Returns the new balance.
    Raises ValueError if amount is not positive.
    """
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")

    conn = get_connection()
    try:
        conn.execute(
            "UPDATE customers SET balance = balance + ? WHERE id = ?",
            (amount, user_id),
        )
        conn.execute(
            "INSERT INTO transactions (customer_id, type, amount) VALUES (?, 'deposit', ?)",
            (user_id, amount),
        )
        conn.commit()
        new_balance = conn.execute(
            "SELECT balance FROM customers WHERE id = ?", (user_id,)
        ).fetchone()["balance"]
        return new_balance
    finally:
        conn.close()


def withdraw(user_id: int, amount: float) -> float:
    """Subtract *amount* from the customer's balance.

    Returns the new balance.
    Raises ValueError for invalid amounts or insufficient funds.
    """
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")

    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT balance FROM customers WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            raise ValueError("Account not found.")

        current_balance = row["balance"]
        if amount > current_balance:
            raise ValueError(
                f"Insufficient funds. Your current balance is ${current_balance:,.2f}."
            )

        conn.execute(
            "UPDATE customers SET balance = balance - ? WHERE id = ?",
            (amount, user_id),
        )
        conn.execute(
            "INSERT INTO transactions (customer_id, type, amount) VALUES (?, 'withdrawal', ?)",
            (user_id, amount),
        )
        conn.commit()
        new_balance = conn.execute(
            "SELECT balance FROM customers WHERE id = ?", (user_id,)
        ).fetchone()["balance"]
        return new_balance
    finally:
        conn.close()
