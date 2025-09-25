# TODO: Fix Pylint Warnings

## src/tutorial_app/streamlit_app.py
- [x] Move import streamlit as st to top
- [x] Move import httpx to top
- [x] Move from common.sidebar import APP_SIDEBAR to top
- [x] Move from common.middleware import setup_middleware to top
- [x] Change except Exception to except httpx.RequestError

## src/tutorial_app/common/middleware.py
- [x] Remove unused Any from typing import
- [x] Move from typing import Callable before import streamlit
- [x] Move import httpx to top level
- [x] Rename BACKEND_URL to backend_url
- [x] Change f-string logging to % formatting in auth_middleware (line 27)
- [x] Change f-string logging to % formatting in auth_middleware (line 35)
- [x] Change f-string logging to % formatting in logging_middleware (line 46)
- [x] Change f-string logging to % formatting in logging_middleware (line 48)
- [x] Change f-string logging to % formatting in logging_middleware (line 51)
- [x] Change f-string logging to % formatting in request_middleware (line 73)

## src/tutorial_app/backend/database.py
- [x] Move from typing import Optional before import redis
- [x] Change os.getenv("REDIS_PORT", 6379) to os.getenv("REDIS_PORT", "6379")
- [x] Change os.getenv("REDIS_DB", 0) to os.getenv("REDIS_DB", "0")
- [x] Change except Exception in store_user_data to except redis.RedisError
- [x] Change except Exception in get_user_data to except redis.RedisError
- [x] Change except Exception in store_app_data to except redis.RedisError
- [x] Change except Exception in get_app_data to except redis.RedisError

## src/tutorial_app/backend/main.py
- [x] Move from typing import Callable, BaseModel before third party imports
- [x] Add docstrings to UserData and AppData classes
- [x] Fix import to absolute path
- [x] Add __init__.py in backend directory
