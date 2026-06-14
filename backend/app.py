from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.db import init_indexes
from backend.utils.json import APIError, ok
from backend.routes.auth import auth_bp
from backend.routes.menu import menu_bp
from backend.routes.orders import orders_bp
from backend.routes.admin import admin_bp
from backend.routes.feedback import feedback_bp
import os

def create_app():
    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    CORS(app)
    init_indexes()

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(feedback_bp)

    @app.get("/api/health")
    def health():
        return ok({"service": "Canteen-Flow API", "database": "MongoDB only"})

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return {"success": False, "message": error.message}, error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        return {"success": False, "message": str(error)}, 500

    return app
