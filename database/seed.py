from datetime import datetime, timezone, timedelta
import random
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.db import db, init_indexes
from backend.utils.auth import hash_password
from backend.services.order_service import place_order, update_order_status

now = lambda: datetime.now(timezone.utc)

def seed():
    db.users.delete_many({})
    db.menu_items.delete_many({})
    db.orders.delete_many({})
    db.order_items.delete_many({})
    db.payments.delete_many({})
    db.inventory.delete_many({})
    db.stock_logs.delete_many({})
    db.transactions.delete_many({})
    db.feedback.delete_many({})
    db.forecasts.delete_many({})
    init_indexes()

    users = [
        {"name": "Ali Student", "email": "student@canteenflow.edu", "password_hash": hash_password("student123"), "role": "student", "wallet_balance": 50000, "created_at": now()},
        {"name": "Canteen Staff", "email": "staff@canteenflow.edu", "password_hash": hash_password("staff123"), "role": "staff", "wallet_balance": 0, "created_at": now()},
        {"name": "Admin User", "email": "admin@canteenflow.edu", "password_hash": hash_password("admin123"), "role": "admin", "wallet_balance": 0, "created_at": now()},
    ]
    db.users.insert_many(users)
    student = db.users.find_one({"email": "student@canteenflow.edu"})

    menu = [
        {"name": "Chicken Biryani", "category": "Rice", "price": 280, "description": "Campus favourite biryani plate", "calories": 620, "is_special": True, "is_available": True, "created_at": now()},
        {"name": "Zinger Burger", "category": "Fast Food", "price": 360, "description": "Crispy chicken burger", "calories": 710, "is_special": False, "is_available": True, "created_at": now()},
        {"name": "Club Sandwich", "category": "Fast Food", "price": 300, "description": "Triple-layer sandwich", "calories": 540, "is_special": False, "is_available": True, "created_at": now()},
        {"name": "Daal Chawal", "category": "Rice", "price": 180, "description": "Simple healthy meal", "calories": 480, "is_special": False, "is_available": True, "created_at": now()},
        {"name": "Paratha Roll", "category": "Snacks", "price": 220, "description": "Spicy chicken roll", "calories": 590, "is_special": True, "is_available": True, "created_at": now()},
        {"name": "Cold Coffee", "category": "Drinks", "price": 180, "description": "Chilled coffee drink", "calories": 220, "is_special": False, "is_available": True, "created_at": now()},
        {"name": "Fresh Lime", "category": "Drinks", "price": 140, "description": "Refreshing lemon soda", "calories": 90, "is_special": False, "is_available": True, "created_at": now()},
        {"name": "Fries", "category": "Snacks", "price": 160, "description": "Crispy potato fries", "calories": 350, "is_special": False, "is_available": True, "created_at": now()},
    ]
    db.menu_items.insert_many(menu)

    inventory = [
        {"item_name": "Rice", "quantity": 50, "unit": "kg", "reorder_level": 12, "created_at": now()},
        {"item_name": "Chicken", "quantity": 25, "unit": "kg", "reorder_level": 10, "created_at": now()},
        {"item_name": "Potatoes", "quantity": 8, "unit": "kg", "reorder_level": 10, "created_at": now()},
        {"item_name": "Burger Buns", "quantity": 120, "unit": "pcs", "reorder_level": 30, "created_at": now()},
        {"item_name": "Milk", "quantity": 9, "unit": "liters", "reorder_level": 10, "created_at": now()},
    ]
    db.inventory.insert_many(inventory)

    menu_items = list(db.menu_items.find({}))
    for _ in range(18):
        cart = []
        for item in random.sample(menu_items, random.randint(1, 3)):
            cart.append({"menu_item_id": str(item["_id"]), "quantity": random.randint(1, 3)})
        order = place_order(student["_id"], cart)
        status = random.choice(["pending", "in_preparation", "ready", "delivered"])
        update_order_status(order["_id"], status)
        db.orders.update_one({"_id": order["_id"]}, {"$set": {"created_at": now() - timedelta(days=random.randint(0, 29))}})

    delivered = list(db.orders.find({"status": "delivered"}).limit(5))
    for order in delivered:
        item = db.order_items.find_one({"order_id": order["_id"]})
        db.feedback.insert_one({
            "order_id": order["_id"], "user_id": student["_id"], "student_name": student["name"],
            "menu_item_id": item["menu_item_id"], "menu_item_name": item["item_name"],
            "rating": random.randint(4, 5), "comment": "Good taste and quick service.", "created_at": now()
        })
    print("Seed completed.")
    print("Student: student@canteenflow.edu / student123")
    print("Staff: staff@canteenflow.edu / staff123")
    print("Admin: admin@canteenflow.edu / admin123")

if __name__ == "__main__":
    seed()
