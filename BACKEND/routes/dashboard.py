"""
routes/dashboard.py
--------------------
Blueprint for /dashboard — the post-login landing page.
"""

from flask import Blueprint, render_template, session
from utils import login_required
from services.account_service import get_account

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    account = get_account(session["user_id"])
    return render_template("dashboard.html", account=account)
