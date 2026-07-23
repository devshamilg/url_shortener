from redis_connection import redis_client
from fastapi import Request, HTTPException

REQUEST_LIMIT = 10
DAY_SECONDS = 60 * 60 * 24

def check_rate_limit(request: Request):
    ip = request.client.host

    key = f"rate_limit:{ip}"

    request_count = redis_client.incr(key)

    if request_count > 1:
        redis_client.expire(key, DAY_SECONDS)

    if request_count > 2:
        raise HTTPException(status_code=429, detail="Rate limit per day exceeded")
    
    