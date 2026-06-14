from datetime import datetime, timezone
from bson import ObjectId
from backend.db import db
from backend.utils.json import APIError

ORDER_STATUSES = ["pending", "in_preparation", "ready", "delivered", "cancelled"]

def now():
    return datetime.now(timezone.utc)

def place_order(user_id, cart_items, payment_method="campus_wallet"):
    if not cart_items:
        raise APIError("Cart is empty")

    menu_ids = [ObjectId(item["menu_item_id"]) for item in cart_items]
    menu_docs = list(db.menu_items.find({"_id": {"$in": menu_ids}, "is_available": True}))
    menu_map = {str(item["_id"]): item for item in menu_docs}

    lines = []
    total = 0.0
    for item in cart_items:
        menu_id = item["menu_item_id"]
        qty = int(item.get("quantity", 1))
        if qty <= 0:
            raise APIError("Quantity must be greater than zero")
        if menu_id not in menu_map:
            raise APIError("One or more menu items are unavailable")
        menu = menu_map[menu_id]
        price = float(menu["price"])
        line_total = price * qty
        total += line_total
        lines.append({
            "menu_item_id": ObjectId(menu_id),
            "item_name": menu["name"],
            "category": menu.get("category", "General"),
            "quantity": qty,
            "unit_price": price,
            "line_total": line_total,
            "created_at": now()
        })

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise APIError("User not found", 404)
    if float(user.get("wallet_balance", 0)) < total:
        raise APIError("Insufficient wallet balance")

    order_doc = {
        "user_id": ObjectId(user_id),
        "student_name": user.get("name"),
        "status": "pending",
        "total_amount": round(total, 2),
        "created_at": now(),
        "updated_at": now()
    }

    order_id = db.orders.insert_one(order_doc).inserted_id
    for line in lines:
        line["order_id"] = order_id
    db.order_items.insert_many(lines)

    db.users.update_one({"_id": ObjectId(user_id)}, {"$inc": {"wallet_balance": -round(total, 2)}})
    db.payments.insert_one({
        "order_id": order_id,
        "user_id": ObjectId(user_id),
        "amount": round(total, 2),
        "method": payment_method,
        "status": "paid",
        "created_at": now()
    })
    db.transactions.insert_one({
        "order_id": order_id,
        "user_id": ObjectId(user_id),
        "type": "order_payment",
        "amount": round(total, 2),
        "description": "Order payment deducted from campus wallet",
        "created_at": now()
    })

    return get_order(order_id)

def get_order(order_id):
    order = db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise APIError("Order not found", 404)
    order["items"] = list(db.order_items.find({"order_id": order["_id"]}))
    order["payment"] = db.payments.find_one({"order_id": order["_id"]})
    return order

def update_order_status(order_id, status):
    if status not in ORDER_STATUSES:
        raise APIError("Invalid order status")
    db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status, "updated_at": now()}})
    return get_order(order_id)
