"""
tests/test_auth.py
-------------------
Unit and integration tests for login and logout flows.
Uses Flask's test client with an in-memory SQLite database.
"""

import sys
import os
import pytest

# Add BACKEND to the import path so app, models, etc. can be found
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "BACKEND"))

from app import create_app
from models import database as db_module
from werkzeug.security import generate_password_hash


@pytest.fixture()
def app(tmp_path):
    """Create a test app using a temporary SQLite database."""
    test_db = str(tmp_path / "test_banking.db")
    db_module.DB_PATH = test_db

    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_valid_credentials_redirects_to_dashboard(client):
    response = client.post(
        "/login", data={"username": "demo", "password": "password123"}, follow_redirects=False
    )
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_login_wrong_password_shows_error(client):
    response = client.post(
        "/login", data={"username": "demo", "password": "wrongpassword"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_login_unknown_user_shows_error(client):
    response = client.post(
        "/login", data={"username": "nobody", "password": "password123"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_login_missing_username_shows_error(client):
    response = client.post(
        "/login", data={"username": "", "password": "password123"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Username is required" in response.data


def test_login_missing_password_shows_error(client):
    response = client.post(
        "/login", data={"username": "demo", "password": ""}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Password is required" in response.data


def test_dashboard_without_session_redirects_to_login(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout_clears_session(client):
    client.post("/login", data={"username": "demo", "password": "password123"})
    client.get("/logout")
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
