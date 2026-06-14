from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime, timezone
from backend.db import db
from backend.utils.auth import require_auth
from backend.utils.json import ok, APIError

feedback_bp = Blueprint("feedback", __name__, url_prefix="/api/feedback")

@feedback_bp.post("")
@require_auth("student")
def create_feedback():
    user = request.current_user
    data = request.get_json(force=True)
    order = db.orders.find_one({"_id": ObjectId(data.get("order_id")), "user_id": user["_id"]})
    if not order:
        raise APIError("Order not found for this student", 404)
    menu = db.menu_items.find_one({"_id": ObjectId(data.get("menu_item_id"))})
    if not menu:
        raise APIError("Menu item not found", 404)
    rating = int(data.get("rating", 5))
    if rating < 1 or rating > 5:
        raise APIError("Rating must be between 1 and 5")
    doc = {
        "order_id": order["_id"],
        "user_id": user["_id"],
        "student_name": user.get("name"),
        "menu_item_id": menu["_id"],
        "menu_item_name": menu["name"],
        "rating": rating,
        "comment": data.get("comment", ""),
        "created_at": datetime.now(timezone.utc)
    }
    doc["_id"] = db.feedback.insert_one(doc).inserted_id
    return ok(doc, "feedback submitted")

@feedback_bp.get("")
@require_auth("admin", "staff")
def list_feedback():
    return ok(list(db.feedback.find({}).sort("created_at", -1).limit(100)))
