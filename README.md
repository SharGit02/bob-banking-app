# bob-banking-app

Banking web application built with Flask, SQLite and Bootstrap.

## Tech Stack
- **Frontend:** HTML5 + Bootstrap 5 (FRONTEND folder)
- **Backend:** Python Flask (BACKEND folder)
- **Database:** SQLite (auto-created at startup)

## Features
- Customer Login with hashed password authentication
- Dashboard with live account balance
- Deposit Funds
- Withdraw Funds (with insufficient-funds guard)
- Logout with full session cleanup

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r BACKEND/requirements.txt

# 3. Run the app
cd BACKEND
python app.py
```

Open **http://localhost:5000** in your browser.

**Demo credentials:** `demo` / `password123`

## Running Tests

```bash
# From the project root (with venv active)
python -m pytest tests/ -v
```

## Project Structure

```
bob-banking-app/
├── FRONTEND/               # Static Bootstrap HTML wireframes
├── BACKEND/
│   ├── app.py              # Flask app factory + entry point
│   ├── requirements.txt
│   ├── models/             # SQLite schema & seed
│   ├── services/           # Business logic (deposit, withdraw)
│   ├── routes/             # Flask Blueprints
│   ├── utils/              # @login_required decorator
│   └── templates/          # Jinja2 HTML templates
└── tests/                  # Pytest suite (25 tests)
```

---
Built with [IBM Bob](https://ibm.com) during the Banking App Workshop.
