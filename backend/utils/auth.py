from functools import wraps
from flask import request
from bson import ObjectId
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import Config
from backend.db import db
from backend.utils.json import APIError

VALID_ROLES = {"student", "staff", "admin"}

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

def create_token(user):
    payload = {
        "sub": str(user["_id"]),
        "role": user["role"],
        "name": user.get("name", ""),
        "exp": datetime.now(timezone.utc) + timedelta(hours=10)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def get_current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise APIError("Authorization token is missing", 401)
    token = auth.replace("Bearer ", "", 1)
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise APIError("Session expired. Please login again.", 401)
    except jwt.InvalidTokenError:
        raise APIError("Invalid authorization token", 401)
    user = db.users.find_one({"_id": ObjectId(payload["sub"])}, {"password_hash": 0})
    if not user:
        raise APIError("User not found", 401)
    return user

def require_auth(*roles):
    allowed = set(roles) if roles else VALID_ROLES
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user.get("role") not in allowed:
                raise APIError("You do not have permission to access this resource", 403)
            request.current_user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator
