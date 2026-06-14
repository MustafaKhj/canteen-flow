from flask import Blueprint, request
from backend.db import db
from backend.utils.auth import hash_password, verify_password, create_token
from backend.utils.json import ok, APIError
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(force=True)
    required = ["name", "email", "password", "role"]
    for field in required:
        if not data.get(field):
            raise APIError(f"{field} is required")
    if data["role"] not in ["student", "staff", "admin"]:
        raise APIError("Invalid role")
    user = {
        "name": data["name"].strip(),
        "email": data["email"].lower().strip(),
        "password_hash": hash_password(data["password"]),
        "role": data["role"],
        "wallet_balance": float(data.get("wallet_balance", 2000 if data["role"] == "student" else 0)),
        "created_at": datetime.now(timezone.utc)
    }
    try:
        inserted = db.users.insert_one(user)
    except Exception:
        raise APIError("Email already exists")
    user["_id"] = inserted.inserted_id
    token = create_token(user)
    user.pop("password_hash", None)
    return ok({"token": token, "user": user}, "registered")

@auth_bp.post("/login")
def login():
    data = request.get_json(force=True)
    user = db.users.find_one({"email": data.get("email", "").lower().strip()})
    if not user or not verify_password(data.get("password", ""), user["password_hash"]):
        raise APIError("Invalid email or password", 401)
    token = create_token(user)
    user.pop("password_hash", None)
    return ok({"token": token, "user": user}, "logged in")
