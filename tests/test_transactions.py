"""
tests/test_transactions.py — unit + integration tests for deposit/withdraw.
"""
import sys, os, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "BACKEND"))
from app import create_app
from models import database as db_module
import services.account_service as svc

@pytest.fixture()
def app(tmp_path):
    db_module.DB_PATH = str(tmp_path / "test_banking.db")
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    yield flask_app

@pytest.fixture()
def client(app): return app.test_client()

@pytest.fixture()
def auth_client(client):
    client.post("/login", data={"username": "demo", "password": "password123"})
    return client

def test_deposit_increases_balance(app):
    with app.app_context():
        initial = svc.get_account(1)["balance"]
        assert svc.deposit(1, 200.0) == initial + 200.0

def test_deposit_zero_raises_error(app):
    with app.app_context():
        with pytest.raises(ValueError, match="greater than zero"): svc.deposit(1, 0)

def test_deposit_negative_raises_error(app):
    with app.app_context():
        with pytest.raises(ValueError, match="greater than zero"): svc.deposit(1, -50.0)

def test_withdraw_decreases_balance(app):
    with app.app_context():
        initial = svc.get_account(1)["balance"]
        assert svc.withdraw(1, 100.0) == initial - 100.0

def test_withdraw_full_balance_leaves_zero(app):
    with app.app_context():
        bal = svc.get_account(1)["balance"]
        assert svc.withdraw(1, bal) == 0.0

def test_withdraw_exceeds_balance_raises_error(app):
    with app.app_context():
        bal = svc.get_account(1)["balance"]
        with pytest.raises(ValueError, match="Insufficient funds"): svc.withdraw(1, bal + 1)

def test_withdraw_zero_raises_error(app):
    with app.app_context():
        with pytest.raises(ValueError, match="greater than zero"): svc.withdraw(1, 0)

def test_deposit_route_get(auth_client): assert auth_client.get("/deposit").status_code == 200
def test_deposit_route_valid_amount_redirects(auth_client):
    r = auth_client.post("/deposit", data={"amount": "100"}, follow_redirects=False)
    assert r.status_code == 302 and "/dashboard" in r.headers["Location"]
def test_deposit_route_invalid_amount_shows_error(auth_client):
    assert b"valid number" in auth_client.post("/deposit", data={"amount": "abc"}, follow_redirects=True).data
def test_deposit_route_zero_shows_error(auth_client):
    assert b"greater than zero" in auth_client.post("/deposit", data={"amount": "0"}, follow_redirects=True).data
def test_deposit_route_unauthenticated_redirects(client):
    r = client.post("/deposit", data={"amount": "100"}, follow_redirects=False)
    assert r.status_code == 302 and "/login" in r.headers["Location"]
def test_withdraw_route_get(auth_client): assert auth_client.get("/withdraw").status_code == 200
def test_withdraw_route_valid_amount_redirects(auth_client):
    r = auth_client.post("/withdraw", data={"amount": "100"}, follow_redirects=False)
    assert r.status_code == 302 and "/dashboard" in r.headers["Location"]
def test_withdraw_route_insufficient_funds_shows_error(auth_client):
    assert b"Insufficient funds" in auth_client.post("/withdraw", data={"amount": "999999"}, follow_redirects=True).data
def test_withdraw_route_negative_shows_error(auth_client):
    assert b"greater than zero" in auth_client.post("/withdraw", data={"amount": "-50"}, follow_redirects=True).data
def test_withdraw_route_unauthenticated_redirects(client):
    r = client.post("/withdraw", data={"amount": "100"}, follow_redirects=False)
    assert r.status_code == 302 and "/login" in r.headers["Location"]
