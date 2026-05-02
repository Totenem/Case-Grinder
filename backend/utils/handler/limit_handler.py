from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

async def rate_limit_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Slow down."},
    )