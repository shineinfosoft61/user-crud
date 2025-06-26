from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis

# from database import engine
# import models
from router.admin.v1.api import router as user_router


app = FastAPI(
    title="User_crud",
    description="Fast_crud",
    version="1.0.0",
    redoc_url=None,
)

# models.Base.metadata.create_all(bind = engine)

app.include_router(user_router)


@app.on_event("startup")
async def startup():
    redis_instance = redis.Redis(host="localhost", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_instance), prefix="fastapi-cache")
