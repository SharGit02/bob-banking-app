"""
app.py
------
Flask application factory, configuration, Blueprint registration,
database initialisation, and development server entry point.
"""

import os
from flask import Flask, render_template

# Load .env file if present (python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # ── Security configuration ────────────────────────────────────────────────
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # ── Register Blueprints ───────────────────────────────────────────────────
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)

    # ── Root redirect ─────────────────────────────────────────────────────────
    from flask import redirect, url_for

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # ── Custom error handlers ─────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"Server error: {e}")
        return render_template("errors/500.html"), 500

    # ── Initialise database (creates tables + seeds demo account) ─────────────
    from models.database import init_db
    with app.app_context():
        init_db()

    return app


# ── Development entry point ───────────────────────────────────────────────────
if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True, port=5000)
