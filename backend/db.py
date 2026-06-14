from pymongo import MongoClient, ASCENDING, DESCENDING
from .config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]

def init_indexes():
    db.users.create_index("email", unique=True)
    db.users.create_index("role")
    db.menu_items.create_index([("category", ASCENDING), ("is_available", ASCENDING)])
    db.orders.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    db.orders.create_index("status")
    db.order_items.create_index("order_id")
    db.payments.create_index("order_id", unique=True)
    db.inventory.create_index("item_name", unique=True)
    db.stock_logs.create_index([("inventory_id", ASCENDING), ("created_at", DESCENDING)])
    db.transactions.create_index([("order_id", ASCENDING), ("created_at", DESCENDING)])
    db.feedback.create_index([("menu_item_id", ASCENDING), ("created_at", DESCENDING)])
    db.forecasts.create_index("created_at")
