from flask import Flask, jsonify
from flask_cors import CORS

from app.routes.bus_routes import bus_bp
from app.routes.search_routes import search_bp


def create_app():

    app = Flask(__name__)

    # Allow frontend requests during development
    CORS(app)

    # Register API routes
    app.register_blueprint(bus_bp)
    app.register_blueprint(search_bp)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "success": True,
            "message": "Welcome to TransitFlow Backend API",
            "status": "Running"
        }), 200

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "message": "TransitFlow backend is working."
        }), 200

    return app