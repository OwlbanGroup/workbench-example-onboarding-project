"""Database module for Redis integration."""

import json
import logging
import os
from typing import Optional

import redis  # pylint: disable=import-error

# Fallback in-memory storage for when Redis is not available
users_db: dict = {}
app_db: dict = {}


def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)


def store_user_data(user_id: str, data: dict) -> bool:
    """Store user data in Redis or fallback to in-memory."""
    try:
        client = get_redis_client()
        key = f"user:{user_id}"
        # Serialize nested data to JSON string for Redis hash storage
        serialized_data = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()}
        client.hset(key, mapping=serialized_data)
        return True
    except redis.RedisError as e:
        logging.error("Redis error storing user data for user_id=%s: %s", user_id, e)
        # Fallback to in-memory storage
        users_db[user_id] = data
        return True


def get_user_data(user_id: str) -> Optional[dict]:
    """Retrieve user data from Redis or fallback to in-memory."""
    try:
        client = get_redis_client()
        key = f"user:{user_id}"
        data = client.hgetall(key)
        if data:
            # Deserialize
            for k, v in data.items():
                if k == "progress" and v:
                    try:
                        data[k] = json.loads(v)
                    except (json.JSONDecodeError, TypeError):
                        pass
                elif isinstance(v, str):
                    # Try to deserialize if it's JSON
                    try:
                        data[k] = json.loads(v)
                    except (json.JSONDecodeError, TypeError):
                        pass
            return data
        return None  # type: ignore
    except redis.RedisError:
        return users_db.get(user_id)


def store_app_data(key: str, value: str) -> bool:
    """Store application data in Redis or fallback to in-memory."""
    try:
        client = get_redis_client()
        client.set(key, value)
        return True
    except redis.RedisError:
        app_db[key] = value
        return True


def get_app_data(key: str) -> Optional[str]:
    """Retrieve application data from Redis or fallback to in-memory."""
    try:
        client = get_redis_client()
        return client.get(key)  # type: ignore
    except redis.RedisError:
        return app_db.get(key)
