from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime, timezone
from backend.db import db
from backend.utils.auth import require_auth
from backend.utils.json import ok, APIError

menu_bp = Blueprint("menu", __name__, url_prefix="/api/menu")

@menu_bp.get("")
def list_menu():
    category = request.args.get("category")
    query = {"is_available": True}
    if category:
        query["category"] = category
    items = list(db.menu_items.find(query).sort("category", 1))
    return ok(items)

@menu_bp.post("")
@require_auth("admin")
def create_item():
    data = request.get_json(force=True)
    for field in ["name", "category", "price"]:
        if not data.get(field):
            raise APIError(f"{field} is required")
    doc = {
        "name": data["name"].strip(),
        "category": data["category"].strip(),
        "price": float(data["price"]),
        "description": data.get("description", ""),
        "calories": int(data.get("calories", 0)),
        "is_special": bool(data.get("is_special", False)),
        "is_available": bool(data.get("is_available", True)),
        "created_at": datetime.now(timezone.utc)
    }
    doc["_id"] = db.menu_items.insert_one(doc).inserted_id
    return ok(doc, "menu item created")

@menu_bp.put("/<item_id>")
@require_auth("admin")
def update_item(item_id):
    data = request.get_json(force=True)
    allowed = {"name", "category", "price", "description", "calories", "is_special", "is_available"}
    update = {k: data[k] for k in allowed if k in data}
    if "price" in update:
        update["price"] = float(update["price"])
    update["updated_at"] = datetime.now(timezone.utc)
    db.menu_items.update_one({"_id": ObjectId(item_id)}, {"$set": update})
    return ok(db.menu_items.find_one({"_id": ObjectId(item_id)}), "menu item updated")

@menu_bp.delete("/<item_id>")
@require_auth("admin")
def delete_item(item_id):
    db.menu_items.update_one({"_id": ObjectId(item_id)}, {"$set": {"is_available": False, "updated_at": datetime.now(timezone.utc)}})
    return ok(message="menu item disabled")
