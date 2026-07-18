"""
routes/auth.py
--------------
Blueprint for /login and /logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.database import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Already logged in — go straight to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    # --- POST: validate and authenticate ---
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username:
        flash("Username is required.", "danger")
        return render_template("login.html")

    if not password:
        flash("Password is required.", "danger")
        return render_template("login.html")

    conn = get_connection()
    try:
        customer = conn.execute(
            "SELECT id, password FROM customers WHERE username = ?", (username,)
        ).fetchone()
    finally:
        conn.close()

    # Generic error — do not reveal whether the username exists
    if customer is None or not check_password_hash(customer["password"], password):
        flash("Invalid username or password.", "danger")
        return render_template("login.html")

    # Success — store only the customer ID in the session
    session.clear()
    session["user_id"] = customer["id"]
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
