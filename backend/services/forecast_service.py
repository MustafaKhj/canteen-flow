from datetime import datetime, timezone, timedelta
from collections import defaultdict
from backend.db import db

def generate_forecast(days=30, top_n=5):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    pipeline = [
        {"$lookup": {"from": "orders", "localField": "order_id", "foreignField": "_id", "as": "order"}},
        {"$unwind": "$order"},
        {"$match": {"order.created_at": {"$gte": since}, "order.status": {"$ne": "cancelled"}}},
        {"$group": {
            "_id": {"menu_item_id": "$menu_item_id", "item_name": "$item_name", "category": "$category"},
            "total_quantity": {"$sum": "$quantity"},
            "total_revenue": {"$sum": "$line_total"},
            "order_count": {"$sum": 1}
        }},
        {"$sort": {"total_quantity": -1}},
        {"$limit": top_n}
    ]
    rows = list(db.order_items.aggregate(pipeline))
    predictions = []
    for row in rows:
        avg_daily = round(row["total_quantity"] / max(days, 1), 2)
        predicted = max(1, round(avg_daily * 1.15))
        predictions.append({
            "menu_item_id": row["_id"]["menu_item_id"],
            "item_name": row["_id"]["item_name"],
            "category": row["_id"].get("category", "General"),
            "past_30_day_quantity": row["total_quantity"],
            "predicted_next_day_quantity": predicted,
            "confidence_note": "Simple weighted moving average based on recent demand"
        })

    doc = {"created_at": datetime.now(timezone.utc), "days_used": days, "predictions": predictions}
    db.forecasts.insert_one(doc)
    return doc
