from flask import Blueprint, jsonify, request

from app.services.search_service import search_buses


search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/api/search"
)


@search_bp.route("/", methods=["GET"])
def search_bus_routes():
    """
    GET /api/search/?source=...&destination=...
    """

    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()

    if not source or not destination:
        return jsonify({
            "success": False,
            "message": "Please provide both source and destination."
        }), 400

    try:
        results = search_buses(
            source,
            destination
        )

        return jsonify({
            "success": True,
            "results": results
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Bus search failed.",
            "error": str(error)
        }), 500