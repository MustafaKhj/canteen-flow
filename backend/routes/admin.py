from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime, timezone
from backend.db import db
from backend.utils.auth import require_auth
from backend.utils.json import ok, APIError
from backend.services.forecast_service import generate_forecast

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.get("/dashboard")
@require_auth("admin", "staff")
def dashboard():
    total_orders = db.orders.count_documents({})
    pending_orders = db.orders.count_documents({"status": "pending"})
    revenue = list(db.payments.aggregate([
        {"$match": {"status": "paid"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]))
    top_items = list(db.order_items.aggregate([
        {"$group": {"_id": "$item_name", "quantity": {"$sum": "$quantity"}, "revenue": {"$sum": "$line_total"}}},
        {"$sort": {"quantity": -1}}, {"$limit": 5}
    ]))
    feedback = list(db.feedback.aggregate([
        {"$group": {"_id": "$menu_item_name", "avg_rating": {"$avg": "$rating"}, "count": {"$sum": 1}}},
        {"$sort": {"avg_rating": -1}}
    ]))
    low_stock = list(db.inventory.find({"quantity": {"$lte": 10}}).limit(10))
    latest_forecast = db.forecasts.find_one(sort=[("created_at", -1)])
    return ok({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": round(revenue[0]["total"], 2) if revenue else 0,
        "top_items": top_items,
        "feedback_summary": feedback,
        "low_stock": low_stock,
        "latest_forecast": latest_forecast
    })

@admin_bp.get("/inventory")
@require_auth("admin", "staff")
def inventory():
    return ok(list(db.inventory.find({}).sort("item_name", 1)))

@admin_bp.post("/inventory")
@require_auth("admin")
def create_inventory():
    data = request.get_json(force=True)
    doc = {
        "item_name": data["item_name"],
        "quantity": float(data.get("quantity", 0)),
        "unit": data.get("unit", "pcs"),
        "reorder_level": float(data.get("reorder_level", 10)),
        "created_at": datetime.now(timezone.utc)
    }
    doc["_id"] = db.inventory.insert_one(doc).inserted_id
    return ok(doc, "inventory item created")

@admin_bp.patch("/inventory/<inventory_id>")
@require_auth("admin", "staff")
def update_inventory(inventory_id):
    data = request.get_json(force=True)
    change = float(data.get("change", 0))
    reason = data.get("reason", "manual adjustment")
    db.inventory.update_one({"_id": ObjectId(inventory_id)}, {"$inc": {"quantity": change}, "$set": {"updated_at": datetime.now(timezone.utc)}})
    db.stock_logs.insert_one({"inventory_id": ObjectId(inventory_id), "change": change, "reason": reason, "created_at": datetime.now(timezone.utc)})
    return ok(db.inventory.find_one({"_id": ObjectId(inventory_id)}), "inventory updated")

@admin_bp.post("/forecast")
@require_auth("admin", "staff")
def forecast():
    return ok(generate_forecast(), "forecast generated")
