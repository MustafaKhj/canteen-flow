from flask import Blueprint, request
from bson import ObjectId
from backend.db import db
from backend.utils.auth import require_auth
from backend.utils.json import ok, APIError
from backend.services.order_service import place_order, get_order, update_order_status

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_bp.post("")
@require_auth("student")
def create_order():
    user = request.current_user
    data = request.get_json(force=True)
    order = place_order(user["_id"], data.get("items", []), data.get("payment_method", "campus_wallet"))
    return ok(order, "order placed")

@orders_bp.get("")
@require_auth("student", "staff", "admin")
def list_orders():
    user = request.current_user
    query = {}
    if user["role"] == "student":
        query["user_id"] = user["_id"]
    status = request.args.get("status")
    if status:
        query["status"] = status
    orders = list(db.orders.find(query).sort("created_at", -1).limit(100))
    for order in orders:
        order["items"] = list(db.order_items.find({"order_id": order["_id"]}))
    return ok(orders)

@orders_bp.get("/<order_id>")
@require_auth("student", "staff", "admin")
def read_order(order_id):
    order = get_order(order_id)
    user = request.current_user
    if user["role"] == "student" and order["user_id"] != user["_id"]:
        raise APIError("You can view only your own orders", 403)
    return ok(order)

@orders_bp.patch("/<order_id>/status")
@require_auth("staff", "admin")
def patch_status(order_id):
    data = request.get_json(force=True)
    return ok(update_order_status(order_id, data.get("status")), "order status updated")
