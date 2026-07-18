"""
routes/transactions.py
-----------------------
Blueprint for /deposit and /withdraw.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import login_required
from services import account_service

transactions_bp = Blueprint("transactions", __name__)


# ── Deposit ──────────────────────────────────────────────────────────────────

@transactions_bp.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "GET":
        return render_template("deposit.html")

    raw_amount = request.form.get("amount", "").strip()

    # Validation
    if not raw_amount:
        flash("Please enter an amount.", "danger")
        return render_template("deposit.html")

    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Amount must be a valid number.", "danger")
        return render_template("deposit.html")

    if amount <= 0:
        flash("Amount must be greater than zero.", "danger")
        return render_template("deposit.html")

    try:
        new_balance = account_service.deposit(session["user_id"], amount)
        flash(f"Deposit of ${amount:,.2f} was successful. New balance: ${new_balance:,.2f}.", "success")
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("deposit.html")

    return redirect(url_for("dashboard.dashboard"))


# ── Withdraw ──────────────────────────────────────────────────────────────────

@transactions_bp.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "GET":
        return render_template("withdraw.html")

    raw_amount = request.form.get("amount", "").strip()

    # Validation
    if not raw_amount:
        flash("Please enter an amount.", "danger")
        return render_template("withdraw.html")

    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Amount must be a valid number.", "danger")
        return render_template("withdraw.html")

    if amount <= 0:
        flash("Amount must be greater than zero.", "danger")
        return render_template("withdraw.html")

    try:
        new_balance = account_service.withdraw(session["user_id"], amount)
        flash(f"Withdrawal of ${amount:,.2f} was successful. New balance: ${new_balance:,.2f}.", "success")
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("withdraw.html")

    return redirect(url_for("dashboard.dashboard"))
