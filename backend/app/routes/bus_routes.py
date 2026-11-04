from flask import Blueprint, jsonify

from app.services.bus_service import (
    get_all_buses,
    get_bus_by_id
)


bus_bp = Blueprint(
    "bus",
    __name__,
    url_prefix="/api/buses"
)


@bus_bp.route("/", methods=["GET"])
def get_buses():
    """
    GET /api/buses/

    Returns all active buses.
    """

    try:
        buses = get_all_buses()

        return jsonify({
            "success": True,
            "count": len(buses),
            "buses": buses
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Unable to retrieve buses.",
            "error": str(error)
        }), 500


@bus_bp.route("/<bus_id>", methods=["GET"])
def get_bus_details(bus_id):
    """
    GET /api/buses/<bus_id>

    Returns details of one bus.
    """

    try:
        bus = get_bus_by_id(bus_id)

        if bus is None:
            return jsonify({
                "success": False,
                "message": "Bus not found."
            }), 404

        return jsonify({
            "success": True,
            "bus": bus
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Unable to retrieve bus details.",
            "error": str(error)
        }), 500