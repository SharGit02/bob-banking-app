"""
utils/__init__.py
-----------------
Shared decorators used across route Blueprints.
"""

from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """Redirect to /login if no valid session exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
